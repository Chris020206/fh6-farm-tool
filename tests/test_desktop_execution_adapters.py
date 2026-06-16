import inspect
import unittest

from desktop import app
from desktop import companion_shell
from desktop.execution.auto1_desktop_execution import start_auto1_ui_execution
from desktop.execution.auto2_desktop_execution import start_auto2_ui_execution
from desktop.execution.auto3_desktop_execution import start_auto3_ui_execution
from desktop.execution.execution_boundary import (
    is_desktop_execution_supported,
    is_desktop_preparation_available,
)
from desktop.execution.execution_messages import (
    completion_state_id_for_auto1_status,
    completion_state_id_for_status,
    desktop_execution_confirmation_summary,
)


class DesktopExecutionAdapterTest(unittest.TestCase):
    def test_auto1_auto2_auto3_desktop_execution_remains_supported(self) -> None:
        self.assertTrue(callable(start_auto1_ui_execution))
        self.assertTrue(callable(start_auto2_ui_execution))
        self.assertTrue(callable(start_auto3_ui_execution))

        for automation_id in ("auto1", "auto2", "auto3"):
            with self.subTest(automation_id=automation_id):
                self.assertTrue(is_desktop_execution_supported(automation_id))
                self.assertTrue(is_desktop_preparation_available(automation_id))
                self.assertIn(
                    f"guarded {automation_id.title().replace('Auto', 'Auto')}",
                    desktop_execution_confirmation_summary(automation_id),
                )

    def test_auto4_remains_refused_inactive(self) -> None:
        self.assertFalse(is_desktop_execution_supported("auto4"))
        self.assertFalse(is_desktop_preparation_available("auto4"))
        self.assertEqual(
            "Execution is unavailable from the desktop UI.",
            desktop_execution_confirmation_summary("auto4"),
        )

    def test_desktop_app_imports_safely_without_real_keyboard_backend(self) -> None:
        source = inspect.getsource(app)

        self.assertNotIn("RealKeyboardBackend", source)
        self.assertNotIn("core.input.real_keyboard_backend", source)

    def test_companion_shell_no_longer_imports_direct_dangerous_runners(self) -> None:
        source = inspect.getsource(companion_shell)

        self.assertNotIn("dangerous_auto2", source)
        self.assertNotIn("dangerous_auto3", source)

    def test_completion_state_mapping_preserved(self) -> None:
        for mapper in (completion_state_id_for_status, completion_state_id_for_auto1_status):
            with self.subTest(mapper=mapper.__name__):
                self.assertEqual("completed", mapper("completed"))
                self.assertEqual("stopped", mapper("stopped"))
                self.assertEqual("refused", mapper("failed"))
                self.assertEqual("refused", mapper("unknown"))


if __name__ == "__main__":
    unittest.main()
