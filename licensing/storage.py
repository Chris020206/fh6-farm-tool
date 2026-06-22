"""Atomic local storage for the active offline license."""

import os
from pathlib import Path


APP_DATA_DIRECTORY_NAME = "ForzaAutomationAssist"
LICENSE_FILE_NAME = "license.lic"


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

    def remove(self) -> bool:
        if not self.license_path.exists():
            return False
        try:
            self.license_path.unlink()
        except OSError as error:
            raise LicenseStorageError("Stored license could not be removed.") from error
        return True


def _atomic_write_text(path: Path, content: str) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = path.with_suffix(path.suffix + ".tmp")
        temporary_path.write_text(content, encoding="utf-8")
        temporary_path.replace(path)
    except OSError as error:
        raise LicenseStorageError(f"Licensing state could not be stored at {path}.") from error
