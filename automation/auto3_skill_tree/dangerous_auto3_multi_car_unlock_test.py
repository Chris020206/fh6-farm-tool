import argparse
from copy import deepcopy

from app.commands import (
    CommandResult,
    CommandStatus,
    ConfirmationRequirement,
    OperatorMessage,
    RefusalReason,
    RiskLevel,
    RunSummary,
    print_command_intro,
    print_error,
    print_refusal,
    print_run_summary,
    require_confirmations,
)
from app_logging.log_manager import ProjectLogger, configure_logging
from automation.auto3_skill_tree.auto3_result import Auto3RunResult
from automation.auto3_skill_tree.auto3_runner import (
    DEFAULT_AUTO3_PROFILE_PATH,
    Auto3SkillTreeRunner,
)
from automation.auto3_skill_tree.auto3_sequence import (
    build_auto3_multi_car_unlock_actions,
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


MAX_CARS = 4
FAST_TIMINGS = {
    "startup_delay": 0.1,
    "menu_key_delay": 0.1,
    "safety_navigation_key_delay": 0.1,
    "grid_transition_key_delay": 0.1,
    "escape_key_delay": 0.1,
    "return_menu_transition_delay": 0.1,
    "skill_tree_key_delay": 0.1,
    "wait_after_get_in": 0.1,
    "wait_after_get_in_next_car": 0.1,
    "wait_after_menu_open": 0.1,
    "wait_after_unlock": 0.1,
    "post_cycle_delay": 0.1,
}


class Auto3MultiCarUnlockTestError(Exception):
    """Raised when guarded Auto3 multi-car unlock execution cannot start."""


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Dangerous manual Auto3 small-count multi-car unlock test. "
            "Test-only and skill points will be spent. Example: "
            "python -B -m automation.auto3_skill_tree."
            "dangerous_auto3_multi_car_unlock_test "
            "--cars 4 --confirm-real-input --confirm-unlock"
        )
    )
    parser.add_argument(
        "--cars",
        type=int,
        required=True,
        help=f"Required. Number of cars to unlock. Must be 1-{MAX_CARS}.",
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
        "--fast",
        action="store_true",
        help=(
            "Use shortened timings for validation. Avoid this for real FH6 "
            "unlock validation unless deliberately testing timing behavior."
        ),
    )
    parser.add_argument(
        "--profile",
        help="Optional profile_id, profile_name, or profile filename stem to use.",
    )
    args = parser.parse_args()

    logger = configure_logging()
    command_label = "Auto3 multi-car unlock test"

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
        validate_car_count(args.cars)
    except ValueError as error:
        logger.error(str(error), category="error")
        print_refusal(build_car_count_refusal(str(error), args.cars))
        return 1

    try:
        profile_data = load_unlock_test_profile(args.fast, args.profile)
    except ProfileSelectionError as error:
        logger.error(
            "Auto3 multi-car unlock profile selection failed: %s",
            error,
            category="profile",
        )
        print_error(f"Auto3 multi-car unlock profile selection failed: {error}")
        return 1

    print_command_intro(
        "Auto3 Multi-Car Unlock Test",
        [
            "This test sends real keyboard input.",
            "This test will spend skill points.",
        ],
        requested_cycles=1,
        mode="multi-car-unlock-test",
        profile=profile_data["profile_id"],
        notes=[
            f"Cars: {args.cars}",
            "Dangerous/manual/test-only. Not a production command.",
        ],
        f8_stop_available=True,
    )
    logger.warning("Auto3 multi-car unlock test starting.", category="sequence")

    try:
        result = run_auto3_multi_car_unlock_test(
            car_count=args.cars,
            profile_data=profile_data,
            logger=logger,
        )
    except Auto3MultiCarUnlockTestError as error:
        logger.error(
            "Auto3 multi-car unlock test unavailable: %s",
            error,
            category="error",
        )
        print_error(f"Auto3 multi-car unlock test unavailable: {error}")
        return 1

    print_run_summary(
        RunSummary(
            status=CommandStatus(result.status),
            command="Auto3 Multi-Car Unlock Test",
            fields=[
                ("Mode", "multi-car-unlock-test"),
                ("Cars", args.cars),
                ("Profile", profile_data["profile_id"]),
                ("Final status", result.status),
            ],
            operator_message=OperatorMessage(
                message=(
                    "Auto3 returned control after guarded multi-car unlock execution."
                ),
                suggested_next_step=(
                    "Verify FH6 baseline and selected car state before another run."
                ),
                risk_level=RiskLevel.MEDIUM,
            ),
        )
    )

    if result.completed:
        logger.warning("Auto3 multi-car unlock test completed.", category="sequence")
        return 0

    if result.stopped:
        logger.warning("Auto3 multi-car unlock test stopped.", category="sequence")
        return 1

    logger.error(
        "Auto3 multi-car unlock test failed: %s",
        result.message,
        category="error",
    )
    print_error(result.message)
    return 1


def validate_car_count(car_count: int) -> None:
    if not isinstance(car_count, int):
        raise ValueError("cars must be an integer.")

    if car_count <= 0:
        raise ValueError("cars must be greater than 0.")

    if car_count > MAX_CARS:
        raise ValueError(f"cars must be {MAX_CARS} or fewer.")


def build_car_count_refusal(message: str, car_count: int) -> CommandResult:
    details: list[tuple[str, object]] = [
        ("Requested cars", car_count),
        ("Current validated limit", f"{MAX_CARS} cars"),
        ("Validated traversal", "A1 -> B1 -> C1 -> A2"),
    ]

    return CommandResult(
        status=CommandStatus.REFUSED,
        command="Auto3 Multi-Car Unlock Test",
        reason="Requested car count is outside the current validated boundary.",
        refusal_reason=RefusalReason.INVALID_COUNT,
        operator_message=OperatorMessage(
            message=message,
            required_action=f"Choose 1-{MAX_CARS} cars.",
            suggested_next_step=(
                "Use the validated A-start traversal boundary until a future "
                "scaling milestone changes it."
            ),
            risk_level=RiskLevel.MEDIUM,
        ),
        details=details,
    )


def run_auto3_multi_car_unlock_test(
    car_count: int,
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
        raise Auto3MultiCarUnlockTestError(str(error)) from error

    runner = Auto3SkillTreeRunner(
        input_controller=input_controller,
        stop_manager=stop_manager,
        profile_data=profile_data,
        action_builder=lambda profile: build_auto3_multi_car_unlock_actions(
            car_count,
            profile,
        ),
        logger=logger,
    )

    try:
        return runner.run_one_cycle()
    finally:
        stop_hotkey_registration.unregister()


def load_unlock_test_profile(use_fast_timings: bool, profile_name: str | None) -> dict:
    profile_data = load_profile_for_automation(
        profile_name,
        "auto3_skill_tree",
        DEFAULT_AUTO3_PROFILE_PATH,
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
