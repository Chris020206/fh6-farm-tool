import argparse
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from app.commands import print_error, print_info_summary
from profiles import ProfileLoadError, ProfileManager, ProfileValidationError
from profiles.profile_validator import ProfileValidator


SAFE_PROFILE_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Create a custom profile by copying an official profile. Example: "
            "python -B -m profiles.profile_create_custom "
            "--source auto1_race_default --name auto1_safe_slow"
        )
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Official source profile_id to copy.",
    )
    parser.add_argument(
        "--name",
        required=True,
        help="New custom profile name and profile_id.",
    )
    args = parser.parse_args()

    try:
        created_profile_path, profile_data = create_custom_profile(
            source_profile_id=args.source,
            custom_profile_name=args.name,
        )
    except CustomProfileCreationError as error:
        print_error(f"Custom profile creation failed: {error}")
        return 1

    print_info_summary(
        "FH6 Farm Tool - Custom Profile Creation",
        [
            ("Source profile", args.source),
            ("Created profile path", created_profile_path),
            ("Profile type", profile_data["profile_type"]),
        ],
    )
    return 0


def create_custom_profile(
    source_profile_id: str,
    custom_profile_name: str,
) -> tuple[Path, dict[str, Any]]:
    custom_profile_id = _validate_custom_profile_name(custom_profile_name)
    profile_manager = ProfileManager()
    source_profile = _load_source_profile(profile_manager, source_profile_id)
    custom_profile_path = profile_manager.custom_profiles_path / f"{custom_profile_id}.json"

    _validate_custom_profile_does_not_exist(
        profile_manager=profile_manager,
        custom_profile_id=custom_profile_id,
        custom_profile_name=custom_profile_name,
        custom_profile_path=custom_profile_path,
    )

    custom_profile = deepcopy(source_profile)
    custom_profile["profile_id"] = custom_profile_id
    custom_profile["profile_name"] = custom_profile_name
    custom_profile["is_official"] = False
    custom_profile["based_on"] = source_profile_id

    try:
        ProfileValidator().validate(custom_profile)
    except ProfileValidationError as error:
        raise CustomProfileCreationError(
            f"Created custom profile did not validate: {error}"
        ) from error

    profile_manager.custom_profiles_path.mkdir(parents=True, exist_ok=True)
    with custom_profile_path.open("w", encoding="utf-8") as profile_file:
        json.dump(custom_profile, profile_file, indent=2)
        profile_file.write("\n")

    try:
        profile_manager.load_profile(custom_profile_path)
    except ProfileLoadError as error:
        raise CustomProfileCreationError(
            f"Created custom profile could not be loaded: {error}"
        ) from error

    return custom_profile_path, custom_profile


def _validate_custom_profile_name(custom_profile_name: str) -> str:
    custom_profile_id = custom_profile_name.strip()

    if not custom_profile_id:
        raise CustomProfileCreationError("Custom profile name must not be empty.")

    if not SAFE_PROFILE_ID_PATTERN.fullmatch(custom_profile_id):
        raise CustomProfileCreationError(
            "Custom profile name may only contain letters, numbers, underscores, "
            "and hyphens."
        )

    return custom_profile_id


def _load_source_profile(
    profile_manager: ProfileManager,
    source_profile_id: str,
) -> dict[str, Any]:
    try:
        official_profiles = profile_manager.load_official_profiles()
    except ProfileLoadError as error:
        raise CustomProfileCreationError(str(error)) from error

    for profile_data in official_profiles:
        if profile_data["profile_id"] == source_profile_id:
            return profile_data

    raise CustomProfileCreationError(
        f"Official source profile was not found: {source_profile_id}"
    )


def _validate_custom_profile_does_not_exist(
    profile_manager: ProfileManager,
    custom_profile_id: str,
    custom_profile_name: str,
    custom_profile_path: Path,
) -> None:
    if custom_profile_path.exists():
        raise CustomProfileCreationError(
            f"Custom profile file already exists: {custom_profile_path}"
        )

    try:
        custom_profiles = profile_manager.load_custom_profiles()
    except ProfileLoadError as error:
        raise CustomProfileCreationError(str(error)) from error

    for profile_data in custom_profiles:
        if profile_data["profile_id"] == custom_profile_id:
            raise CustomProfileCreationError(
                f"Custom profile_id already exists: {custom_profile_id}"
            )

        if profile_data["profile_name"] == custom_profile_name:
            raise CustomProfileCreationError(
                f"Custom profile_name already exists: {custom_profile_name}"
            )


class CustomProfileCreationError(Exception):
    """Raised when a custom profile cannot be created safely."""


if __name__ == "__main__":
    raise SystemExit(main())
