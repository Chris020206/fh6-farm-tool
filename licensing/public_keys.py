"""Bundled public verification keys. Private signing keys never belong here."""

from licensing.constants import DEFAULT_SIGNING_KEY_ID

# Verification-only Ed25519 public key. The corresponding private key is not
# stored in this repository or application package.
BUNDLED_PUBLIC_KEYS_BASE64 = {
    DEFAULT_SIGNING_KEY_ID: "zxcECCoPBxcD72FdV32VirENoPTQ3DiAvKdAa3yJU64=",
}
