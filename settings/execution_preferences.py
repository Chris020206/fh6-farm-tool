import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExecutionPreferences:
    show_auto2_purchase_confirmation: bool = True
    show_auto3_unlock_confirmation: bool = True


class ExecutionPreferencesError(RuntimeError):
    """Raised when execution preferences cannot be persisted."""


class ExecutionPreferencesStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_execution_preferences_path()

    def load(self) -> ExecutionPreferences:
        if not self.path.exists():
            return ExecutionPreferences()

        try:
            with self.path.open("r", encoding="utf-8") as preferences_file:
                data = json.load(preferences_file)
        except (OSError, json.JSONDecodeError):
            return ExecutionPreferences()

        if not isinstance(data, dict):
            return ExecutionPreferences()

        execution = data.get("execution")
        if not isinstance(execution, dict):
            return ExecutionPreferences()

        defaults = ExecutionPreferences()
        return ExecutionPreferences(
            show_auto2_purchase_confirmation=_boolean_or_default(
                execution.get("show_auto2_purchase_confirmation"),
                defaults.show_auto2_purchase_confirmation,
            ),
            show_auto3_unlock_confirmation=_boolean_or_default(
                execution.get("show_auto3_unlock_confirmation"),
                defaults.show_auto3_unlock_confirmation,
            ),
        )

    def save(self, preferences: ExecutionPreferences) -> None:
        payload = {"execution": asdict(preferences)}
        temporary_path = self.path.with_suffix(f"{self.path.suffix}.tmp")

        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with temporary_path.open("w", encoding="utf-8") as preferences_file:
                json.dump(payload, preferences_file, indent=2)
                preferences_file.write("\n")
            temporary_path.replace(self.path)
        except OSError as error:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
            raise ExecutionPreferencesError(
                f"Execution preferences could not be saved: {self.path}"
            ) from error


def default_execution_preferences_path() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "Forza Automation Assist" / "settings.json"
    return Path.home() / ".forza_automation_assist" / "settings.json"


def _boolean_or_default(value: object, default: bool) -> bool:
    return value if isinstance(value, bool) else default
