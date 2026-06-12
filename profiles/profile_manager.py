import json
from pathlib import Path
from typing import Any

from app_logging.log_manager import get_logger
from profiles.profile_validator import ProfileValidationError, ProfileValidator


class ProfileLoadError(Exception):
    """Raised when a profile cannot be loaded safely."""


class ProfileManager:
    def __init__(
        self,
        profiles_root: Path | None = None,
        validator: ProfileValidator | None = None,
    ) -> None:
        self._profiles_root = profiles_root or Path(__file__).resolve().parent
        self._validator = validator or ProfileValidator()
        self._logger = get_logger()

    def load_profile(self, profile_path: Path) -> dict[str, Any]:
        self._logger.info("Loading profile: %s", profile_path, category="profile")

        try:
            with profile_path.open("r", encoding="utf-8") as profile_file:
                profile_data = json.load(profile_file)
        except FileNotFoundError as error:
            message = f"Profile file is missing: {profile_path}"
            self._logger.error(message, category="profile")
            raise ProfileLoadError(message) from error
        except json.JSONDecodeError as error:
            message = (
                f"Profile file is invalid JSON: {profile_path} "
                f"(line {error.lineno}, column {error.colno})"
            )
            self._logger.error(message, category="profile")
            raise ProfileLoadError(message) from error
        except OSError as error:
            message = f"Profile file could not be read: {profile_path}"
            self._logger.error(message, category="profile")
            raise ProfileLoadError(message) from error

        if not isinstance(profile_data, dict):
            message = f"Profile root must be a JSON object: {profile_path}"
            self._logger.error(message, category="profile")
            raise ProfileLoadError(message)

        try:
            self._validator.validate(profile_data)
        except ProfileValidationError as error:
            message = f"Profile validation failed for {profile_path}: {error}"
            self._logger.error(message, category="profile")
            raise ProfileLoadError(message) from error

        self._logger.info(
            "Profile loaded successfully: %s",
            profile_data["profile_id"],
            category="profile",
        )
        return profile_data

    def load_official_profiles(self) -> list[dict[str, Any]]:
        return self._load_profiles_from_folder(self.official_profiles_path)

    def load_custom_profiles(self) -> list[dict[str, Any]]:
        return self._load_profiles_from_folder(self.custom_profiles_path)

    @property
    def official_profiles_path(self) -> Path:
        return self._profiles_root / "official"

    @property
    def custom_profiles_path(self) -> Path:
        return self._profiles_root / "custom"

    def _load_profiles_from_folder(self, folder_path: Path) -> list[dict[str, Any]]:
        profiles: list[dict[str, Any]] = []

        for profile_path in sorted(folder_path.glob("*.json")):
            profiles.append(self.load_profile(profile_path))

        return profiles
