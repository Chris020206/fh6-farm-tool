import unittest
from unittest.mock import Mock, patch

from automation.auto1_race.manual_real_input_runner import (
    Auto1ManualRunError,
    run_manual_real_input_auto1,
)
from automation.auto2_buy_car.dangerous_auto2_one_car_purchase_test import (
    Auto2PurchaseTestError,
    run_auto2_one_car_purchase_test,
)
from automation.auto2_buy_car.dangerous_auto2_test_mode_real_input_test import (
    run_auto2_test_mode_real_input,
)
from automation.auto3_skill_tree.dangerous_auto3_multi_car_test_mode_real_input_test import (
    run_auto3_multi_car_test_mode_real_input,
)
from automation.auto3_skill_tree.dangerous_auto3_multi_car_unlock_test import (
    Auto3MultiCarUnlockTestError,
    run_auto3_multi_car_unlock_test,
)
from licensing.models import EntitlementDecision


class _RecordingLicenseService:
    def __init__(self, allowed: bool) -> None:
        self.allowed = allowed
        self.calls: list[tuple[str, str | None]] = []

    def check_execution(self, automation_id: str, mode: str | None = None):
        self.calls.append((automation_id, mode))
        return EntitlementDecision(
            allowed=self.allowed,
            message="Entitlement refused for test." if not self.allowed else "Allowed.",
            edition="community",
            required_feature="test.feature",
        )


class LicenseExecutionBoundaryTest(unittest.TestCase):
    @patch("automation.auto1_race.manual_real_input_runner.create_real_keyboard_backend")
    def test_auto1_refuses_before_real_keyboard_backend(self, create_backend: Mock) -> None:
        service = _RecordingLicenseService(False)

        with self.assertRaisesRegex(Auto1ManualRunError, "Entitlement refused"):
            run_manual_real_input_auto1(
                cycle_count=1,
                use_fast_timings=False,
                logger=Mock(),
                profile_data={},
                license_service=service,
            )

        self.assertEqual([("auto1", None)], service.calls)
        create_backend.assert_not_called()

    @patch(
        "automation.auto2_buy_car.dangerous_auto2_one_car_purchase_test.create_real_keyboard_backend"
    )
    def test_auto2_purchase_refuses_before_real_keyboard_backend(
        self,
        create_backend: Mock,
    ) -> None:
        service = _RecordingLicenseService(False)

        with self.assertRaisesRegex(Auto2PurchaseTestError, "Entitlement refused"):
            run_auto2_one_car_purchase_test(1, {}, Mock(), license_service=service)

        self.assertEqual([("auto2", "purchase")], service.calls)
        create_backend.assert_not_called()

    @patch(
        "automation.auto2_buy_car.dangerous_auto2_test_mode_real_input_test.create_real_keyboard_backend"
    )
    def test_auto2_navigation_uses_navigation_entitlement(
        self,
        create_backend: Mock,
    ) -> None:
        service = _RecordingLicenseService(False)

        with self.assertRaisesRegex(Exception, "Entitlement refused"):
            run_auto2_test_mode_real_input(1, {}, Mock(), license_service=service)

        self.assertEqual([("auto2", "test")], service.calls)
        create_backend.assert_not_called()

    @patch(
        "automation.auto3_skill_tree.dangerous_auto3_multi_car_unlock_test.create_real_keyboard_backend"
    )
    def test_auto3_unlock_refuses_before_real_keyboard_backend(
        self,
        create_backend: Mock,
    ) -> None:
        service = _RecordingLicenseService(False)

        with self.assertRaisesRegex(Auto3MultiCarUnlockTestError, "Entitlement refused"):
            run_auto3_multi_car_unlock_test(1, {}, Mock(), license_service=service)

        self.assertEqual([("auto3", "unlock")], service.calls)
        create_backend.assert_not_called()

    @patch(
        "automation.auto3_skill_tree.dangerous_auto3_multi_car_test_mode_real_input_test.create_real_keyboard_backend"
    )
    def test_auto3_navigation_uses_navigation_entitlement(
        self,
        create_backend: Mock,
    ) -> None:
        service = _RecordingLicenseService(False)

        with self.assertRaisesRegex(Exception, "Entitlement refused"):
            run_auto3_multi_car_test_mode_real_input(
                1,
                {},
                Mock(),
                license_service=service,
            )

        self.assertEqual([("auto3", "test")], service.calls)
        create_backend.assert_not_called()


if __name__ == "__main__":
    unittest.main()
