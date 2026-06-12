import json
from pathlib import Path
from typing import Any


class ConfigurationError(Exception):
    """Raised when application configuration cannot be loaded safely."""


def default_settings_path() -> Path:
    return Path(__file__).resolve().parent.parent / "config" / "default_settings.json"


def load_default_settings(path: Path | None = None) -> dict[str, Any]:
    settings_path = path or default_settings_path()

    if not settings_path.exists():
        raise ConfigurationError(
            f"Configuration file is missing: {settings_path}"
        )

    try:
        with settings_path.open("r", encoding="utf-8") as settings_file:
            settings = json.load(settings_file)
    except json.JSONDecodeError as error:
        raise ConfigurationError(
            f"Configuration file is invalid JSON: {settings_path} "
            f"(line {error.lineno}, column {error.colno})"
        ) from error
    except OSError as error:
        raise ConfigurationError(
            f"Configuration file could not be read: {settings_path}"
        ) from error

    if not isinstance(settings, dict):
        raise ConfigurationError(
            f"Configuration root must be a JSON object: {settings_path}"
        )

    return settings
