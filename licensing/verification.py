"""Offline Ed25519 verification and license validity checks."""

import base64
from datetime import datetime, timezone
from typing import Callable, Mapping

from licensing.constants import PRODUCT_ID, SUPPORTED_EDITIONS, SUPPORTED_LICENSE_VERSION
from licensing.models import SignedLicense
from licensing.public_keys import BUNDLED_PUBLIC_KEYS_BASE64


class LicenseVerificationError(ValueError):
    """Raised when a signed license cannot be trusted or used."""


class LicenseVerifier:
    def __init__(
        self,
        public_keys: Mapping[str, bytes] | None = None,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self._public_keys = dict(public_keys or load_bundled_public_keys())
        self._now = now or (lambda: datetime.now(timezone.utc))

    def verify(self, signed_license: SignedLicense) -> None:
        public_key_bytes = self._public_keys.get(signed_license.signing_key_id)
        if public_key_bytes is None:
            raise LicenseVerificationError("License signing key is not supported.")

        try:
            from cryptography.exceptions import InvalidSignature
            from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        except ImportError as error:
            raise LicenseVerificationError(
                "Offline license verification dependency is unavailable."
            ) from error

        try:
            Ed25519PublicKey.from_public_bytes(public_key_bytes).verify(
                signed_license.signature,
                signed_license.signed_payload,
            )
        except (InvalidSignature, ValueError) as error:
            raise LicenseVerificationError("License signature is invalid.") from error

        payload = signed_license.payload
        if payload.product != PRODUCT_ID:
            raise LicenseVerificationError("License is for a different product.")
        if payload.license_version != SUPPORTED_LICENSE_VERSION:
            raise LicenseVerificationError("License format version is not supported.")
        if payload.edition not in SUPPORTED_EDITIONS:
            raise LicenseVerificationError("License edition is not supported.")
        if payload.expires_at is not None and payload.expires_at <= self._now():
            raise LicenseVerificationError("License has expired.")


def load_bundled_public_keys() -> dict[str, bytes]:
    keys: dict[str, bytes] = {}
    for key_id, encoded_key in BUNDLED_PUBLIC_KEYS_BASE64.items():
        try:
            key_bytes = base64.b64decode(encoded_key, validate=True)
        except (ValueError, base64.binascii.Error) as error:
            raise LicenseVerificationError("Bundled public key is malformed.") from error
        if len(key_bytes) != 32:
            raise LicenseVerificationError("Bundled Ed25519 public key has an invalid length.")
        keys[key_id] = key_bytes
    return keys
