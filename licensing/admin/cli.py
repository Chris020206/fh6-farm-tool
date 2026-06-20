"""CLI-first manual FAA license administration."""

import argparse
from datetime import datetime
import os
from pathlib import Path
import sys

from licensing.admin.authority import LicenseAdminError, ManualLicensingAuthority
from licensing.admin.repository import LicenseAdminRepository, LicenseRepositoryError
from licensing.admin.signing import LicenseSigner
from licensing.constants import DEFAULT_SIGNING_KEY_ID


AUTHORITY_DIRECTORY = Path.home() / ".faa-licensing" / "development"
DEFAULT_DATABASE_PATH = AUTHORITY_DIRECTORY / "licensing.db"
DEFAULT_PRIVATE_KEY_PATH = (
    AUTHORITY_DIRECTORY / "FAA_KEY_DEV_2026_01_private.pem"
)
DEFAULT_ISSUED_DIRECTORY = AUTHORITY_DIRECTORY / "issued"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="license-admin",
        description="Manual Forza Automation Assist license administration.",
    )
    parser.add_argument(
        "--database",
        default=os.environ.get("FAA_LICENSE_DB_PATH", str(DEFAULT_DATABASE_PATH)),
        help="SQLite licensing records path.",
    )
    parser.add_argument(
        "--private-key",
        default=os.environ.get(
            "FAA_LICENSE_PRIVATE_KEY_PATH",
            str(DEFAULT_PRIVATE_KEY_PATH),
        ),
        help="External Ed25519 private key path for issue/replace commands.",
    )
    parser.add_argument(
        "--signing-key-id",
        default=os.environ.get("FAA_LICENSE_SIGNING_KEY_ID", DEFAULT_SIGNING_KEY_ID),
        help="Bundled desktop verification key ID.",
    )

    commands = parser.add_subparsers(dest="command", required=True)
    issue = commands.add_parser("issue", help="Issue a first active license.")
    _add_issuance_arguments(issue)

    lookup = commands.add_parser("lookup", help="Lookup customer license history.")
    _add_discord_id(lookup)

    export = commands.add_parser("export", help="Export/resend the active license.")
    _add_discord_id(export)
    export.add_argument("--out", required=True, help="Destination .lic file path.")

    replace = commands.add_parser("replace", help="Replace with a higher edition.")
    _add_issuance_arguments(replace)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repository = LicenseAdminRepository(args.database)
    try:
        repository.initialize()
        if args.command == "lookup":
            return _run_lookup(repository, args.discord_id)
        if args.command == "export":
            authority = ManualLicensingAuthority(repository)
            output_path = authority.export_active(args.discord_id, args.out)
            print(f"Active license exported: {output_path}")
            return 0

        signer = LicenseSigner(
            private_key_path=args.private_key,
            signing_key_id=args.signing_key_id,
        )
        authority = ManualLicensingAuthority(repository, signer=signer)
        expires_at = _parse_optional_timestamp(args.expires_at)
        if args.command == "issue":
            issued = authority.issue(args.discord_id, args.edition, expires_at)
        else:
            issued = authority.replace(args.discord_id, args.edition, expires_at)

        output_path = Path(args.out) if args.out else (
            DEFAULT_ISSUED_DIRECTORY / f"{issued.signed_license.payload.license_id}.lic"
        )
        authority.export_active(args.discord_id, output_path)
        print(f"License ID: {issued.signed_license.payload.license_id}")
        print(f"Edition: {issued.signed_license.payload.edition}")
        print(f"License file: {output_path}")
        print(f"License key: {issued.paste_key}")
        return 0
    except (LicenseAdminError, LicenseRepositoryError, ValueError) as error:
        print(f"License administration failed: {error}", file=sys.stderr)
        return 1


def _run_lookup(repository: LicenseAdminRepository, discord_user_id: str) -> int:
    lookup = ManualLicensingAuthority(repository).lookup(discord_user_id)
    print(f"Discord user ID: {lookup.customer.discord_user_id}")
    print(f"First seen: {lookup.customer.first_seen_at}")
    if lookup.active_license is None:
        print("Active license: none")
    else:
        print(f"Active license: {lookup.active_license.license_id}")
        print(f"Edition: {lookup.active_license.edition}")
    print("License history:")
    for license_record in lookup.license_history:
        print(
            f"- {license_record.license_id} | {license_record.edition} | "
            f"{license_record.status} | {license_record.issued_at}"
        )
    print(f"Recorded events: {len(lookup.events)}")
    return 0


def _add_discord_id(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--discord-id", required=True, help="Discord numeric user ID.")


def _add_issuance_arguments(parser: argparse.ArgumentParser) -> None:
    _add_discord_id(parser)
    parser.add_argument(
        "--edition",
        required=True,
        choices=("basic", "plus", "founding"),
    )
    parser.add_argument(
        "--expires-at",
        help="Optional timezone-aware ISO-8601 expiration. Founding cannot expire.",
    )
    parser.add_argument("--out", help="Optional destination .lic file path.")


def _parse_optional_timestamp(value: str | None) -> datetime | None:
    if value is None:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("Expiration must be a valid ISO-8601 timestamp.") from error
    if parsed.tzinfo is None:
        raise ValueError("Expiration must include a timezone.")
    return parsed


if __name__ == "__main__":
    raise SystemExit(main())
