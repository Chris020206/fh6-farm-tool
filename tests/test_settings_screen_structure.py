from datetime import datetime, timezone
import unittest

from licensing.constants import (
    FEATURE_AUTO1_UNLIMITED,
    FEATURE_AUTO2_FULL,
    FEATURE_AUTO3_FULL,
    FEATURE_PROFILES_BASIC,
)
from licensing.entitlements import community_entitlements
from licensing.models import (
    EntitlementProfile,
    LicensePayload,
    LicenseState,
    SignedLicense,
)
from ui.settings_screen import (
    SettingsSectionId,
    build_settings_screen,
    product_facing_edition_name,
    version_information_text,
)
from product.support import OFFICIAL_DISCORD_URL
from settings.execution_preferences import ExecutionPreferences


class SettingsScreenStructureTest(unittest.TestCase):
    def test_community_settings_are_edition_first(self) -> None:
        screen = build_settings_screen(
            LicenseState(
                status="community",
                entitlements=community_entitlements(),
                message="Community Edition is active.",
            )
        )

        section = screen.license_and_edition
        self.assertEqual(SettingsSectionId.LICENSE_AND_EDITION, section.section_id)
        self.assertTrue(section.is_primary)
        self.assertEqual("Community Edition", section.edition_name)
        self.assertEqual(
            ("Auto1 Community", "Auto2 Navigation Test", "Auto3 Navigation Test"),
            tuple(feature.label for feature in section.included_features),
        )
        self.assertEqual(
            ("No license required", "Community Edition", "Community access", "No license required"),
            tuple(item.value for item in section.status_items),
        )

    def test_licensed_features_and_status_come_from_entitlements(self) -> None:
        screen = build_settings_screen(_licensed_state("founding"))

        section = screen.license_and_edition
        self.assertEqual("Founding Tester Edition", section.edition_name)
        self.assertEqual(
            (
                "Auto1 Unlimited",
                "Auto2 Full Automation",
                "Auto3 Full Automation",
                "Basic Profiles",
            ),
            tuple(feature.label for feature in section.included_features),
        )
        self.assertEqual(
            ("Licensed", "Founding Tester Edition", "Lifetime", "Offline"),
            tuple(item.value for item in section.status_items),
        )

    def test_about_is_secondary_and_copy_text_is_stable(self) -> None:
        screen = build_settings_screen(version="v0.2.0-beta")

        self.assertEqual(SettingsSectionId.ABOUT, screen.about.section_id)
        self.assertTrue(screen.about.is_secondary)
        self.assertEqual("FAA Desktop", screen.about.product)
        self.assertEqual("https://discord.gg/SgARD8YenU", OFFICIAL_DISCORD_URL)
        self.assertEqual(OFFICIAL_DISCORD_URL, screen.about.discord_url)
        self.assertEqual(
            "FAA Desktop\nVersion: v0.2.0-beta\nEdition: Community Edition\nPlatform: Windows",
            version_information_text(screen.about),
        )

    def test_execution_safety_contains_exactly_two_real_preferences(self) -> None:
        screen = build_settings_screen()

        self.assertEqual(SettingsSectionId.EXECUTION, screen.execution.section_id)
        self.assertEqual("Execution Safety", screen.execution.title)
        self.assertEqual(
            (
                "Show Auto2 Purchase confirmation",
                "Show Auto3 Unlock confirmation",
            ),
            tuple(setting.label for setting in screen.execution.settings),
        )
        self.assertTrue(all(setting.enabled for setting in screen.execution.settings))

    def test_execution_safety_reflects_persisted_values(self) -> None:
        screen = build_settings_screen(
            execution_preferences=ExecutionPreferences(
                show_auto2_purchase_confirmation=False,
                show_auto3_unlock_confirmation=True,
            )
        )

        self.assertEqual(
            (False, True),
            tuple(setting.enabled for setting in screen.execution.settings),
        )

    def test_supported_editions_have_distinct_product_names(self) -> None:
        self.assertEqual("Community Edition", product_facing_edition_name("community"))
        self.assertEqual("Basic Edition", product_facing_edition_name("basic"))
        self.assertEqual("Plus Edition", product_facing_edition_name("plus"))
        self.assertEqual(
            "Founding Tester Edition",
            product_facing_edition_name("founding"),
        )

    def test_placeholder_and_unrelated_settings_are_absent(self) -> None:
        serialized = repr(build_settings_screen()).lower()

        for prohibited in (
            "theme",
            "notification",
            "startup behavior",
            "window behavior",
            "advanced system",
            "update behavior",
            "environment detection",
            "execution tuning",
            "profile editor",
        ):
            self.assertNotIn(prohibited, serialized)


def _licensed_state(edition: str) -> LicenseState:
    issued_at = datetime(2026, 6, 21, tzinfo=timezone.utc)
    payload = LicensePayload(
        license_id="FAA-TEST-1",
        product="forza_automation_assist",
        license_version=1,
        discord_user_id="123",
        edition=edition,
        features=frozenset(
            {
                FEATURE_AUTO1_UNLIMITED,
                FEATURE_AUTO2_FULL,
                FEATURE_AUTO3_FULL,
                FEATURE_PROFILES_BASIC,
            }
        ),
        limits={},
        issued_at=issued_at,
        expires_at=None,
    )
    signed = SignedLicense(
        payload=payload,
        signature=b"signature",
        signing_key_id="test-key",
        signed_payload=b"{}",
        serialized_json="{}",
    )
    return LicenseState(
        status="licensed",
        entitlements=EntitlementProfile(
            edition=edition,
            features=payload.features,
            limits={},
            license_id=payload.license_id,
        ),
        message="License active.",
        license=signed,
    )


if __name__ == "__main__":
    unittest.main()
