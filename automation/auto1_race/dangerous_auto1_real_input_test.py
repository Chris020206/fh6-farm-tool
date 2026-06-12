import argparse

from app_logging.log_manager import configure_logging
from automation.auto1_race.manual_real_input_runner import (
    Auto1ManualRunError,
    run_manual_real_input_auto1,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dangerous manual Auto1 real-input test. Test-only."
    )
    parser.add_argument(
        "cycles",
        type=int,
        help="Finite number of Auto1 cycles to run.",
    )
    parser.add_argument(
        "--confirm-real-input",
        action="store_true",
        help="Required. Confirms that Auto1 may send real keyboard input.",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Use shortened official-profile timings for validation.",
    )
    args = parser.parse_args()

    logger = configure_logging()

    if not args.confirm_real_input:
        message = (
            "Refusing to run Auto1 real-input test without "
            "--confirm-real-input."
        )
        logger.warning(message, category="sequence")
        print(message)
        return 1

    if args.cycles <= 0:
        message = "Refusing to run Auto1 real-input test: cycles must be greater than 0."
        logger.error(message, category="error")
        print(message)
        return 1

    print("WARNING: This test sends real keyboard input.")
    print(f"requested_cycles: {args.cycles}")
    logger.warning("Auto1 real-input test starting.", category="sequence")

    try:
        result = run_manual_real_input_auto1(
            cycle_count=args.cycles,
            use_fast_timings=args.fast,
            logger=logger,
        )
    except Auto1ManualRunError as error:
        logger.error("Auto1 real-input test unavailable: %s", error, category="error")
        print(f"Auto1 real-input test unavailable: {error}")
        return 1

    print(f"requested_cycles: {result.requested_cycles}")
    print(f"completed_cycles: {result.completed_cycles}")
    print(f"final_status: {result.status}")

    if result.completed:
        logger.warning("Auto1 real-input test completed.", category="sequence")
        return 0

    if result.stopped:
        logger.warning("Auto1 real-input test stopped.", category="sequence")
        return 1

    logger.error("Auto1 real-input test failed: %s", result.message, category="error")
    print(f"message: {result.message}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
