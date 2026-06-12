import argparse
from copy import deepcopy

from app.commands import (
    print_command_intro,
    print_error,
    print_result_summary,
    validate_cycle_count,
)
from app_logging.log_manager import configure_logging
from automation.auto2_buy_car.auto2_runner import (
    DEFAULT_AUTO2_PROFILE_PATH,
    Auto2BuyCarRunner,
)
from automation.auto2_buy_car.auto2_sequence import build_auto2_test_cycle_actions
from core.input import InputController
from core.input.input_backend import InMemoryInputBackend
from profiles.profile_selection import ProfileSelectionError, load_profile_for_automation


FAST_TIMINGS = {
    "startup_delay": 0.0,
    "menu_key_delay": 0.0,
    "wait_after_menu_confirm": 0.0,
    "wait_after_car_selection": 0.0,
    "wait_after_purchase_confirm": 0.0,
    "post_cycle_delay": 0.0,
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Test-only Auto2 runner using in-memory input. Example: "
            "python -B -m automation.auto2_buy_car.auto2_cli_test 1 --fast --test-mode"
        )
    )
    parser.add_argument(
        "cycles",
        type=int,
        help="Finite number of Auto2 cycles to run.",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Use zero-delay timings for quick validation.",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Navigate to purchase path without purchase actions.",
    )
    parser.add_argument(
        "--profile",
        help="Optional profile_id, profile_name, or profile filename stem to use.",
    )
    args = parser.parse_args()

    logger = configure_logging()

    if not validate_cycle_count(args.cycles, "Auto2 CLI test", logger):
        return 1

    try:
        profile_data = _load_profile(args.fast, args.profile)
    except ProfileSelectionError as error:
        logger.error("Auto2 profile selection failed: %s", error, category="profile")
        print_error(f"Auto2 profile selection failed: {error}")
        return 1

    input_controller = InputController(InMemoryInputBackend())
    runner = Auto2BuyCarRunner(
        input_controller=input_controller,
        profile_data=profile_data,
        action_builder=build_auto2_test_cycle_actions if args.test_mode else None,
        logger=logger,
    )
    print_command_intro(
        "Auto2 In-Memory CLI Test",
        [],
        args.cycles,
        mode="test" if args.test_mode else "full",
        profile=profile_data["profile_id"],
        estimated_total_cost=_calculate_estimated_total_cost(profile_data, args.cycles),
    )
    result = runner.run_cycles(args.cycles)
    estimated_total_cost = _calculate_estimated_total_cost(
        profile_data,
        result.requested_cycles,
    )

    print_result_summary(
        result,
        estimated_total_cost=estimated_total_cost,
    )

    if result.failed:
        print_error(result.message)
        return 1

    return 0


def _load_profile(use_fast_timings: bool, profile_name: str | None) -> dict:
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


def _calculate_estimated_total_cost(profile_data: dict, requested_cycles: int) -> float:
    if requested_cycles <= 0:
        return 0

    return profile_data["estimated_cost_per_car"] * requested_cycles


if __name__ == "__main__":
    raise SystemExit(main())
