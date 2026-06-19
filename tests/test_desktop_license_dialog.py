import unittest

from desktop.license_dialog import license_dialog_status
from licensing.entitlements import community_entitlements
from licensing.models import LicenseState


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


if __name__ == "__main__":
    unittest.main()
