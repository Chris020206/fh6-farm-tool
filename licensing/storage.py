"""Atomic local storage for the active license and Community usage state."""

import json
import os
from pathlib import Path
import threading


APP_DATA_DIRECTORY_NAME = "ForzaAutomationAssist"
LICENSE_FILE_NAME = "license.lic"
USAGE_FILE_NAME = "community_usage.json"
_USAGE_LOCK = threading.Lock()


class LicenseStorageError(OSError):
    """Raised when local licensing state cannot be read or written safely."""


def default_app_data_directory() -> Path:
    app_data = os.environ.get("APPDATA")
    if app_data:
        return Path(app_data) / APP_DATA_DIRECTORY_NAME
    return Path.home() / "AppData" / "Roaming" / APP_DATA_DIRECTORY_NAME


class LicenseStorage:
    def __init__(self, directory: Path | None = None) -> None:
        self.directory = Path(directory) if directory is not None else default_app_data_directory()
        self.license_path = self.directory / LICENSE_FILE_NAME

    def read(self) -> str | None:
        if not self.license_path.exists():
            return None
        try:
            return self.license_path.read_text(encoding="utf-8")
        except OSError as error:
            raise LicenseStorageError("Stored license could not be read.") from error

    def write(self, serialized_license: str) -> None:
        _atomic_write_text(self.license_path, serialized_license)


class CommunityUsageStore:
    def __init__(self, directory: Path | None = None) -> None:
        self.directory = Path(directory) if directory is not None else default_app_data_directory()
        self.usage_path = self.directory / USAGE_FILE_NAME

    def execution_count(self) -> int:
        with _USAGE_LOCK:
            return self._read_count()

    def consume_auto1_execution(self, maximum: int) -> tuple[bool, int]:
        with _USAGE_LOCK:
            current = self._read_count()
            if current >= maximum:
                return False, current
            updated = current + 1
            _atomic_write_text(
                self.usage_path,
                json.dumps({"version": 1, "auto1_executions": updated}, indent=2) + "\n",
            )
            return True, updated

    def _read_count(self) -> int:
        if not self.usage_path.exists():
            return 0
        try:
            data = json.loads(self.usage_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise LicenseStorageError("Community usage state is unavailable or malformed.") from error
        count = data.get("auto1_executions") if isinstance(data, dict) else None
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise LicenseStorageError("Community usage state is unavailable or malformed.")
        return count


def _atomic_write_text(path: Path, content: str) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = path.with_suffix(path.suffix + ".tmp")
        temporary_path.write_text(content, encoding="utf-8")
        temporary_path.replace(path)
    except OSError as error:
        raise LicenseStorageError(f"Licensing state could not be stored at {path}.") from error
