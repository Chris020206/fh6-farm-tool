import argparse
from copy import deepcopy

from app.commands import (
    ConfirmationRequirement,
    print_command_intro,
    print_error,
    print_result_summary,
    require_confirmations,
    validate_cycle_count,
)
from app_logging.log_manager import ProjectLogger, configure_logging
from automation.auto2_buy_car.auto2_result import Auto2LoopResult
from automation.auto2_buy_car.auto2_runner import (
    DEFAULT_AUTO2_PROFILE_PATH,
    Auto2BuyCarRunner,
)
from automation.auto2_buy_car.auto2_sequence import build_auto2_test_cycle_actions
from core.input import InputController
from core.input.real_keyboard_backend import (
    RealKeyboardBackendError,
    create_real_keyboard_backend,
)
from core.input.stop_hotkey import StopHotkeyError, register_stop_hotkey
from core.stop import StopManager
from licensing import EntitlementDeniedError, LicenseService, require_execution_entitlement
from profiles.profile_selection import ProfileSelectionError, load_profile_for_automation


FAST_TIMINGS = {
    "startup_delay": 0.1,
    "menu_key_delay": 0.1,
    "wait_after_menu_confirm": 0.1,
    "wait_after_car_selection": 0.1,
    "wait_after_purchase_confirm": 0.1,
    "post_cycle_delay": 0.1,
}


class Auto2TestModeRealInputError(Exception):
    """Raised when guarded Auto2 test-mode real-input execution cannot start."""


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Dangerous manual Auto2 test-mode real-input test. "
            "Test-only and no purchase actions are included. Example: "
            "python -B -m automation.auto2_buy_car.dangerous_auto2_test_mode_real_input_test "
            "1 --confirm-real-input --profile auto2_safe_slow"
        )
    )
    parser.add_argument(
        "cycles",
        type=int,
        help="Finite number of Auto2 test-mode cycles to run.",
    )
    parser.add_argument(
        "--confirm-real-input",
        action="store_true",
        help="Required. Confirms that Auto2 may send real keyboard input.",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Use shortened official-profile timings for validation.",
    )
    parser.add_argument(
        "--profile",
        help="Optional profile_id, profile_name, or profile filename stem to use.",
    )
    args = parser.parse_args()

    logger = configure_logging()

    command_label = "Auto2 test-mode real-input test"

    if not require_confirmations(
        command_label,
        [ConfirmationRequirement("confirm-real-input", args.confirm_real_input)],
        logger,
    ):
        return 1

    if not validate_cycle_count(args.cycles, command_label, logger):
        return 1

    try:
        profile_data = load_test_mode_profile(args.fast, args.profile)
    except (Auto2TestModeRealInputError, ProfileSelectionError) as error:
        logger.error(
            "Auto2 test-mode profile selection failed: %s",
            error,
            category="profile",
        )
        print_error(f"Auto2 test-mode profile selection failed: {error}")
        return 1

    print_command_intro(
        "Auto2 Test-Mode Real-Input Validation",
        ["This test sends real keyboard input."],
        args.cycles,
        mode="test",
        profile=profile_data["profile_id"],
        notes=["No purchase actions are included."],
        f8_stop_available=True,
    )
    logger.warning("Auto2 test-mode real-input starting.", category="sequence")

    try:
        result = run_auto2_test_mode_real_input(
            cycle_count=args.cycles,
            profile_data=profile_data,
            logger=logger,
        )
    except Auto2TestModeRealInputError as error:
        logger.error(
            "Auto2 test-mode real-input unavailable: %s",
            error,
            category="error",
        )
        print_error(f"Auto2 test-mode real-input unavailable: {error}")
        return 1

    print_result_summary(result)

    if result.completed:
        logger.warning("Auto2 test-mode real-input completed.", category="sequence")
        return 0

    if result.stopped:
        logger.warning("Auto2 test-mode real-input stopped.", category="sequence")
        return 1

    logger.error(
        "Auto2 test-mode real-input failed: %s",
        result.message,
        category="error",
    )
    print_error(result.message)
    return 1


def run_auto2_test_mode_real_input(
    cycle_count: int,
    profile_data: dict,
    logger: ProjectLogger,
    license_service: LicenseService | None = None,
) -> Auto2LoopResult:
    stop_manager = StopManager()

    try:
        require_execution_entitlement(
            "auto2",
            mode="test",
            license_service=license_service,
        )
        input_controller = InputController(create_real_keyboard_backend())
        stop_hotkey_registration = register_f8_stop_hotkey(stop_manager, logger)
    except (
        EntitlementDeniedError,
        RealKeyboardBackendError,
        StopHotkeyError,
    ) as error:
        raise Auto2TestModeRealInputError(str(error)) from error

    runner = Auto2BuyCarRunner(
        input_controller=input_controller,
        stop_manager=stop_manager,
        profile_data=profile_data,
        action_builder=build_auto2_test_cycle_actions,
        logger=logger,
    )

    try:
        return runner.run_cycles(cycle_count)
    finally:
        stop_hotkey_registration.unregister()


def load_test_mode_profile(use_fast_timings: bool, profile_name: str | None) -> dict:
    profile_data = load_profile_for_automation(
        profile_name,
        "auto2_buy_car",
        DEFAULT_AUTO2_PROFILE_PATH,
    )

    if not use_fast_timings:
        return profile_data

    fast_profile_data = deepcopy(profile_data)
    fast_profile_data["timings"] = FAST_TIMINGS
    return fast_profile_data


def register_f8_stop_hotkey(
    stop_manager: StopManager,
    logger: ProjectLogger,
):
    def request_stop() -> None:
        logger.warning("F8 stop hotkey triggered.", category="stop")
        stop_manager.request_stop()

    registration = register_stop_hotkey("f8", request_stop)
    logger.warning("F8 stop hotkey registered.", category="stop")
    return registration


if __name__ == "__main__":
    raise SystemExit(main())
