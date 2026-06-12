import argparse
import json
from copy import deepcopy
from math import isfinite
from pathlib import Path
from typing import Any

from app.commands import print_error, print_info_summary
from profiles import ProfileLoadError, ProfileManager, ProfileValidationError
from profiles.profile_validator import ProfileValidator


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Edit one timing value on a custom profile only. Example: "
            "python -B -m profiles.profile_edit_timing "
            "--profile auto1_safe_slow --timing startup_delay --value 7.0"
        )
    )
    parser.add_argument(
        "--profile",
        required=True,
        help="Custom profile_id or profile_name to edit.",
    )
    parser.add_argument(
        "--timing",
        required=True,
        help="Timing key to edit.",
    )
    parser.add_argument(
        "--value",
        required=True,
        help="New non-negative numeric timing value.",
    )
    args = parser.parse_args()

    print("FH6 Farm Tool - Timing Editing")
    print()
    print("Recommendation: create a profile backup before editing timings.")
    print()

    try:
        result = edit_custom_profile_timing(
            profile_name=args.profile,
            timing_key=args.timing,
            raw_value=args.value,
        )
    except ProfileTimingEditError as error:
        print_error(f"Profile timing edit failed: {error}")
        return 1

    print_info_summary(
        "## Run Summary",
        [
            ("Profile", result.profile_name),
            ("Timing key", result.timing_key),
            ("Old value", result.old_value),
            ("New value", result.new_value),
        ],
    )
    return 0


def edit_custom_profile_timing(
    profile_name: str,
    timing_key: str,
    raw_value: str,
) -> "ProfileTimingEditResult":
    new_value = _parse_timing_value(raw_value)
    profile_manager = ProfileManager()
    profile_path, profile_data = _load_editable_custom_profile(
        profile_manager,
        profile_name,
    )

    timings = profile_data.get("timings")
    if not isinstance(timings, dict):
        raise ProfileTimingEditError("Profile does not contain editable timings.")

    if timing_key not in timings:
        raise ProfileTimingEditError(f"Unknown timing key: {timing_key}")

    old_value = timings[timing_key]
    edited_profile = deepcopy(profile_data)
    edited_profile["timings"][timing_key] = new_value

    try:
        ProfileValidator().validate(edited_profile)
    except ProfileValidationError as error:
        raise ProfileTimingEditError(
            f"Edited profile failed validation: {error}"
        ) from error

    with profile_path.open("w", encoding="utf-8") as profile_file:
        json.dump(edited_profile, profile_file, indent=2)
        profile_file.write("\n")

    try:
        profile_manager.load_profile(profile_path)
    except ProfileLoadError as error:
        raise ProfileTimingEditError(
            f"Edited profile could not be loaded: {error}"
        ) from error

    return ProfileTimingEditResult(
        profile_name=edited_profile["profile_name"],
        timing_key=timing_key,
        old_value=old_value,
        new_value=new_value,
    )


def _parse_timing_value(raw_value: str) -> float:
    try:
        timing_value = float(raw_value)
    except ValueError as error:
        raise ProfileTimingEditError(
            f"Timing value must be a number: {raw_value}"
        ) from error

    if not isfinite(timing_value) or timing_value < 0:
        raise ProfileTimingEditError(
            "Timing value must be a finite non-negative number."
        )

    return timing_value


def _load_editable_custom_profile(
    profile_manager: ProfileManager,
    profile_name: str,
) -> tuple[Path, dict[str, Any]]:
    for profile_path in sorted(profile_manager.custom_profiles_path.glob("*.json")):
        try:
            profile_data = profile_manager.load_profile(profile_path)
        except ProfileLoadError as error:
            raise ProfileTimingEditError(str(error)) from error

        if (
            profile_data["profile_id"] == profile_name
            or profile_data["profile_name"] == profile_name
        ):
            if profile_data.get("is_official") is True:
                raise ProfileTimingEditError(
                    "Official profiles cannot be edited."
                )

            return profile_path, profile_data

    for profile_path in sorted(profile_manager.official_profiles_path.glob("*.json")):
        try:
            profile_data = profile_manager.load_profile(profile_path)
        except ProfileLoadError as error:
            raise ProfileTimingEditError(str(error)) from error

        if (
            profile_data["profile_id"] == profile_name
            or profile_data["profile_name"] == profile_name
        ):
            raise ProfileTimingEditError("Official profiles cannot be edited.")

    raise ProfileTimingEditError(f"Custom profile was not found: {profile_name}")


class ProfileTimingEditResult:
    def __init__(
        self,
        profile_name: str,
        timing_key: str,
        old_value: Any,
        new_value: float,
    ) -> None:
        self.profile_name = profile_name
        self.timing_key = timing_key
        self.old_value = old_value
        self.new_value = new_value


class ProfileTimingEditError(Exception):
    """Raised when a custom profile timing cannot be edited safely."""


if __name__ == "__main__":
    raise SystemExit(main())
