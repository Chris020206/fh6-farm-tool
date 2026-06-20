from pathlib import Path
from tempfile import TemporaryDirectory
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
    Auto2TestModeRealInputError,
    run_auto2_test_mode_real_input,
)
from automation.auto3_skill_tree.dangerous_auto3_multi_car_test_mode_real_input_test import (
    Auto3MultiCarTestModeRealInputError,
    run_auto3_multi_car_test_mode_real_input,
)
from automation.auto3_skill_tree.dangerous_auto3_multi_car_unlock_test import (
    Auto3MultiCarUnlockTestError,
    run_auto3_multi_car_unlock_test,
)
from licensing.models import EntitlementDecision
from licensing.service import LicenseService
from licensing.storage import LicenseStorage
from core.input.real_keyboard_backend import RealKeyboardBackendError


class _RecordingLicenseService:
    def __init__(self, allowed: bool) -> None:
        self.allowed = allowed
        self.calls: list[tuple[str, str | None, int | None]] = []

    def evaluate_execution(
        self,
        automation_id: str,
        mode: str | None = None,
        requested_count: int | None = None,
    ):
        self.calls.append((automation_id, mode, requested_count))
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

        self.assertEqual([("auto1", None, 1)], service.calls)
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

        self.assertEqual([("auto2", "purchase", None)], service.calls)
        create_backend.assert_not_called()

    @patch(
        "automation.auto2_buy_car.dangerous_auto2_test_mode_real_input_test.create_real_keyboard_backend"
    )
    def test_auto2_navigation_uses_navigation_entitlement(
        self,
        create_backend: Mock,
    ) -> None:
        service = _RecordingLicenseService(False)

        with self.assertRaisesRegex(Auto2TestModeRealInputError, "Entitlement refused"):
            run_auto2_test_mode_real_input(1, {}, Mock(), license_service=service)

        self.assertEqual([("auto2", "test", None)], service.calls)
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

        self.assertEqual([("auto3", "unlock", None)], service.calls)
        create_backend.assert_not_called()

    @patch(
        "automation.auto3_skill_tree.dangerous_auto3_multi_car_test_mode_real_input_test.create_real_keyboard_backend"
    )
    def test_auto3_navigation_uses_navigation_entitlement(
        self,
        create_backend: Mock,
    ) -> None:
        service = _RecordingLicenseService(False)

        with self.assertRaisesRegex(
            Auto3MultiCarTestModeRealInputError,
            "Entitlement refused",
        ):
            run_auto3_multi_car_test_mode_real_input(
                1,
                {},
                Mock(),
                license_service=service,
            )

        self.assertEqual([("auto3", "test", None)], service.calls)
        create_backend.assert_not_called()

    @patch("automation.auto1_race.manual_real_input_runner.create_real_keyboard_backend")
    def test_auto1_setup_failure_uses_one_nonmutating_entitlement_check(
        self,
        create_backend: Mock,
    ) -> None:
        service = _RecordingLicenseService(True)
        create_backend.side_effect = RealKeyboardBackendError("backend unavailable")

        with self.assertRaisesRegex(Auto1ManualRunError, "backend unavailable"):
            run_manual_real_input_auto1(
                cycle_count=1,
                use_fast_timings=False,
                logger=Mock(),
                profile_data={"profile_id": "test"},
                license_service=service,
            )

        self.assertEqual([("auto1", None, 1)], service.calls)

    @patch("automation.auto1_race.manual_real_input_runner.Auto1RaceRunner")
    @patch("automation.auto1_race.manual_real_input_runner.register_f8_stop_hotkey")
    @patch("automation.auto1_race.manual_real_input_runner.create_real_keyboard_backend")
    def test_auto1_passes_requested_count_to_entitlement_before_runner_start(
        self,
        create_backend: Mock,
        register_hotkey: Mock,
        runner_type: Mock,
    ) -> None:
        service = _RecordingLicenseService(True)
        expected_result = object()
        runner_type.return_value.run_cycles.return_value = expected_result

        result = run_manual_real_input_auto1(
            cycle_count=2,
            use_fast_timings=False,
            logger=Mock(),
            profile_data={"profile_id": "test"},
            license_service=service,
        )

        self.assertIs(expected_result, result)
        self.assertEqual([("auto1", None, 2)], service.calls)
        runner_type.return_value.run_cycles.assert_called_once_with(2)
        register_hotkey.return_value.unregister.assert_called_once_with()

    @patch("automation.auto1_race.manual_real_input_runner.create_real_keyboard_backend")
    def test_community_auto1_refuses_six_loops_before_keyboard_backend(
        self,
        create_backend: Mock,
    ) -> None:
        with TemporaryDirectory() as directory:
            service = LicenseService(storage=LicenseStorage(Path(directory)))

            with self.assertRaisesRegex(Auto1ManualRunError, "at most 5 Auto1 loops"):
                run_manual_real_input_auto1(
                    cycle_count=6,
                    use_fast_timings=False,
                    logger=Mock(),
                    profile_data={"profile_id": "test"},
                    license_service=service,
                )

        create_backend.assert_not_called()

    @patch("automation.auto1_race.manual_real_input_runner.Auto1RaceRunner")
    @patch("automation.auto1_race.manual_real_input_runner.register_f8_stop_hotkey")
    @patch("automation.auto1_race.manual_real_input_runner.create_real_keyboard_backend")
    def test_community_auto1_can_start_more_than_five_bounded_executions(
        self,
        create_backend: Mock,
        register_hotkey: Mock,
        runner_type: Mock,
    ) -> None:
        expected_result = object()
        runner_type.return_value.run_cycles.return_value = expected_result

        with TemporaryDirectory() as directory:
            service = LicenseService(storage=LicenseStorage(Path(directory)))

            results = [
                run_manual_real_input_auto1(
                    cycle_count=5,
                    use_fast_timings=False,
                    logger=Mock(),
                    profile_data={"profile_id": "test"},
                    license_service=service,
                )
                for _ in range(6)
            ]

        self.assertEqual([expected_result] * 6, results)
        self.assertEqual(6, create_backend.call_count)
        self.assertEqual(6, runner_type.return_value.run_cycles.call_count)
        runner_type.return_value.run_cycles.assert_called_with(5)
        self.assertEqual(6, register_hotkey.return_value.unregister.call_count)


if __name__ == "__main__":
    unittest.main()
