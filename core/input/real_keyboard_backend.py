from core.input.input_backend import InputBackend


class RealKeyboardBackendError(Exception):
    """Raised when the real keyboard backend cannot be used safely."""


class RealKeyboardBackend:
    def __init__(self) -> None:
        try:
            import keyboard
        except ImportError as error:
            raise RealKeyboardBackendError(
                "Real keyboard backend requires the optional 'keyboard' package."
            ) from error

        self._keyboard = keyboard

    def press_key(self, key_name: str) -> None:
        self._keyboard.press_and_release(key_name)

    def hold_key(self, key_name: str) -> None:
        self._keyboard.press(key_name)

    def release_key(self, key_name: str) -> None:
        self._keyboard.release(key_name)


def create_real_keyboard_backend() -> InputBackend:
    return RealKeyboardBackend()
