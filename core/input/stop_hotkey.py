from collections.abc import Callable
from typing import Any


class StopHotkeyError(Exception):
    """Raised when a manual stop hotkey cannot be registered."""


class StopHotkeyRegistration:
    def __init__(self, hotkey_handle: Any) -> None:
        self._hotkey_handle = hotkey_handle

    def unregister(self) -> None:
        try:
            import keyboard
        except ImportError as error:
            raise StopHotkeyError(
                "Stop hotkey cleanup requires the optional 'keyboard' package."
            ) from error

        keyboard.remove_hotkey(self._hotkey_handle)


def register_stop_hotkey(
    key_name: str,
    on_stop_requested: Callable[[], None],
) -> StopHotkeyRegistration:
    try:
        import keyboard
    except ImportError as error:
        raise StopHotkeyError(
            "Stop hotkey requires the optional 'keyboard' package."
        ) from error

    hotkey_handle = keyboard.add_hotkey(key_name, on_stop_requested)
    return StopHotkeyRegistration(hotkey_handle)
