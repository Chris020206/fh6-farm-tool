from app_logging.log_manager import get_logger
from core.input.input_backend import InMemoryInputBackend, InputBackend
from core.input.input_result import InputResult


class InputController:
    def __init__(self, backend: InputBackend | None = None) -> None:
        self._backend = backend or InMemoryInputBackend()
        self._held_keys: set[str] = set()
        self._logger = get_logger()

    @property
    def held_keys(self) -> frozenset[str]:
        return frozenset(self._held_keys)

    def press_key(self, key_name: str) -> InputResult:
        normalized_key_name = self._normalize_key_name(key_name)
        self._backend.press_key(normalized_key_name)
        self._logger.info(
            "Input action requested: press_key(%s)",
            normalized_key_name,
            category="input",
        )

        return InputResult(
            action_name="press_key",
            key_name=normalized_key_name,
            changed=True,
            message=f"Pressed key: {normalized_key_name}",
        )

    def hold_key(self, key_name: str) -> InputResult:
        normalized_key_name = self._normalize_key_name(key_name)

        if normalized_key_name in self._held_keys:
            return InputResult(
                action_name="hold_key",
                key_name=normalized_key_name,
                changed=False,
                message=f"Key already held: {normalized_key_name}",
            )

        self._backend.hold_key(normalized_key_name)
        self._held_keys.add(normalized_key_name)
        self._logger.info(
            "Input action requested: hold_key(%s)",
            normalized_key_name,
            category="input",
        )

        return InputResult(
            action_name="hold_key",
            key_name=normalized_key_name,
            changed=True,
            message=f"Held key: {normalized_key_name}",
        )

    def release_key(self, key_name: str) -> InputResult:
        normalized_key_name = self._normalize_key_name(key_name)

        if normalized_key_name not in self._held_keys:
            return InputResult(
                action_name="release_key",
                key_name=normalized_key_name,
                changed=False,
                message=f"Key was not held: {normalized_key_name}",
            )

        self._backend.release_key(normalized_key_name)
        self._held_keys.remove(normalized_key_name)
        self._logger.info(
            "Input action requested: release_key(%s)",
            normalized_key_name,
            category="input",
        )

        return InputResult(
            action_name="release_key",
            key_name=normalized_key_name,
            changed=True,
            message=f"Released key: {normalized_key_name}",
        )

    def release_all_keys(self) -> InputResult:
        released_key_names = sorted(self._held_keys)

        for key_name in released_key_names:
            self._backend.release_key(key_name)

        self._held_keys.clear()
        self._logger.info("Input action requested: release_all_keys", category="input")

        return InputResult(
            action_name="release_all_keys",
            key_name=None,
            changed=bool(released_key_names),
            message=f"Released {len(released_key_names)} held key(s).",
        )

    def _normalize_key_name(self, key_name: str) -> str:
        normalized_key_name = key_name.strip().lower()

        if not normalized_key_name:
            raise ValueError("Key name must not be empty.")

        return normalized_key_name
