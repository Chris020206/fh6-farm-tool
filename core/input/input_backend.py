from typing import Protocol


class InputBackend(Protocol):
    def press_key(self, key_name: str) -> None:
        pass

    def hold_key(self, key_name: str) -> None:
        pass

    def release_key(self, key_name: str) -> None:
        pass


class InMemoryInputBackend:
    def __init__(self) -> None:
        self.pressed_keys: list[str] = []
        self.held_keys: set[str] = set()
        self.released_keys: list[str] = []

    def press_key(self, key_name: str) -> None:
        self.pressed_keys.append(key_name)

    def hold_key(self, key_name: str) -> None:
        self.held_keys.add(key_name)

    def release_key(self, key_name: str) -> None:
        self.held_keys.discard(key_name)
        self.released_keys.append(key_name)
