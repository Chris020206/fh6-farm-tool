import argparse
from copy import deepcopy

from app.commands import print_command_intro, print_error
from app_logging.log_manager import configure_logging
from automation.auto3_skill_tree.auto3_runner import (
    DEFAULT_AUTO3_PROFILE_PATH,
    Auto3SkillTreeRunner,
)
from automation.auto3_skill_tree.auto3_sequence import (
    build_auto3_cycle_actions,
    build_auto3_first_car_exception_test_actions,
    build_auto3_multi_car_test_actions,
    build_auto3_multi_car_unlock_actions,
    build_auto3_normal_next_car_test_actions,
)
from core.input import InputController
from core.input.input_backend import InMemoryInputBackend
from profiles.profile_selection import ProfileSelectionError, load_profile_for_automation


FAST_TIMINGS = {
    "startup_delay": 0.0,
    "menu_key_delay": 0.0,
    "skill_tree_key_delay": 0.0,
    "wait_after_get_in": 0.0,
    "wait_after_get_in_next_car": 0.0,
    "wait_after_menu_open": 0.0,
    "wait_after_unlock": 0.0,
    "post_cycle_delay": 0.0,
}
ACTION_BUILDERS = {
    "first-car-test": build_auto3_first_car_exception_test_actions,
    "normal-next-car-test": build_auto3_normal_next_car_test_actions,
    "multi-car-test": None,
    "multi-car-unlock": None,
    "full-first-car": build_auto3_cycle_actions,
    "full-normal-next-car": lambda profile_data: build_auto3_cycle_actions(
        profile_data,
        is_first_car=False,
    ),
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Test-only Auto3 runner using in-memory input. Example: "
            "python -B -m automation.auto3_skill_tree.auto3_cli_test "
        "--mode first-car-test --fast"
        )
    )
    parser.add_argument(
        "--mode",
        choices=sorted(ACTION_BUILDERS),
        default="first-car-test",
        help="Auto3 in-memory sequence mode to run.",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Use zero-delay timings for quick validation.",
    )
    parser.add_argument(
        "--profile",
        help="Optional profile_id, profile_name, or profile filename stem to use.",
    )
    parser.add_argument(
        "--cars",
        type=int,
        default=1,
        help=(
            "Number of cars for --mode multi-car-test or "
            "--mode multi-car-unlock. Must be greater than 0."
        ),
    )
    args = parser.parse_args()

    logger = configure_logging()

    try:
        action_builder = _get_action_builder(args.mode, args.cars)
    except ValueError as error:
        print_error(str(error))
        return 1

    try:
        profile_data = _load_profile(args.fast, args.profile)
    except ProfileSelectionError as error:
        logger.error("Auto3 profile selection failed: %s", error, category="profile")
        print_error(f"Auto3 profile selection failed: {error}")
        return 1

    input_controller = InputController(InMemoryInputBackend())
    runner = Auto3SkillTreeRunner(
        input_controller=input_controller,
        profile_data=profile_data,
        action_builder=action_builder,
        logger=logger,
    )
    print_command_intro(
        "Auto3 In-Memory CLI Test",
        [],
        requested_cycles=1,
        mode=args.mode,
        profile=profile_data["profile_id"],
        notes=_build_intro_notes(args.mode, args.cars),
    )
    result = runner.run_one_cycle()

    print()
    print("## Run Summary")
    print()
    print(f"Mode: {args.mode}")
    if args.mode == "multi-car-test":
        print(f"Car count: {args.cars}")
    if args.mode == "multi-car-unlock":
        print(f"Car count: {args.cars}")
    print(f"Profile: {profile_data['profile_id']}")
    print(f"Final status: {result.status}")

    if result.failed:
        print_error(result.message)
        return 1

    return 0


def _get_action_builder(mode: str, car_count: int):
    if mode not in {"multi-car-test", "multi-car-unlock"}:
        return ACTION_BUILDERS[mode]

    if not isinstance(car_count, int):
        raise ValueError("cars must be an integer.")

    if car_count <= 0:
        raise ValueError("cars must be greater than 0.")

    if mode == "multi-car-test":
        return lambda profile_data: build_auto3_multi_car_test_actions(
            car_count,
            profile_data,
        )

    return lambda profile_data: build_auto3_multi_car_unlock_actions(
        car_count,
        profile_data,
    )


def _build_intro_notes(mode: str, car_count: int) -> list[str]:
    if mode == "multi-car-test":
        return [
            "Test-only: in-memory input backend.",
            f"Car count: {car_count}",
            "No perk unlock actions are included.",
        ]

    if mode == "multi-car-unlock":
        return [
            "Test-only: in-memory input backend.",
            f"Car count: {car_count}",
            "Generates unlock actions in memory only.",
            "No real keyboard input is sent.",
        ]

    return ["Test-only: in-memory input backend, one cycle only."]


def _load_profile(use_fast_timings: bool, profile_name: str | None) -> dict:
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


if __name__ == "__main__":
    raise SystemExit(main())
