"""Manual Licensing Authority operations for Milestone 2."""

import base64
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Callable
import uuid

from licensing.admin.editions import get_issuable_edition
from licensing.admin.repository import (
    AdminLicenseRecord,
    CustomerRecord,
    LicenseAdminRepository,
    LicenseEventRecord,
    LicenseRepositoryError,
)
from licensing.admin.signing import LicenseSigner
from licensing.constants import EDITION_RANKS, PRODUCT_ID, SUPPORTED_LICENSE_VERSION
from licensing.models import SignedLicense
from licensing.parsing import encode_license_key, parse_signed_license_json


class LicenseAdminError(RuntimeError):
    """Raised when a requested manual administration operation is refused."""


@dataclass(frozen=True)
class IssuedLicense:
    signed_license: SignedLicense
    paste_key: str


@dataclass(frozen=True)
class CustomerLicenseLookup:
    customer: CustomerRecord
    active_license: AdminLicenseRecord | None
    license_history: tuple[AdminLicenseRecord, ...]
    events: tuple[LicenseEventRecord, ...]


class ManualLicensingAuthority:
    def __init__(
        self,
        repository: LicenseAdminRepository,
        signer: LicenseSigner | None = None,
        now: Callable[[], datetime] | None = None,
        license_id_factory: Callable[[datetime], str] | None = None,
    ) -> None:
        self.repository = repository
        self.signer = signer
        self._now = now or (lambda: datetime.now(timezone.utc))
        self._license_id_factory = license_id_factory or _default_license_id

    def issue(
        self,
        discord_user_id: str,
        edition: str,
        expires_at: datetime | None = None,
    ) -> IssuedLicense:
        discord_user_id = _validate_discord_user_id(discord_user_id)
        definition = get_issuable_edition(edition)
        issued_at = _normalized_now(self._now())
        expires_at = _validate_expiration(definition.edition, issued_at, expires_at)
        if self.repository.get_active_license(discord_user_id) is not None:
            raise LicenseAdminError(
                "Customer already has an active license. Use replace or export."
            )

        license_id = self._license_id_factory(issued_at)
        signed_license = self._sign(
            _build_payload(
                license_id=license_id,
                discord_user_id=discord_user_id,
                edition=definition.edition,
                features=definition.features,
                limits=dict(definition.limits),
                issued_at=issued_at,
                expires_at=expires_at,
                replaces_license_id=None,
                metadata=dict(definition.metadata),
            )
        )
        record = _record_from_signed_license(signed_license)
        try:
            self.repository.record_issue(record, _format_timestamp(issued_at))
        except LicenseRepositoryError as error:
            raise LicenseAdminError(str(error)) from error
        return IssuedLicense(signed_license, encode_license_key(signed_license))

    def replace(
        self,
        discord_user_id: str,
        edition: str,
        expires_at: datetime | None = None,
    ) -> IssuedLicense:
        discord_user_id = _validate_discord_user_id(discord_user_id)
        current = self.repository.get_active_license(discord_user_id)
        if current is None:
            raise LicenseAdminError("Customer has no active license to replace.")
        definition = get_issuable_edition(edition)
        if EDITION_RANKS[definition.edition] <= EDITION_RANKS[current.edition]:
            raise LicenseAdminError("Replacement edition must be an upgrade.")

        issued_at = _normalized_now(self._now())
        expires_at = _validate_expiration(definition.edition, issued_at, expires_at)
        signed_license = self._sign(
            _build_payload(
                license_id=self._license_id_factory(issued_at),
                discord_user_id=discord_user_id,
                edition=definition.edition,
                features=definition.features,
                limits=dict(definition.limits),
                issued_at=issued_at,
                expires_at=expires_at,
                replaces_license_id=current.license_id,
                metadata=dict(definition.metadata),
            )
        )
        record = _record_from_signed_license(signed_license)
        try:
            self.repository.record_replacement(
                current.license_id,
                record,
                _format_timestamp(issued_at),
            )
        except LicenseRepositoryError as error:
            raise LicenseAdminError(str(error)) from error
        return IssuedLicense(signed_license, encode_license_key(signed_license))

    def lookup(self, discord_user_id: str) -> CustomerLicenseLookup:
        discord_user_id = _validate_discord_user_id(discord_user_id)
        customer = self.repository.get_customer(discord_user_id)
        if customer is None:
            raise LicenseAdminError("Customer was not found.")
        return CustomerLicenseLookup(
            customer=customer,
            active_license=self.repository.get_active_license(discord_user_id),
            license_history=self.repository.list_licenses(discord_user_id),
            events=self.repository.list_events(discord_user_id),
        )

    def export_active(
        self,
        discord_user_id: str,
        output_path: str | Path,
    ) -> Path:
        discord_user_id = _validate_discord_user_id(discord_user_id)
        active = self.repository.get_active_license(discord_user_id)
        if active is None:
            raise LicenseAdminError("Customer has no active license to export.")
        signed_license = _signed_license_from_record(active)
        destination = Path(output_path)
        try:
            _atomic_write_text(destination, signed_license.serialized_json)
            self.repository.record_export(
                active.license_id,
                discord_user_id,
                _format_timestamp(_normalized_now(self._now())),
                str(destination),
            )
        except (OSError, LicenseRepositoryError) as error:
            raise LicenseAdminError(f"Active license could not be exported: {error}") from error
        return destination

    def _sign(self, payload: dict[str, object]) -> SignedLicense:
        if self.signer is None:
            raise LicenseAdminError("A private signing key is required for this operation.")
        try:
            return self.signer.sign_payload(payload)
        except RuntimeError as error:
            raise LicenseAdminError(str(error)) from error


def _build_payload(
    *,
    license_id: str,
    discord_user_id: str,
    edition: str,
    features: tuple[str, ...],
    limits: dict[str, int | None],
    issued_at: datetime,
    expires_at: datetime | None,
    replaces_license_id: str | None,
    metadata: dict[str, object],
) -> dict[str, object]:
    return {
        "license_id": license_id,
        "product": PRODUCT_ID,
        "license_version": SUPPORTED_LICENSE_VERSION,
        "discord_user_id": discord_user_id,
        "edition": edition,
        "features": list(features),
        "limits": limits,
        "issued_at": _format_timestamp(issued_at),
        "expires_at": (
            _format_timestamp(expires_at) if expires_at is not None else None
        ),
        "replaces_license_id": replaces_license_id,
        "metadata": metadata,
    }


def _record_from_signed_license(signed_license: SignedLicense) -> AdminLicenseRecord:
    payload = signed_license.payload
    return AdminLicenseRecord(
        license_id=payload.license_id,
        discord_user_id=payload.discord_user_id,
        edition=payload.edition,
        payload_json=signed_license.signed_payload.decode("utf-8"),
        signature=base64.b64encode(signed_license.signature).decode("ascii"),
        signing_key_id=signed_license.signing_key_id,
        status="active",
        issued_at=_format_timestamp(payload.issued_at),
        expires_at=(
            _format_timestamp(payload.expires_at)
            if payload.expires_at is not None
            else None
        ),
        replaces_license_id=payload.replaces_license_id,
    )


def _signed_license_from_record(record: AdminLicenseRecord) -> SignedLicense:
    document = {
        "payload": json.loads(record.payload_json),
        "signature": record.signature,
        "signing_key_id": record.signing_key_id,
    }
    return parse_signed_license_json(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    )


def _validate_discord_user_id(value: str) -> str:
    normalized = value.strip()
    if not normalized.isdigit():
        raise LicenseAdminError("Discord user ID must contain digits only.")
    return normalized


def _validate_expiration(
    edition: str,
    issued_at: datetime,
    expires_at: datetime | None,
) -> datetime | None:
    if edition == "founding" and expires_at is not None:
        raise LicenseAdminError("Founding Edition must not expire.")
    if expires_at is None:
        return None
    normalized = _normalized_now(expires_at)
    if normalized <= issued_at:
        raise LicenseAdminError("Expiration must be later than issuance time.")
    return normalized


def _normalized_now(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise LicenseAdminError("Licensing timestamps must include a timezone.")
    return value.astimezone(timezone.utc)


def _format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _default_license_id(issued_at: datetime) -> str:
    return f"FAA-{issued_at.year}-{uuid.uuid4().hex[:12].upper()}"


def _atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_text(content, encoding="utf-8")
    temporary_path.replace(path)
