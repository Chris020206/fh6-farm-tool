import argparse

from app_logging.log_manager import configure_logging
from core.input.input_controller import InputController
from core.input.real_keyboard_backend import (
    RealKeyboardBackendError,
    create_real_keyboard_backend,
)
from core.timing import TimingSystem


DEFAULT_TEST_KEY = "shift"
HOLD_DURATION_SECONDS = 0.1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dangerous manual smoke test for real keyboard input."
    )
    parser.add_argument(
        "--confirm-real-input",
        action="store_true",
        help="Required. Confirms that this test may send real keyboard input.",
    )
    parser.add_argument(
        "--key",
        default=DEFAULT_TEST_KEY,
        help="Key to test. Default is a short Shift press/hold.",
    )
    args = parser.parse_args()

    logger = configure_logging()

    if not args.confirm_real_input:
        message = (
            "Refusing to run real keyboard smoke test without "
            "--confirm-real-input."
        )
        logger.warning(message, category="input")
        print(message)
        return 1

    logger.warning("Real keyboard smoke test starting.", category="input")

    try:
        input_controller = InputController(create_real_keyboard_backend())
    except RealKeyboardBackendError as error:
        logger.error("Real keyboard smoke test unavailable: %s", error, category="input")
        print(f"Real keyboard smoke test unavailable: {error}")
        return 1

    timing_system = TimingSystem()

    try:
        input_controller.press_key(args.key)
        input_controller.hold_key(args.key)
        timing_system.wait(HOLD_DURATION_SECONDS)
        input_controller.release_key(args.key)
        input_controller.release_all_keys()
    except Exception as error:
        input_controller.release_all_keys()
        logger.error("Real keyboard smoke test failed: %s", error, category="error")
        print(f"Real keyboard smoke test failed: {error}")
        return 1

    logger.warning("Real keyboard smoke test completed.", category="input")
    print("Real keyboard smoke test completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
