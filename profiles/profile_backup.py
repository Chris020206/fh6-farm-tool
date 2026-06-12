import argparse
from datetime import datetime
from pathlib import Path
from shutil import copy2

from app.commands import print_error, print_info_summary


PROFILE_FOLDERS = ["official", "custom"]


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Create a timestamped backup of official and custom profiles. "
            "Example: python -B -m profiles.profile_backup"
        )
    )
    parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    profiles_root = project_root / "profiles"
    backup_root = project_root / "backups" / "profiles"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_root / timestamp

    try:
        _validate_sources(profiles_root)
        files_copied = _copy_profile_folders(
            profiles_root=profiles_root,
            backup_path=backup_path,
        )
    except ProfileBackupError as error:
        print_error(f"Profile backup failed: {error}")
        return 1

    print_info_summary(
        "FH6 Farm Tool - Profile Backup",
        [
            ("Backup location", backup_path),
            ("Files copied", files_copied),
        ],
    )
    return 0


def _validate_sources(profiles_root: Path) -> None:
    for folder_name in PROFILE_FOLDERS:
        source_folder = profiles_root / folder_name

        if not source_folder.exists():
            raise ProfileBackupError(f"Source folder is missing: {source_folder}")

        if not source_folder.is_dir():
            raise ProfileBackupError(f"Source path is not a folder: {source_folder}")


def _copy_profile_folders(profiles_root: Path, backup_path: Path) -> int:
    files_copied = 0

    for folder_name in PROFILE_FOLDERS:
        source_folder = profiles_root / folder_name
        destination_folder = backup_path / folder_name
        destination_folder.mkdir(parents=True, exist_ok=True)

        for source_file in source_folder.rglob("*"):
            if not source_file.is_file():
                continue

            relative_path = source_file.relative_to(source_folder)
            destination_file = destination_folder / relative_path
            destination_file.parent.mkdir(parents=True, exist_ok=True)
            copy2(source_file, destination_file)
            files_copied += 1

    return files_copied


class ProfileBackupError(Exception):
    """Raised when profile backup cannot be completed safely."""


if __name__ == "__main__":
    raise SystemExit(main())
