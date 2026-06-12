import argparse

from app_logging.log_manager import configure_logging
from automation.auto1_race.auto1_runner import Auto1RaceRunner
from core.input import InputController
from core.input.input_backend import InMemoryInputBackend


FAST_TEST_PROFILE = {
    "profile_id": "auto1_cli_test",
    "profile_name": "Auto1 CLI Test",
    "profile_type": "auto1_race",
    "profile_version": "1.0.0",
    "is_official": False,
    "description": "Test-only fast Auto1 profile for in-memory CLI validation.",
    "keys": {
        "restart_key": "x",
        "confirm_key": "enter",
        "throttle_key": "w",
    },
    "timings": {
        "startup_delay": 0.0,
        "wait_after_restart": 0.0,
        "wait_after_first_confirm": 0.0,
        "race_duration": 0.0,
        "post_cycle_delay": 0.0,
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Test-only Auto1 runner using in-memory input."
    )
    parser.add_argument(
        "cycles",
        type=int,
        help="Finite number of Auto1 cycles to run.",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Use a zero-delay test profile for quick validation.",
    )
    args = parser.parse_args()

    logger = configure_logging()
    input_controller = InputController(InMemoryInputBackend())
    profile_data = FAST_TEST_PROFILE if args.fast else None
    runner = Auto1RaceRunner(
        input_controller=input_controller,
        profile_data=profile_data,
        logger=logger,
    )
    result = runner.run_cycles(args.cycles)

    print(f"requested_cycles: {result.requested_cycles}")
    print(f"completed_cycles: {result.completed_cycles}")
    print(f"final_status: {result.status}")

    if result.failed:
        print(f"message: {result.message}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
