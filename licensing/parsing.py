"""Strict parsing for signed JSON licenses and pasteable license keys."""

import base64
from datetime import datetime, timezone
import json
from typing import Mapping

from licensing.constants import DEFAULT_SIGNING_KEY_ID
from licensing.models import LicensePayload, SignedLicense


class LicenseParseError(ValueError):
    """Raised when license input is malformed or structurally unsupported."""


def canonical_payload_bytes(payload: Mapping[str, object]) -> bytes:
    return json.dumps(
        payload,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def parse_signed_license_json(raw_text: str) -> SignedLicense:
    try:
        document = _load_json(raw_text)
    except (TypeError, json.JSONDecodeError) as error:
        raise LicenseParseError("License file is not valid JSON.") from error

    if not isinstance(document, dict):
        raise LicenseParseError("License document must be a JSON object.")

    payload_data = _require_mapping(document, "payload")
    signature = _decode_base64(_require_string(document, "signature"), "signature")
    signing_key_id = _require_string(document, "signing_key_id")
    payload = _parse_payload(payload_data)
    normalized_document = {
        "payload": dict(payload_data),
        "signature": base64.b64encode(signature).decode("ascii"),
        "signing_key_id": signing_key_id,
    }

    return SignedLicense(
        payload=payload,
        signature=signature,
        signing_key_id=signing_key_id,
        signed_payload=canonical_payload_bytes(payload_data),
        serialized_json=json.dumps(normalized_document, indent=2, ensure_ascii=False) + "\n",
    )


def parse_license_key(raw_key: str) -> SignedLicense:
    parts = raw_key.strip().split(".")
    if parts[0] != "FAA-LIC-v1" or len(parts) not in (3, 4):
        raise LicenseParseError("License key format is not supported.")

    if len(parts) == 4:
        signing_key_id = _decode_key_id(parts[1])
        payload_part, signature_part = parts[2], parts[3]
    else:
        # Legacy Milestone 1 keys did not carry a key ID. They remain tied to
        # the default bundled key and cannot participate in key rotation.
        signing_key_id = DEFAULT_SIGNING_KEY_ID
        payload_part, signature_part = parts[1], parts[2]

    payload_bytes = _decode_base64url(payload_part, "payload")
    signature = _decode_base64url(signature_part, "signature")
    try:
        payload_data = _load_json(payload_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise LicenseParseError("License key payload is not valid JSON.") from error

    if not isinstance(payload_data, dict):
        raise LicenseParseError("License key payload must be a JSON object.")

    canonical_payload = canonical_payload_bytes(payload_data)
    payload = _parse_payload(payload_data)
    normalized_document = {
        "payload": payload_data,
        "signature": base64.b64encode(signature).decode("ascii"),
        "signing_key_id": signing_key_id,
    }
    return SignedLicense(
        payload=payload,
        signature=signature,
        signing_key_id=signing_key_id,
        signed_payload=canonical_payload,
        serialized_json=json.dumps(normalized_document, indent=2, ensure_ascii=False) + "\n",
    )


def _parse_payload(data: Mapping[str, object]) -> LicensePayload:
    license_version = _require_int(data, "license_version")
    features_data = data.get("features")
    if not isinstance(features_data, list) or not all(
        isinstance(feature, str) and feature.strip() for feature in features_data
    ):
        raise LicenseParseError("License features must be a list of non-empty strings.")
    if len(features_data) != len(set(features_data)):
        raise LicenseParseError("License features must not contain duplicates.")

    limits_data = _require_mapping(data, "limits")
    limits: dict[str, int | None] = {}
    for name, value in limits_data.items():
        if not isinstance(name, str) or not name:
            raise LicenseParseError("License limit names must be non-empty strings.")
        if value is not None and (isinstance(value, bool) or not isinstance(value, int) or value < 0):
            raise LicenseParseError("License limits must be non-negative integers or null.")
        limits[name] = value

    metadata = data.get("metadata", {})
    if not isinstance(metadata, dict):
        raise LicenseParseError("License metadata must be a JSON object.")

    expires_raw = data.get("expires_at")
    expires_at = None if expires_raw is None else _parse_timestamp(expires_raw, "expires_at")
    replaces = data.get("replaces_license_id")
    if replaces is not None and (not isinstance(replaces, str) or not replaces.strip()):
        raise LicenseParseError("Replacement license ID must be a non-empty string or null.")

    return LicensePayload(
        license_id=_require_string(data, "license_id"),
        product=_require_string(data, "product"),
        license_version=license_version,
        discord_user_id=_require_string(data, "discord_user_id"),
        edition=_require_string(data, "edition"),
        features=frozenset(features_data),
        limits=limits,
        issued_at=_parse_timestamp(data.get("issued_at"), "issued_at"),
        expires_at=expires_at,
        replaces_license_id=replaces,
        metadata=metadata,
    )


def _parse_timestamp(value: object, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise LicenseParseError(f"License {field_name} must be an ISO-8601 timestamp.")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise LicenseParseError(f"License {field_name} must be an ISO-8601 timestamp.") from error
    if parsed.tzinfo is None:
        raise LicenseParseError(f"License {field_name} must include a timezone.")
    return parsed.astimezone(timezone.utc)


def _require_mapping(data: Mapping[str, object], field_name: str) -> Mapping[str, object]:
    value = data.get(field_name)
    if not isinstance(value, dict):
        raise LicenseParseError(f"License {field_name} must be a JSON object.")
    return value


def _require_string(data: Mapping[str, object], field_name: str) -> str:
    value = data.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise LicenseParseError(f"License {field_name} must be a non-empty string.")
    return value


def _require_int(data: Mapping[str, object], field_name: str) -> int:
    value = data.get(field_name)
    if isinstance(value, bool) or not isinstance(value, int):
        raise LicenseParseError(f"License {field_name} must be an integer.")
    return value


def _decode_base64(value: str, field_name: str) -> bytes:
    try:
        return base64.b64decode(value, validate=True)
    except (ValueError, base64.binascii.Error) as error:
        raise LicenseParseError(f"License {field_name} is not valid base64.") from error


def _decode_base64url(value: str, field_name: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    try:
        return base64.b64decode(value + padding, altchars=b"-_", validate=True)
    except (ValueError, base64.binascii.Error) as error:
        raise LicenseParseError(f"License key {field_name} is not valid base64url.") from error


def _decode_key_id(value: str) -> str:
    try:
        decoded = _decode_base64url(value, "signing key ID").decode("utf-8")
    except UnicodeDecodeError as error:
        raise LicenseParseError("License key signing key ID is not valid UTF-8.") from error
    if not decoded.strip():
        raise LicenseParseError("License key signing key ID must not be empty.")
    return decoded


def _load_json(raw_text: str) -> object:
    def reject_non_finite(value: str) -> object:
        raise LicenseParseError(f"Non-finite JSON number is not supported: {value}.")

    return json.loads(raw_text, parse_constant=reject_non_finite)
