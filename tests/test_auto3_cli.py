import subprocess
import sys
import unittest


class Auto3CliTest(unittest.TestCase):
    def test_multi_car_test_runs_in_memory_for_one_to_four_cars(self) -> None:
        for car_count in [1, 2, 3, 4]:
            with self.subTest(car_count=car_count):
                result = _run_auto3_cli(
                    "--mode",
                    "multi-car-test",
                    "--cars",
                    str(car_count),
                    "--fast",
                )

                self.assertEqual(0, result.returncode, result.output)
                self.assertIn("Mode: multi-car-test", result.output)
                self.assertIn(f"Car count: {car_count}", result.output)
                self.assertIn("Final status: completed", result.output)
                self.assertNotIn("RealKeyboardBackend", result.output)
                self.assertNotIn("F8 stop hotkey registered", result.output)

    def test_multi_car_unlock_runs_in_memory_for_one_two_and_four_cars(self) -> None:
        for car_count in [1, 2, 4]:
            with self.subTest(car_count=car_count):
                result = _run_auto3_cli(
                    "--mode",
                    "multi-car-unlock",
                    "--cars",
                    str(car_count),
                    "--fast",
                )

                self.assertEqual(0, result.returncode, result.output)
                self.assertIn("Mode: multi-car-unlock", result.output)
                self.assertIn(f"Car count: {car_count}", result.output)
                self.assertIn("Final status: completed", result.output)
                self.assertIn("No real keyboard input is sent.", result.output)
                self.assertNotIn("RealKeyboardBackend", result.output)
                self.assertNotIn("F8 stop hotkey registered", result.output)

    def test_multi_car_test_rejects_zero_cars(self) -> None:
        result = _run_auto3_cli(
            "--mode",
            "multi-car-test",
            "--cars",
            "0",
            "--fast",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Error: cars must be greater than 0.", result.output)

    def test_multi_car_unlock_rejects_zero_cars(self) -> None:
        result = _run_auto3_cli(
            "--mode",
            "multi-car-unlock",
            "--cars",
            "0",
            "--fast",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Error: cars must be greater than 0.", result.output)

    def test_multi_car_test_rejects_non_integer_cars(self) -> None:
        result = _run_auto3_cli(
            "--mode",
            "multi-car-test",
            "--cars",
            "abc",
            "--fast",
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("invalid int value", result.output)

    def test_existing_auto3_cli_mode_still_runs(self) -> None:
        result = _run_auto3_cli("--mode", "first-car-test", "--fast")

        self.assertEqual(0, result.returncode, result.output)
        self.assertIn("Mode: first-car-test", result.output)
        self.assertIn("Final status: completed", result.output)


def _run_auto3_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "automation.auto3_skill_tree.auto3_cli_test",
            *arguments,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    result.output = result.stdout + result.stderr
    return result


if __name__ == "__main__":
    unittest.main()
