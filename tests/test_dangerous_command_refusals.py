import subprocess
import sys
import unittest


class DangerousCommandRefusalTest(unittest.TestCase):
    def test_auto1_refuses_without_confirmation(self) -> None:
        result = _run_module("automation.auto1_race.run_auto1", "1")

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Refused:", result.output)
        self.assertIn("--confirm", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto2_test_mode_refuses_without_real_input_confirmation(self) -> None:
        result = _run_module(
            "automation.auto2_buy_car.dangerous_auto2_test_mode_real_input_test",
            "1",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Refused:", result.output)
        self.assertIn("--confirm-real-input", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto2_one_car_purchase_requires_real_input_confirmation(self) -> None:
        result = _run_module(
            "automation.auto2_buy_car.dangerous_auto2_one_car_purchase_test",
            "1",
            "--confirm-purchase",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Refused:", result.output)
        self.assertIn("--confirm-real-input", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto2_one_car_purchase_requires_purchase_confirmation(self) -> None:
        result = _run_module(
            "automation.auto2_buy_car.dangerous_auto2_one_car_purchase_test",
            "1",
            "--confirm-real-input",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Refused:", result.output)
        self.assertIn("--confirm-purchase", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto2_one_car_purchase_rejects_cycle_counts_other_than_one(self) -> None:
        result = _run_module(
            "automation.auto2_buy_car.dangerous_auto2_one_car_purchase_test",
            "2",
            "--confirm-real-input",
            "--confirm-purchase",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Refused:", result.output)
        self.assertIn("exactly 1", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto3_test_mode_refuses_without_real_input_confirmation(self) -> None:
        result = _run_module(
            "automation.auto3_skill_tree.dangerous_auto3_test_mode_real_input_test",
            "--mode",
            "first-car-test",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Refused:", result.output)
        self.assertIn("--confirm-real-input", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto3_test_mode_rejects_unsupported_mode(self) -> None:
        result = _run_module(
            "automation.auto3_skill_tree.dangerous_auto3_test_mode_real_input_test",
            "--mode",
            "full-first-car",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("invalid choice", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto3_multi_car_test_mode_refuses_without_real_input_confirmation(
        self,
    ) -> None:
        result = _run_module(
            "automation.auto3_skill_tree."
            "dangerous_auto3_multi_car_test_mode_real_input_test",
            "--cars",
            "2",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Refused:", result.output)
        self.assertIn("--confirm-real-input", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto3_multi_car_test_mode_requires_cars_argument(self) -> None:
        result = _run_module(
            "automation.auto3_skill_tree."
            "dangerous_auto3_multi_car_test_mode_real_input_test",
            "--confirm-real-input",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("required", result.output)
        self.assertIn("--cars", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto3_multi_car_test_mode_rejects_zero_cars(self) -> None:
        result = _run_module(
            "automation.auto3_skill_tree."
            "dangerous_auto3_multi_car_test_mode_real_input_test",
            "--cars",
            "0",
            "--confirm-real-input",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Error: cars must be greater than 0.", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto3_multi_car_test_mode_rejects_more_than_four_cars(self) -> None:
        result = _run_module(
            "automation.auto3_skill_tree."
            "dangerous_auto3_multi_car_test_mode_real_input_test",
            "--cars",
            "5",
            "--confirm-real-input",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Error: cars must be 4 or fewer.", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto3_multi_car_unlock_requires_real_input_confirmation(self) -> None:
        result = _run_module(
            "automation.auto3_skill_tree.dangerous_auto3_multi_car_unlock_test",
            "--cars",
            "1",
            "--confirm-unlock",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Refused:", result.output)
        self.assertIn("--confirm-real-input", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto3_multi_car_unlock_requires_unlock_confirmation(self) -> None:
        result = _run_module(
            "automation.auto3_skill_tree.dangerous_auto3_multi_car_unlock_test",
            "--cars",
            "1",
            "--confirm-real-input",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Refused:", result.output)
        self.assertIn("--confirm-unlock", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto3_multi_car_unlock_rejects_zero_cars(self) -> None:
        result = _run_module(
            "automation.auto3_skill_tree.dangerous_auto3_multi_car_unlock_test",
            "--cars",
            "0",
            "--confirm-real-input",
            "--confirm-unlock",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Error: cars must be greater than 0.", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto3_multi_car_unlock_rejects_more_than_four_cars(self) -> None:
        result = _run_module(
            "automation.auto3_skill_tree.dangerous_auto3_multi_car_unlock_test",
            "--cars",
            "5",
            "--confirm-real-input",
            "--confirm-unlock",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Error: cars must be 4 or fewer.", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto3_multi_car_unlock_help_works(self) -> None:
        result = _run_module(
            "automation.auto3_skill_tree.dangerous_auto3_multi_car_unlock_test",
            "--help",
        )

        self.assertEqual(0, result.returncode)
        self.assertIn("--confirm-real-input", result.output)
        self.assertIn("--confirm-unlock", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto3_one_car_unlock_requires_real_input_confirmation(self) -> None:
        result = _run_module(
            "automation.auto3_skill_tree.dangerous_auto3_one_car_unlock_test",
            "--mode",
            "first-car",
            "--confirm-unlock",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Refused:", result.output)
        self.assertIn("--confirm-real-input", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto3_one_car_unlock_requires_unlock_confirmation(self) -> None:
        result = _run_module(
            "automation.auto3_skill_tree.dangerous_auto3_one_car_unlock_test",
            "--mode",
            "first-car",
            "--confirm-real-input",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Refused:", result.output)
        self.assertIn("--confirm-unlock", result.output)
        self.assert_no_real_input_startup(result.output)

    def test_auto3_one_car_unlock_rejects_unsupported_mode(self) -> None:
        result = _run_module(
            "automation.auto3_skill_tree.dangerous_auto3_one_car_unlock_test",
            "--mode",
            "normal-next-car",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("invalid choice", result.output)
        self.assert_no_real_input_startup(result.output)

    def assert_no_real_input_startup(self, output: str) -> None:
        self.assertNotIn("F8 stop hotkey registered", output)
        self.assertNotIn("Real keyboard backend", output)
        self.assertNotIn("Run Summary", output)


def _run_module(module_name: str, *arguments: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, "-B", "-m", module_name, *arguments],
        capture_output=True,
        text=True,
        check=False,
    )
    result.output = result.stdout + result.stderr
    return result


if __name__ == "__main__":
    unittest.main()
