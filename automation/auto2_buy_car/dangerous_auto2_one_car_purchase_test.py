import argparse

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
from core.input import InputController
from core.input.real_keyboard_backend import (
    RealKeyboardBackendError,
    create_real_keyboard_backend,
)
from core.input.stop_hotkey import StopHotkeyError, register_stop_hotkey
from core.stop import StopManager
from licensing import (
    EntitlementDeniedError,
    ExecutionEntitlementService,
    require_execution_entitlement,
)
from profiles.profile_selection import ProfileSelectionError, load_profile_for_automation


class Auto2PurchaseTestError(Exception):
    """Raised when guarded Auto2 purchase-test execution cannot start."""


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Dangerous manual Auto2 one-car purchase test. "
            "Test-only and credits will be spent. Example: "
            "python -B -m automation.auto2_buy_car.dangerous_auto2_one_car_purchase_test "
            "1 --confirm-real-input --confirm-purchase --profile auto2_safe_slow"
        )
    )
    parser.add_argument(
        "cycles",
        type=int,
        help="Must be exactly 1 for the one-car purchase test.",
    )
    parser.add_argument(
        "--confirm-real-input",
        action="store_true",
        help="Required. Confirms that Auto2 may send real keyboard input.",
    )
    parser.add_argument(
        "--confirm-purchase",
        action="store_true",
        help="Required. Confirms that this test may spend credits.",
    )
    parser.add_argument(
        "--profile",
        help="Optional profile_id, profile_name, or profile filename stem to use.",
    )
    args = parser.parse_args()

    logger = configure_logging()

    command_label = "Auto2 one-car purchase test"

    if not require_confirmations(
        command_label,
        [
            ConfirmationRequirement("confirm-real-input", args.confirm_real_input),
            ConfirmationRequirement("confirm-purchase", args.confirm_purchase),
        ],
        logger,
    ):
        return 1

    if not validate_cycle_count(args.cycles, command_label, logger, exact_count=1):
        return 1

    try:
        profile_data = load_purchase_test_profile(args.profile)
    except (Auto2PurchaseTestError, ProfileSelectionError) as error:
        logger.error(
            "Auto2 one-car purchase profile selection failed: %s",
            error,
            category="profile",
        )
        print_error(f"Auto2 one-car purchase profile selection failed: {error}")
        return 1

    estimated_total_cost = profile_data["estimated_cost_per_car"] * args.cycles

    print_command_intro(
        "Auto2 One-Car Purchase Test",
        ["This test sends real keyboard input and will spend credits."],
        args.cycles,
        mode="purchase_test",
        profile=profile_data["profile_id"],
        estimated_total_cost=estimated_total_cost,
        f8_stop_available=True,
    )
    logger.warning("Auto2 one-car purchase test starting.", category="sequence")

    try:
        result = run_auto2_one_car_purchase_test(
            cycle_count=args.cycles,
            profile_data=profile_data,
            logger=logger,
        )
    except Auto2PurchaseTestError as error:
        logger.error("Auto2 one-car purchase test unavailable: %s", error, category="error")
        print_error(f"Auto2 one-car purchase test unavailable: {error}")
        return 1

    print_result_summary(
        result,
        estimated_total_cost=estimated_total_cost,
    )

    if result.completed:
        logger.warning("Auto2 one-car purchase test completed.", category="sequence")
        return 0

    if result.stopped:
        logger.warning("Auto2 one-car purchase test stopped.", category="sequence")
        return 1

    logger.error("Auto2 one-car purchase test failed: %s", result.message, category="error")
    print_error(result.message)
    return 1


def load_purchase_test_profile(profile_name: str | None) -> dict:
    return load_profile_for_automation(
        profile_name,
        "auto2_buy_car",
        DEFAULT_AUTO2_PROFILE_PATH,
    )


def run_auto2_one_car_purchase_test(
    cycle_count: int,
    profile_data: dict,
    logger: ProjectLogger,
    license_service: ExecutionEntitlementService | None = None,
) -> Auto2LoopResult:
    stop_manager = StopManager()

    try:
        require_execution_entitlement(
            "auto2",
            mode="purchase",
            license_service=license_service,
        )
        input_controller = InputController(create_real_keyboard_backend())
        stop_hotkey_registration = register_f8_stop_hotkey(stop_manager, logger)
    except (EntitlementDeniedError, RealKeyboardBackendError, StopHotkeyError) as error:
        raise Auto2PurchaseTestError(str(error)) from error

    runner = Auto2BuyCarRunner(
        input_controller=input_controller,
        stop_manager=stop_manager,
        profile_data=profile_data,
        logger=logger,
    )

    try:
        return runner.run_cycles(cycle_count)
    finally:
        stop_hotkey_registration.unregister()


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
