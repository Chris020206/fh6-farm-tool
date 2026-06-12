import argparse

from app.commands import (
    ConfirmationRequirement,
    print_command_intro,
    print_error,
    print_result_summary,
    require_confirmations,
    validate_cycle_count,
)
from app_logging.log_manager import configure_logging
from automation.auto1_race.auto1_runner import DEFAULT_AUTO1_PROFILE_PATH
from automation.auto1_race.manual_real_input_runner import (
    Auto1ManualRunError,
    run_manual_real_input_auto1,
)
from profiles.profile_selection import ProfileSelectionError, load_profile_for_automation


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Official guarded manual Auto1 command. Example: "
            "python -B -m automation.auto1_race.run_auto1 25 --confirm"
        )
    )
    parser.add_argument(
        "cycles",
        type=int,
        help="Finite number of Auto1 cycles to run.",
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Required. Confirms that Auto1 may send real keyboard input.",
    )
    parser.add_argument(
        "--profile",
        help="Optional profile_id, profile_name, or profile filename stem to use.",
    )
    args = parser.parse_args()

    logger = configure_logging()

    if not require_confirmations(
        "Auto1",
        [ConfirmationRequirement("confirm", args.confirm)],
        logger,
    ):
        return 1

    if not validate_cycle_count(args.cycles, "Auto1", logger):
        return 1

    try:
        profile_data = load_profile_for_automation(
            args.profile,
            "auto1_race",
            DEFAULT_AUTO1_PROFILE_PATH,
        )
    except ProfileSelectionError as error:
        logger.error("Auto1 profile selection failed: %s", error, category="profile")
        print_error(f"Auto1 profile selection failed: {error}")
        return 1

    print_command_intro(
        "Auto1 Official Manual Run",
        [
            "Auto1 will send real keyboard input.",
        ],
        args.cycles,
        mode="manual_real_input",
        profile=profile_data["profile_id"],
        f8_stop_available=True,
    )
    logger.warning("Official Auto1 manual run starting.", category="sequence")

    try:
        result = run_manual_real_input_auto1(
            cycle_count=args.cycles,
            use_fast_timings=False,
            logger=logger,
            profile_data=profile_data,
        )
    except Auto1ManualRunError as error:
        logger.error("Auto1 manual run unavailable: %s", error, category="error")
        print_error(f"Auto1 manual run unavailable: {error}")
        return 1

    print_result_summary(result)

    if result.completed:
        logger.warning("Official Auto1 manual run completed.", category="sequence")
        return 0

    if result.stopped:
        logger.warning("Official Auto1 manual run stopped.", category="sequence")
        return 1

    logger.error("Official Auto1 manual run failed: %s", result.message, category="error")
    print_error(result.message)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
