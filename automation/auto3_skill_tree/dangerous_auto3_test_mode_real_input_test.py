import argparse
from copy import deepcopy

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
    build_auto3_first_car_exception_test_actions,
    build_auto3_real_input_normal_next_car_test_actions,
)
from core.input import InputController
from core.input.real_keyboard_backend import (
    RealKeyboardBackendError,
    create_real_keyboard_backend,
)
from core.input.stop_hotkey import StopHotkeyError, register_stop_hotkey
from core.stop import StopManager
from profiles.profile_selection import ProfileSelectionError, load_profile_for_automation


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
ACTION_BUILDERS = {
    "first-car-test": build_auto3_first_car_exception_test_actions,
    "normal-next-car-test": build_auto3_real_input_normal_next_car_test_actions,
}


class Auto3TestModeRealInputError(Exception):
    """Raised when guarded Auto3 test-mode real-input execution cannot start."""


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Dangerous manual Auto3 test-mode real-input test. "
            "Test-only and no perk unlock actions are included. Example: "
            "python -B -m automation.auto3_skill_tree.dangerous_auto3_test_mode_real_input_test "
            "--mode first-car-test --confirm-real-input"
        )
    )
    parser.add_argument(
        "--mode",
        choices=sorted(ACTION_BUILDERS),
        default="first-car-test",
        help="Auto3 real-input test-mode sequence to run.",
    )
    parser.add_argument(
        "--confirm-real-input",
        action="store_true",
        help="Required. Confirms that Auto3 may send real keyboard input.",
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
    command_label = "Auto3 test-mode real-input test"

    if not require_confirmations(
        command_label,
        [ConfirmationRequirement("confirm-real-input", args.confirm_real_input)],
        logger,
    ):
        return 1

    try:
        profile_data = load_test_mode_profile(args.fast, args.profile)
    except ProfileSelectionError as error:
        logger.error(
            "Auto3 test-mode profile selection failed: %s",
            error,
            category="profile",
        )
        print_error(f"Auto3 test-mode profile selection failed: {error}")
        return 1

    print_command_intro(
        "Auto3 Test-Mode Real-Input Validation",
        ["This test sends real keyboard input."],
        requested_cycles=1,
        mode=args.mode,
        profile=profile_data["profile_id"],
        notes=["No perk unlock actions are included."],
        f8_stop_available=True,
    )
    logger.warning("Auto3 test-mode real-input starting.", category="sequence")

    try:
        result = run_auto3_test_mode_real_input(
            mode=args.mode,
            profile_data=profile_data,
            logger=logger,
        )
    except Auto3TestModeRealInputError as error:
        logger.error(
            "Auto3 test-mode real-input unavailable: %s",
            error,
            category="error",
        )
        print_error(f"Auto3 test-mode real-input unavailable: {error}")
        return 1

    print()
    print("## Run Summary")
    print()
    print(f"Mode: {args.mode}")
    print(f"Profile: {profile_data['profile_id']}")
    print(f"Final status: {result.status}")

    if result.completed:
        logger.warning("Auto3 test-mode real-input completed.", category="sequence")
        return 0

    if result.stopped:
        logger.warning("Auto3 test-mode real-input stopped.", category="sequence")
        return 1

    logger.error(
        "Auto3 test-mode real-input failed: %s",
        result.message,
        category="error",
    )
    print_error(result.message)
    return 1


def run_auto3_test_mode_real_input(
    mode: str,
    profile_data: dict,
    logger: ProjectLogger,
) -> Auto3RunResult:
    stop_manager = StopManager()

    try:
        input_controller = InputController(create_real_keyboard_backend())
        stop_hotkey_registration = register_f8_stop_hotkey(stop_manager, logger)
    except (RealKeyboardBackendError, StopHotkeyError) as error:
        raise Auto3TestModeRealInputError(str(error)) from error

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


def load_test_mode_profile(use_fast_timings: bool, profile_name: str | None) -> dict:
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
