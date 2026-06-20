"""Local Licensing Authority signing with an external Ed25519 private key."""

import base64
import json
from pathlib import Path
from typing import Mapping

from licensing.parsing import canonical_payload_bytes, parse_signed_license_json
from licensing.public_keys import BUNDLED_PUBLIC_KEYS_BASE64
from licensing.models import SignedLicense


class LicenseSigningError(RuntimeError):
    """Raised when local authority signing cannot proceed safely."""


class LicenseSigner:
    def __init__(
        self,
        private_key_path: str | Path,
        signing_key_id: str,
        trusted_public_keys: Mapping[str, bytes] | None = None,
    ) -> None:
        self.private_key_path = Path(private_key_path)
        self.signing_key_id = signing_key_id
        self._trusted_public_keys = dict(
            trusted_public_keys or _decode_bundled_public_keys()
        )

    def sign_payload(self, payload: Mapping[str, object]) -> SignedLicense:
        private_key = self._load_private_key()
        signature = private_key.sign(canonical_payload_bytes(payload))
        document = {
            "payload": dict(payload),
            "signature": base64.b64encode(signature).decode("ascii"),
            "signing_key_id": self.signing_key_id,
        }
        return parse_signed_license_json(
            json.dumps(document, indent=2, ensure_ascii=False) + "\n"
        )

    def _load_private_key(self):
        try:
            key_data = self.private_key_path.read_bytes()
        except OSError as error:
            raise LicenseSigningError(
                f"Private signing key could not be read: {self.private_key_path}"
            ) from error

        try:
            from cryptography.hazmat.primitives.serialization import (
                Encoding,
                PublicFormat,
                load_pem_private_key,
            )
            from cryptography.hazmat.primitives.asymmetric.ed25519 import (
                Ed25519PrivateKey,
            )
        except ImportError as error:
            raise LicenseSigningError("Cryptography dependency is unavailable.") from error

        try:
            private_key = load_pem_private_key(key_data, password=None)
        except (TypeError, ValueError) as error:
            raise LicenseSigningError("Private signing key is invalid.") from error
        if not isinstance(private_key, Ed25519PrivateKey):
            raise LicenseSigningError("Private signing key must be Ed25519.")

        expected_public_key = self._trusted_public_keys.get(self.signing_key_id)
        if expected_public_key is None:
            raise LicenseSigningError(
                f"Signing key ID is not trusted by the desktop verifier: {self.signing_key_id}"
            )
        actual_public_key = private_key.public_key().public_bytes(
            Encoding.Raw,
            PublicFormat.Raw,
        )
        if actual_public_key != expected_public_key:
            raise LicenseSigningError(
                "Private signing key does not match the bundled desktop public key."
            )
        return private_key


def _decode_bundled_public_keys() -> dict[str, bytes]:
    try:
        return {
            key_id: base64.b64decode(encoded, validate=True)
            for key_id, encoded in BUNDLED_PUBLIC_KEYS_BASE64.items()
        }
    except (ValueError, base64.binascii.Error) as error:
        raise LicenseSigningError("Bundled public key configuration is invalid.") from error
