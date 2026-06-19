import argparse

from app.commands import (
    ConfirmationRequirement,
    print_command_intro,
    print_error,
    require_confirmations,
)
from app_logging.log_manager import ProjectLogger, configure_logging
from automation.auto3_skill_tree.auto3_result import Auto3RunResult
from automation.auto3_skill_tree.auto3_runner import (
    DEFAULT_AUTO3_PROFILE_PATH,
    Auto3SkillTreeRunner,
)
from automation.auto3_skill_tree.auto3_sequence import (
    build_auto3_first_car_exception_actions,
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


ACTION_BUILDERS = {
    "first-car": build_auto3_first_car_exception_actions,
}


class Auto3UnlockTestError(Exception):
    """Raised when guarded Auto3 unlock-test execution cannot start."""


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Dangerous manual Auto3 one-car unlock test. "
            "Test-only and skill points may be spent. Example: "
            "python -B -m automation.auto3_skill_tree.dangerous_auto3_one_car_unlock_test "
            "--mode first-car --confirm-real-input --confirm-unlock"
        )
    )
    parser.add_argument(
        "--mode",
        choices=sorted(ACTION_BUILDERS),
        default="first-car",
        help="Auto3 unlock-test path to run. Only first-car is supported.",
    )
    parser.add_argument(
        "--confirm-real-input",
        action="store_true",
        help="Required. Confirms that Auto3 may send real keyboard input.",
    )
    parser.add_argument(
        "--confirm-unlock",
        action="store_true",
        help="Required. Confirms that this test may spend skill points.",
    )
    parser.add_argument(
        "--profile",
        help="Optional profile_id, profile_name, or profile filename stem to use.",
    )
    args = parser.parse_args()

    logger = configure_logging()
    command_label = "Auto3 one-car unlock test"

    if not require_confirmations(
        command_label,
        [
            ConfirmationRequirement("confirm-real-input", args.confirm_real_input),
            ConfirmationRequirement("confirm-unlock", args.confirm_unlock),
        ],
        logger,
    ):
        return 1

    try:
        profile_data = load_unlock_test_profile(args.profile)
    except ProfileSelectionError as error:
        logger.error(
            "Auto3 one-car unlock profile selection failed: %s",
            error,
            category="profile",
        )
        print_error(f"Auto3 one-car unlock profile selection failed: {error}")
        return 1

    print_command_intro(
        "Auto3 One-Car Unlock Test",
        ["This test sends real keyboard input and may spend skill points."],
        requested_cycles=1,
        mode="unlock_test",
        profile=profile_data["profile_id"],
        notes=["Path: first-car"],
        f8_stop_available=True,
    )
    logger.warning("Auto3 one-car unlock test starting.", category="sequence")

    try:
        result = run_auto3_one_car_unlock_test(
            mode=args.mode,
            profile_data=profile_data,
            logger=logger,
        )
    except Auto3UnlockTestError as error:
        logger.error("Auto3 one-car unlock test unavailable: %s", error, category="error")
        print_error(f"Auto3 one-car unlock test unavailable: {error}")
        return 1

    print()
    print("## Run Summary")
    print()
    print("Mode: unlock_test")
    print("Path: first-car")
    print(f"Profile: {profile_data['profile_id']}")
    print(f"Final status: {result.status}")

    if result.completed:
        logger.warning("Auto3 one-car unlock test completed.", category="sequence")
        return 0

    if result.stopped:
        logger.warning("Auto3 one-car unlock test stopped.", category="sequence")
        return 1

    logger.error("Auto3 one-car unlock test failed: %s", result.message, category="error")
    print_error(result.message)
    return 1


def load_unlock_test_profile(profile_name: str | None) -> dict:
    return load_profile_for_automation(
        profile_name,
        "auto3_skill_tree",
        DEFAULT_AUTO3_PROFILE_PATH,
    )


def run_auto3_one_car_unlock_test(
    mode: str,
    profile_data: dict,
    logger: ProjectLogger,
    license_service: ExecutionEntitlementService | None = None,
) -> Auto3RunResult:
    stop_manager = StopManager()

    try:
        require_execution_entitlement(
            "auto3",
            mode="unlock",
            license_service=license_service,
        )
        input_controller = InputController(create_real_keyboard_backend())
        stop_hotkey_registration = register_f8_stop_hotkey(stop_manager, logger)
    except (
        EntitlementDeniedError,
        RealKeyboardBackendError,
        StopHotkeyError,
    ) as error:
        raise Auto3UnlockTestError(str(error)) from error

    runner = Auto3SkillTreeRunner(
        input_controller=input_controller,
        stop_manager=stop_manager,
        profile_data=profile_data,
        action_builder=ACTION_BUILDERS[mode],
        logger=logger,
    )

    try:
        return runner.run_one_cycle()
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
