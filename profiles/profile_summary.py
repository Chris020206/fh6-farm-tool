import argparse
from typing import Any

from app.commands import print_command_title, print_error
from app_logging.log_manager import configure_logging
from profiles import ProfileLoadError, ProfileManager


DISPLAY_FIELDS = [
    "profile_id",
    "profile_name",
    "profile_type",
    "profile_version",
    "is_official",
    "description",
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only summary of official Forza Automation Assist profiles. Example: "
            "python -B -m profiles.profile_summary --type auto2_buy_car"
        )
    )
    parser.add_argument(
        "--type",
        dest="profile_type",
        help="Only show official profiles matching this profile_type.",
    )
    args = parser.parse_args()

    configure_logging()
    profile_manager = ProfileManager()

    try:
        profiles = profile_manager.load_official_profiles()
    except ProfileLoadError as error:
        print_error(f"Profile summary failed: {error}")
        return 1

    if args.profile_type:
        profiles = [
            profile_data
            for profile_data in profiles
            if profile_data.get("profile_type") == args.profile_type
        ]

    if not profiles:
        if args.profile_type:
            print_command_title("Profile Summary")
            print(f"No official profiles found for type: {args.profile_type}")
        else:
            print_command_title("Profile Summary")
            print("No official profiles found.")
        return 0

    print_command_title("Profile Summary")
    if args.profile_type:
        print(f"Filter: {args.profile_type}")
        print()

    for index, profile_data in enumerate(profiles):
        if index > 0:
            print()

        _print_profile(profile_data)

    return 0


def _print_profile(profile_data: dict[str, Any]) -> None:
    for field_name in DISPLAY_FIELDS:
        print(f"{field_name}: {profile_data.get(field_name)}")

    _print_section("keys", profile_data.get("keys"))
    _print_section("timings", profile_data.get("timings"))
    _print_section("navigation_counts", profile_data.get("navigation_counts"))

    if "estimated_cost_per_car" in profile_data:
        print(f"estimated_cost_per_car: {profile_data['estimated_cost_per_car']}")


def _print_section(section_name: str, section_data: Any) -> None:
    if not isinstance(section_data, dict):
        return

    print(f"{section_name}:")
    for key, value in section_data.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    raise SystemExit(main())
