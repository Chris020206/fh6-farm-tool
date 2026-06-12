import argparse
from datetime import datetime
from pathlib import Path
from shutil import copy2

from app.commands import print_error, print_info_summary, print_refusal


PROFILE_FOLDERS = ["official", "custom"]


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Guarded restore of official and custom profile backups. Example: "
            "python -B -m profiles.profile_restore 20260611_045210 --confirm-restore"
        )
    )
    parser.add_argument(
        "backup_timestamp",
        help="Timestamp folder under backups/profiles/ to restore from.",
    )
    parser.add_argument(
        "--confirm-restore",
        action="store_true",
        help="Required. Confirms that current profiles may be overwritten.",
    )
    args = parser.parse_args()

    if not args.confirm_restore:
        print_refusal("Missing required confirmation flag: --confirm-restore.")
        return 1

    project_root = Path(__file__).resolve().parents[1]
    profiles_root = project_root / "profiles"
    backups_root = project_root / "backups" / "profiles"
    restore_source = backups_root / args.backup_timestamp

    try:
        _validate_restore_source(restore_source)
        safety_backup_path = _create_safety_backup(
            profiles_root=profiles_root,
            backups_root=backups_root,
        )
        files_restored = _restore_profile_folders(
            restore_source=restore_source,
            profiles_root=profiles_root,
        )
    except ProfileRestoreError as error:
        print_error(f"Profile restore failed: {error}")
        return 1

    print_info_summary(
        "FH6 Farm Tool - Profile Restore",
        [
            ("Backup restored", restore_source),
            ("Safety backup location", safety_backup_path),
            ("Files restored", files_restored),
        ],
    )
    return 0


def _validate_restore_source(restore_source: Path) -> None:
    if not restore_source.exists():
        raise ProfileRestoreError(f"Backup folder is missing: {restore_source}")

    if not restore_source.is_dir():
        raise ProfileRestoreError(f"Backup path is not a folder: {restore_source}")

    for folder_name in PROFILE_FOLDERS:
        source_folder = restore_source / folder_name

        if not source_folder.exists():
            raise ProfileRestoreError(
                f"Backup is missing expected folder: {source_folder}"
            )

        if not source_folder.is_dir():
            raise ProfileRestoreError(
                f"Backup expected path is not a folder: {source_folder}"
            )


def _create_safety_backup(profiles_root: Path, backups_root: Path) -> Path:
    timestamp = datetime.now().strftime("safety_%Y%m%d_%H%M%S")
    safety_backup_path = backups_root / timestamp
    _copy_profile_folders(
        source_root=profiles_root,
        destination_root=safety_backup_path,
    )
    return safety_backup_path


def _restore_profile_folders(restore_source: Path, profiles_root: Path) -> int:
    return _copy_profile_folders(
        source_root=restore_source,
        destination_root=profiles_root,
    )


def _copy_profile_folders(source_root: Path, destination_root: Path) -> int:
    files_copied = 0

    for folder_name in PROFILE_FOLDERS:
        source_folder = source_root / folder_name
        destination_folder = destination_root / folder_name

        if not source_folder.exists() or not source_folder.is_dir():
            raise ProfileRestoreError(f"Source folder is missing: {source_folder}")

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


class ProfileRestoreError(Exception):
    """Raised when profile restore cannot be completed safely."""


if __name__ == "__main__":
    raise SystemExit(main())
