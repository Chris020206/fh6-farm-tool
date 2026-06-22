import base64
from datetime import datetime, timezone
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from licensing.constants import (
    DEFAULT_SIGNING_KEY_ID,
    FEATURE_AUTO1_UNLIMITED,
    FEATURE_AUTO2_FULL,
    FEATURE_AUTO3_FULL,
    PRODUCT_ID,
)
from licensing.entitlements import (
    COMMUNITY_AUTO1_MAX_LOOPS_PER_EXECUTION,
    LICENSED_AUTO1_MAX_LOOPS_PER_EXECUTION,
)
from licensing.parsing import (
    LicenseParseError,
    canonical_payload_bytes,
    parse_license_key,
    parse_signed_license_json,
)
from licensing.service import LicenseService
from licensing.storage import LicenseStorage
from licensing.verification import (
    LicenseVerificationError,
    LicenseVerifier,
    load_bundled_public_keys,
)


class LicenseFoundationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.private_key = Ed25519PrivateKey.generate()
        public_key = self.private_key.public_key().public_bytes(
            Encoding.Raw,
            PublicFormat.Raw,
        )
        self.verifier = LicenseVerifier(
            {DEFAULT_SIGNING_KEY_ID: public_key},
            now=lambda: datetime(2026, 6, 19, tzinfo=timezone.utc),
        )

    def test_signed_json_parses_and_verifies_offline(self) -> None:
        signed = parse_signed_license_json(self._signed_json())

        self.verifier.verify(signed)

        self.assertEqual("FAA-2026-000001", signed.payload.license_id)
        self.assertEqual("plus", signed.payload.edition)
        self.assertIn(FEATURE_AUTO2_FULL, signed.payload.features)

    def test_bundled_public_key_is_valid_ed25519_material(self) -> None:
        bundled_keys = load_bundled_public_keys()

        self.assertEqual(32, len(bundled_keys[DEFAULT_SIGNING_KEY_ID]))

    def test_fixed_fixture_verifies_with_bundled_public_key(self) -> None:
        fixture_path = (
            Path(__file__).parent
            / "fixtures"
            / "licensing"
            / "valid_plus_license.lic"
        )
        signed = parse_signed_license_json(fixture_path.read_text(encoding="utf-8"))

        LicenseVerifier().verify(signed)

        self.assertEqual("FAA-DEV-FIXTURE-0001", signed.payload.license_id)
        self.assertEqual(DEFAULT_SIGNING_KEY_ID, signed.signing_key_id)

    def test_pasteable_key_decodes_to_same_license_payload(self) -> None:
        payload = self._payload()
        payload_bytes = canonical_payload_bytes(payload)
        signature = self.private_key.sign(payload_bytes)
        key = "FAA-LIC-v1.{}.{}.{}".format(
            _base64url(DEFAULT_SIGNING_KEY_ID.encode("utf-8")),
            _base64url(payload_bytes),
            _base64url(signature),
        )

        signed = parse_license_key(key)
        self.verifier.verify(signed)

        self.assertEqual(payload["license_id"], signed.payload.license_id)
        self.assertEqual(DEFAULT_SIGNING_KEY_ID, signed.signing_key_id)

    def test_legacy_pasteable_key_uses_default_signing_key_id(self) -> None:
        payload = self._payload()
        payload_bytes = canonical_payload_bytes(payload)
        key = "FAA-LIC-v1.{}.{}".format(
            _base64url(payload_bytes),
            _base64url(self.private_key.sign(payload_bytes)),
        )

        signed = parse_license_key(key)

        self.assertEqual(DEFAULT_SIGNING_KEY_ID, signed.signing_key_id)

    def test_pasteable_key_selects_the_encoded_signing_key_id(self) -> None:
        signing_key_id = "FAA_KEY_ROTATED_TEST"
        payload = self._payload()
        payload_bytes = canonical_payload_bytes(payload)
        key = "FAA-LIC-v1.{}.{}.{}".format(
            _base64url(signing_key_id.encode("utf-8")),
            _base64url(payload_bytes),
            _base64url(self.private_key.sign(payload_bytes)),
        )
        public_key = self.private_key.public_key().public_bytes(
            Encoding.Raw,
            PublicFormat.Raw,
        )

        signed = parse_license_key(key)
        LicenseVerifier({signing_key_id: public_key}).verify(signed)

        self.assertEqual(signing_key_id, signed.signing_key_id)

    def test_malformed_invalid_expired_and_unsupported_licenses_fail_closed(self) -> None:
        with self.assertRaises(LicenseParseError):
            parse_signed_license_json("not-json")

        tampered = json.loads(self._signed_json())
        tampered["payload"]["edition"] = "basic"
        with self.assertRaises(LicenseVerificationError):
            self.verifier.verify(parse_signed_license_json(json.dumps(tampered)))

        expired = self._payload(expires_at="2026-06-18T00:00:00Z")
        with self.assertRaisesRegex(LicenseVerificationError, "expired"):
            self.verifier.verify(parse_signed_license_json(self._signed_json(expired)))

        wrong_product = self._payload(product="another_product")
        with self.assertRaisesRegex(LicenseVerificationError, "different product"):
            self.verifier.verify(parse_signed_license_json(self._signed_json(wrong_product)))

        unsupported_version = self._payload(license_version=2)
        with self.assertRaisesRegex(LicenseVerificationError, "version"):
            self.verifier.verify(parse_signed_license_json(self._signed_json(unsupported_version)))

    def test_missing_license_starts_in_community_edition(self) -> None:
        with TemporaryDirectory() as directory:
            service = self._service(Path(directory))

            state = service.current_state()

            self.assertEqual("community", state.status)
            self.assertEqual("community", state.entitlements.edition)
            self.assertFalse(state.is_licensed)

    def test_valid_file_and_key_import_store_active_license(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            service = self._service(root)
            source = root / "incoming.lic"
            source.write_text(self._signed_json(), encoding="utf-8")

            file_result = service.import_file(source)

            self.assertTrue(file_result.accepted)
            self.assertTrue(service.current_state().is_licensed)
            self.assertTrue((root / "license.lic").exists())

            payload = self._payload()
            payload_bytes = canonical_payload_bytes(payload)
            key = "FAA-LIC-v1.{}.{}.{}".format(
                _base64url(DEFAULT_SIGNING_KEY_ID.encode("utf-8")),
                _base64url(payload_bytes),
                _base64url(self.private_key.sign(payload_bytes)),
            )
            key_result = service.import_key(key)
            self.assertTrue(key_result.accepted)

    def test_invalid_import_does_not_replace_valid_installed_license(self) -> None:
        with TemporaryDirectory() as directory:
            service = self._service(Path(directory))
            self.assertTrue(service.import_json(self._signed_json()).accepted)

            result = service.import_json("{}")

            self.assertFalse(result.accepted)
            self.assertTrue(result.state.is_licensed)
            self.assertEqual("FAA-2026-000001", result.state.license.payload.license_id)

    def test_invalid_import_from_community_remains_community(self) -> None:
        with TemporaryDirectory() as directory:
            service = self._service(Path(directory))

            result = service.import_json("not a license")

            self.assertFalse(result.accepted)
            self.assertEqual("community", result.state.entitlements.edition)
            self.assertFalse(result.state.is_licensed)

    def test_rejected_replacement_preserves_existing_edition(self) -> None:
        with TemporaryDirectory() as directory:
            service = self._service(Path(directory))
            self.assertTrue(service.import_json(self._signed_json()).accepted)

            result = service.import_json("malformed replacement")

            self.assertFalse(result.accepted)
            current = service.current_state()
            self.assertTrue(current.is_licensed)
            self.assertEqual("plus", current.entitlements.edition)
            self.assertEqual("FAA-2026-000001", current.license.payload.license_id)

    def test_installed_license_can_be_removed_to_restore_community(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            service = self._service(root)
            self.assertTrue(service.import_json(self._signed_json()).accepted)

            result = service.remove_license()

            self.assertTrue(result.accepted)
            self.assertEqual("community", result.state.status)
            self.assertFalse((root / "license.lic").exists())
            self.assertFalse(service.current_state().is_licensed)

    def test_removing_missing_license_is_a_clear_no_op(self) -> None:
        with TemporaryDirectory() as directory:
            service = self._service(Path(directory))

            result = service.remove_license()

            self.assertFalse(result.accepted)
            self.assertEqual("No local license is installed.", result.message)

    def test_newer_same_owner_upgrade_replaces_license(self) -> None:
        with TemporaryDirectory() as directory:
            service = self._service(Path(directory))
            basic = self._payload(
                license_id="FAA-2026-000001",
                edition="basic",
                features=[FEATURE_AUTO1_UNLIMITED, FEATURE_AUTO2_FULL, FEATURE_AUTO3_FULL],
            )
            plus = self._payload(
                license_id="FAA-2026-000002",
                edition="plus",
                issued_at="2026-06-19T13:00:00Z",
                replaces_license_id="FAA-2026-000001",
            )
            self.assertTrue(service.import_json(self._signed_json(basic)).accepted)

            result = service.import_json(self._signed_json(plus))

            self.assertTrue(result.accepted)
            self.assertEqual("FAA-2026-000002", service.current_state().license.payload.license_id)

    def test_owner_mismatch_older_replacement_and_downgrade_are_refused(self) -> None:
        cases = (
            self._payload(
                license_id="FAA-2",
                discord_user_id="999999999",
                issued_at="2026-06-19T13:00:00Z",
            ),
            self._payload(license_id="FAA-2", issued_at="2026-06-18T13:00:00Z"),
            self._payload(
                license_id="FAA-2",
                edition="basic",
                issued_at="2026-06-19T13:00:00Z",
            ),
        )
        for candidate in cases:
            with self.subTest(candidate=candidate):
                with TemporaryDirectory() as directory:
                    service = self._service(Path(directory))
                    self.assertTrue(service.import_json(self._signed_json()).accepted)
                    result = service.import_json(self._signed_json(candidate))
                    self.assertFalse(result.accepted)
                    self.assertEqual(
                        "FAA-2026-000001",
                        service.current_state().license.payload.license_id,
                    )

    def test_community_auto1_allows_repeated_five_loop_executions(self) -> None:
        with TemporaryDirectory() as directory:
            service = self._service(Path(directory))

            evaluations = [
                service.evaluate_execution("auto1", requested_count=5)
                for _ in range(10)
            ]

            self.assertTrue(all(decision.allowed for decision in evaluations))
            self.assertTrue(
                all(
                    decision.max_loops_per_execution
                    == COMMUNITY_AUTO1_MAX_LOOPS_PER_EXECUTION
                    for decision in evaluations
                )
            )

    def test_community_auto1_refuses_more_than_five_loops(self) -> None:
        with TemporaryDirectory() as directory:
            service = self._service(Path(directory))

            decision = service.evaluate_execution("auto1", requested_count=6)

            self.assertFalse(decision.allowed)
            self.assertIn("at most 5 Auto1 loops", decision.message)

    def test_licensed_auto1_allows_up_to_twenty_five_loops(self) -> None:
        with TemporaryDirectory() as directory:
            service = self._service(Path(directory))
            self.assertTrue(service.import_json(self._signed_json()).accepted)

            allowed = service.evaluate_execution("auto1", requested_count=25)
            refused = service.evaluate_execution("auto1", requested_count=26)

            self.assertTrue(allowed.allowed)
            self.assertEqual(
                LICENSED_AUTO1_MAX_LOOPS_PER_EXECUTION,
                allowed.max_loops_per_execution,
            )
            self.assertFalse(refused.allowed)
            self.assertIn("at most 25 Auto1 loops", refused.message)

    def test_community_and_paid_feature_gates(self) -> None:
        with TemporaryDirectory() as directory:
            service = self._service(Path(directory))
            self.assertTrue(service.evaluate_execution("auto2", "test").allowed)
            self.assertFalse(service.evaluate_execution("auto2", "purchase").allowed)
            self.assertTrue(service.evaluate_execution("auto3", "test").allowed)
            self.assertFalse(service.evaluate_execution("auto3", "unlock").allowed)
            self.assertFalse(service.evaluate_execution("auto4", "full").allowed)

            self.assertTrue(service.import_json(self._signed_json()).accepted)
            self.assertTrue(service.evaluate_execution("auto1").allowed)
            self.assertTrue(service.evaluate_execution("auto2", "purchase").allowed)
            self.assertTrue(service.evaluate_execution("auto3", "unlock").allowed)

    def test_unknown_auto2_and_auto3_modes_fail_closed(self) -> None:
        with TemporaryDirectory() as directory:
            service = self._service(Path(directory))

            for automation_id, mode in (
                ("auto2", None),
                ("auto2", "purchsae"),
                ("auto3", None),
                ("auto3", "unlok"),
            ):
                with self.subTest(automation_id=automation_id, mode=mode):
                    decision = service.evaluate_execution(automation_id, mode)
                    self.assertFalse(decision.allowed)
                    self.assertIn("not supported", decision.message)

            self.assertTrue(service.import_json(self._signed_json()).accepted)
            self.assertFalse(service.evaluate_execution("auto2", "unknown").allowed)
            self.assertFalse(service.evaluate_execution("auto3", "unknown").allowed)

    def test_legacy_community_usage_state_no_longer_limits_auto1(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "community_usage.json").write_text("broken", encoding="utf-8")
            service = self._service(root)

            decision = service.evaluate_execution("auto1", requested_count=5)

            self.assertTrue(decision.allowed)

    def _service(self, directory: Path) -> LicenseService:
        return LicenseService(
            storage=LicenseStorage(directory),
            verifier=self.verifier,
        )

    def _payload(self, **overrides) -> dict:
        payload = {
            "license_id": "FAA-2026-000001",
            "product": PRODUCT_ID,
            "license_version": 1,
            "discord_user_id": "123456789012345678",
            "edition": "plus",
            "features": [
                FEATURE_AUTO1_UNLIMITED,
                FEATURE_AUTO2_FULL,
                FEATURE_AUTO3_FULL,
            ],
            "limits": {
                "FAA.Auto1.MaxRuns": None,
                "FAA.Auto2.MaxBatch": 50,
                "FAA.Auto3.MaxBatch": 50,
            },
            "issued_at": "2026-06-19T12:00:00Z",
            "expires_at": None,
            "replaces_license_id": None,
        }
        payload.update(overrides)
        return payload

    def _signed_json(self, payload: dict | None = None) -> str:
        payload = payload or self._payload()
        signature = self.private_key.sign(canonical_payload_bytes(payload))
        return json.dumps(
            {
                "payload": payload,
                "signature": base64.b64encode(signature).decode("ascii"),
                "signing_key_id": DEFAULT_SIGNING_KEY_ID,
            }
        )


def _base64url(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


if __name__ == "__main__":
    unittest.main()
