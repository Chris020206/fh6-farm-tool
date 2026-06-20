from datetime import datetime, timedelta, timezone
import io
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)

from licensing.admin.authority import LicenseAdminError, ManualLicensingAuthority
from licensing.admin.cli import main as license_admin_main
from licensing.admin.repository import LicenseAdminRepository
from licensing.admin.signing import LicenseSigner, LicenseSigningError
from licensing.constants import (
    FEATURE_AUTO1_UNLIMITED,
    FEATURE_AUTO2_FULL,
    FEATURE_AUTO3_FULL,
    FEATURE_AUTO4_FULL,
    FEATURE_BATCH_LIMIT_EXTENDED,
    FEATURE_PROFILES_BASIC,
    FEATURE_PROFILES_PLUS,
)
from licensing.parsing import parse_license_key, parse_signed_license_json
from licensing.service import LicenseService
from licensing.storage import LicenseStorage
from licensing.verification import LicenseVerifier


class _AdvancingClock:
    def __init__(self) -> None:
        self.current = datetime(2026, 6, 20, 12, 0, tzinfo=timezone.utc)

    def __call__(self) -> datetime:
        result = self.current
        self.current += timedelta(seconds=1)
        return result


class ManualLicenseIssuanceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.private_key = Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key().public_bytes(
            Encoding.Raw,
            PublicFormat.Raw,
        )
        self.key_id = "FAA_KEY_TEST_ISSUANCE"
        self.private_key_path = self.root / "private_key.pem"
        self.private_key_path.write_bytes(
            self.private_key.private_bytes(
                Encoding.PEM,
                PrivateFormat.PKCS8,
                NoEncryption(),
            )
        )
        self.repository = LicenseAdminRepository(self.root / "licensing.db")
        self.repository.initialize()
        self.signer = LicenseSigner(
            self.private_key_path,
            self.key_id,
            trusted_public_keys={self.key_id: self.public_key},
        )
        self.clock = _AdvancingClock()
        self.next_id = 1
        self.authority = ManualLicensingAuthority(
            self.repository,
            signer=self.signer,
            now=self.clock,
            license_id_factory=self._license_id,
        )
        self.verifier = LicenseVerifier(
            {self.key_id: self.public_key},
            now=lambda: datetime(2026, 6, 20, 13, 0, tzinfo=timezone.utc),
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_basic_issuance_creates_customer_license_and_event(self) -> None:
        issued = self.authority.issue("123456789", "basic")

        self.verifier.verify(issued.signed_license)
        payload = issued.signed_license.payload
        self.assertEqual("basic", payload.edition)
        self.assertEqual(
            frozenset(
                {
                    FEATURE_AUTO1_UNLIMITED,
                    FEATURE_AUTO2_FULL,
                    FEATURE_AUTO3_FULL,
                    FEATURE_PROFILES_BASIC,
                }
            ),
            payload.features,
        )
        customer = self.repository.get_customer("123456789")
        self.assertEqual(payload.license_id, customer.current_license_id)
        record = self.repository.get_license(payload.license_id)
        self.assertEqual("active", record.status)
        self.assertEqual("issued", self.repository.list_events("123456789")[0].event_type)

    def test_plus_and_founding_editions_use_locked_claims(self) -> None:
        plus = self.authority.issue("200000001", "plus").signed_license.payload
        founding = self.authority.issue("200000002", "founding").signed_license.payload

        for payload in (plus, founding):
            self.assertIn(FEATURE_AUTO4_FULL, payload.features)
            self.assertIn(FEATURE_PROFILES_PLUS, payload.features)
            self.assertIn(FEATURE_BATCH_LIMIT_EXTENDED, payload.features)
        self.assertEqual("plus", plus.edition)
        self.assertEqual("founding", founding.edition)
        self.assertIsNone(founding.expires_at)
        self.assertTrue(founding.metadata["founding_supporter"])

    def test_founding_expiration_and_developer_edition_are_refused(self) -> None:
        with self.assertRaisesRegex(LicenseAdminError, "must not expire"):
            self.authority.issue(
                "300000001",
                "founding",
                datetime(2027, 1, 1, tzinfo=timezone.utc),
            )
        with self.assertRaisesRegex(ValueError, "basic, plus, founding"):
            self.authority.issue("300000002", "developer_admin")

    def test_lookup_returns_active_license_history_and_events(self) -> None:
        issued = self.authority.issue("400000001", "basic")

        lookup = self.authority.lookup("400000001")

        self.assertEqual("400000001", lookup.customer.discord_user_id)
        self.assertEqual(issued.signed_license.payload.license_id, lookup.active_license.license_id)
        self.assertEqual(1, len(lookup.license_history))
        self.assertEqual(1, len(lookup.events))

    def test_export_resends_the_same_active_license(self) -> None:
        issued = self.authority.issue("500000001", "plus")
        destination = self.root / "exports" / "customer.lic"

        exported_path = self.authority.export_active("500000001", destination)
        exported = parse_signed_license_json(exported_path.read_text(encoding="utf-8"))

        self.verifier.verify(exported)
        self.assertEqual(issued.signed_license.signature, exported.signature)
        self.assertEqual(issued.signed_license.payload.license_id, exported.payload.license_id)
        event_types = [event.event_type for event in self.repository.list_events("500000001")]
        self.assertEqual(["issued", "exported"], event_types)

    def test_basic_to_plus_replacement_is_new_and_desktop_compatible(self) -> None:
        basic = self.authority.issue("600000001", "basic")
        plus = self.authority.replace("600000001", "plus")

        self.assertNotEqual(
            basic.signed_license.payload.license_id,
            plus.signed_license.payload.license_id,
        )
        self.assertEqual(
            basic.signed_license.payload.license_id,
            plus.signed_license.payload.replaces_license_id,
        )
        old_record = self.repository.get_license(basic.signed_license.payload.license_id)
        new_record = self.repository.get_license(plus.signed_license.payload.license_id)
        self.assertEqual("superseded", old_record.status)
        self.assertEqual("active", new_record.status)
        self.assertEqual(
            new_record.license_id,
            self.repository.get_customer("600000001").current_license_id,
        )

        desktop_root = self.root / "desktop_state"
        desktop_service = LicenseService(
            storage=LicenseStorage(desktop_root),
            verifier=self.verifier,
        )
        self.assertTrue(
            desktop_service.import_json(basic.signed_license.serialized_json).accepted
        )
        replacement = desktop_service.import_json(plus.signed_license.serialized_json)
        self.assertTrue(replacement.accepted)
        self.assertEqual("plus", replacement.state.entitlements.edition)
        self.assertEqual(
            plus.signed_license.payload.license_id,
            replacement.state.license.payload.license_id,
        )

    def test_same_or_lower_edition_replacement_is_refused(self) -> None:
        self.authority.issue("700000001", "plus")

        with self.assertRaisesRegex(LicenseAdminError, "must be an upgrade"):
            self.authority.replace("700000001", "plus")
        with self.assertRaisesRegex(LicenseAdminError, "must be an upgrade"):
            self.authority.replace("700000001", "basic")

    def test_paste_key_round_trips_through_milestone_1_parser(self) -> None:
        issued = self.authority.issue("800000001", "basic")

        decoded = parse_license_key(issued.paste_key)
        self.verifier.verify(decoded)

        self.assertEqual(self.key_id, decoded.signing_key_id)
        self.assertEqual(issued.signed_license.payload.license_id, decoded.payload.license_id)

    def test_signer_rejects_private_key_not_trusted_by_desktop(self) -> None:
        another_key = Ed25519PrivateKey.generate()
        path = self.root / "wrong.pem"
        path.write_bytes(
            another_key.private_bytes(
                Encoding.PEM,
                PrivateFormat.PKCS8,
                NoEncryption(),
            )
        )
        signer = LicenseSigner(
            path,
            self.key_id,
            trusted_public_keys={self.key_id: self.public_key},
        )

        with self.assertRaisesRegex(LicenseSigningError, "does not match"):
            signer.sign_payload(
                {
                    "license_id": "test",
                    "product": "forza_automation_assist",
                    "license_version": 1,
                    "discord_user_id": "1",
                    "edition": "basic",
                    "features": [],
                    "limits": {},
                    "issued_at": "2026-06-20T12:00:00Z",
                    "expires_at": None,
                    "replaces_license_id": None,
                }
            )

    def test_cli_issue_lookup_export_and_replace(self) -> None:
        database = self.root / "cli.db"
        first_output = self.root / "cli-basic.lic"
        second_output = self.root / "cli-plus.lic"
        common = [
            "--database",
            str(database),
            "--private-key",
            str(self.private_key_path),
            "--signing-key-id",
            self.key_id,
        ]
        trusted = {self.key_id: self.public_key}
        with patch(
            "licensing.admin.signing._decode_bundled_public_keys",
            return_value=trusted,
        ):
            with patch("sys.stdout", new_callable=io.StringIO):
                self.assertEqual(
                    0,
                    license_admin_main(
                        common
                        + [
                            "issue",
                            "--discord-id",
                            "900000001",
                            "--edition",
                            "basic",
                            "--out",
                            str(first_output),
                        ]
                    ),
                )
                self.assertEqual(
                    0,
                    license_admin_main(
                        common
                        + [
                            "replace",
                            "--discord-id",
                            "900000001",
                            "--edition",
                            "plus",
                            "--out",
                            str(second_output),
                        ]
                    ),
                )
                self.assertEqual(
                    0,
                    license_admin_main(
                        ["--database", str(database), "lookup", "--discord-id", "900000001"]
                    ),
                )
        self.assertTrue(first_output.exists())
        self.assertTrue(second_output.exists())

    def test_repository_contains_no_committed_private_key_material(self) -> None:
        repository_root = Path(__file__).resolve().parents[1]
        private_key_markers = []
        private_key_marker = b"-----BEGIN " + b"PRIVATE KEY-----"
        for path in repository_root.rglob("*"):
            if not path.is_file() or any(
                part in {".git", "__pycache__", "dist", "output", "build"}
                for part in path.parts
            ):
                continue
            try:
                content = path.read_bytes()
            except OSError:
                continue
            if private_key_marker in content:
                private_key_markers.append(path)

        self.assertEqual([], private_key_markers)

    def _license_id(self, _issued_at: datetime) -> str:
        value = f"FAA-TEST-{self.next_id:04d}"
        self.next_id += 1
        return value


if __name__ == "__main__":
    unittest.main()
