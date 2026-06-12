from pathlib import Path
from typing import Any

from profiles import ProfileLoadError, ProfileManager


class ProfileSelectionError(Exception):
    """Raised when a requested automation profile cannot be selected safely."""


def load_profile_for_automation(
    profile_name: str | None,
    expected_profile_type: str,
    default_profile_path: Path,
) -> dict[str, Any]:
    profile_manager = ProfileManager()

    if profile_name is None:
        return _load_and_validate_type(
            profile_manager=profile_manager,
            profile_path=default_profile_path,
            expected_profile_type=expected_profile_type,
        )

    for profile_path in _iter_profile_paths(profile_manager):
        profile_data = _load_profile(profile_manager, profile_path)

        if not _matches_profile(profile_data, profile_path, profile_name):
            continue

        _validate_profile_type(profile_data, expected_profile_type)
        return profile_data

    raise ProfileSelectionError(f"Profile was not found: {profile_name}")


def _load_and_validate_type(
    profile_manager: ProfileManager,
    profile_path: Path,
    expected_profile_type: str,
) -> dict[str, Any]:
    profile_data = _load_profile(profile_manager, profile_path)
    _validate_profile_type(profile_data, expected_profile_type)
    return profile_data


def _iter_profile_paths(profile_manager: ProfileManager):
    yield from sorted(profile_manager.official_profiles_path.glob("*.json"))
    yield from sorted(profile_manager.custom_profiles_path.glob("*.json"))


def _load_profile(profile_manager: ProfileManager, profile_path: Path) -> dict[str, Any]:
    try:
        return profile_manager.load_profile(profile_path)
    except ProfileLoadError as error:
        raise ProfileSelectionError(str(error)) from error


def _matches_profile(
    profile_data: dict[str, Any],
    profile_path: Path,
    requested_profile: str,
) -> bool:
    return requested_profile in {
        profile_data["profile_id"],
        profile_data["profile_name"],
        profile_path.stem,
    }


def _validate_profile_type(
    profile_data: dict[str, Any],
    expected_profile_type: str,
) -> None:
    actual_profile_type = profile_data["profile_type"]

    if actual_profile_type != expected_profile_type:
        raise ProfileSelectionError(
            "Profile type mismatch: "
            f"expected {expected_profile_type}, got {actual_profile_type}."
        )
