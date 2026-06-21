import unittest

from desktop.license_dialog import license_dialog_status, license_import_feedback
from desktop.support_actions import open_official_discord
from licensing.entitlements import community_entitlements
from licensing.models import LicenseState
from product.support import (
    OFFICIAL_DISCORD_URL,
    community_feature_unavailable_message,
)


class DesktopLicenseDialogTest(unittest.TestCase):
    def test_community_status_is_product_facing_and_stable(self) -> None:
        status = license_dialog_status(
            LicenseState(
                status="community",
                entitlements=community_entitlements(),
                message="Community Edition is active.",
            )
        )

        self.assertEqual("Community", status.edition)
        self.assertEqual("Community", status.status)
        self.assertEqual("No local license", status.license_id)
        self.assertIn("FAA.Auto1.Full", status.enabled_features)

    def test_discord_action_opens_the_official_invite(self) -> None:
        opened_urls = []

        opened = open_official_discord(
            lambda url: opened_urls.append(url) or True
        )

        self.assertTrue(opened)
        self.assertEqual([OFFICIAL_DISCORD_URL], opened_urls)

    def test_invalid_license_feedback_is_calm_and_supportive(self) -> None:
        message = license_import_feedback(False, "Malformed input.")

        self.assertIn("License could not be activated.", message)
        self.assertIn("current edition has not been changed", message)
        self.assertIn("official FAA Discord", message)

    def test_community_feature_message_lists_current_access(self) -> None:
        message = community_feature_unavailable_message()

        self.assertIn("Community Edition", message)
        self.assertIn("Auto1 Community", message)
        self.assertIn("Auto2 Navigation Test", message)
        self.assertIn("Auto3 Navigation Test", message)
        self.assertIn("official FAA Discord", message)


if __name__ == "__main__":
    unittest.main()
