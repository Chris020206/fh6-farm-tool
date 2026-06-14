import inspect
import unittest

from desktop import app
from product.automation_registry import (
    AUTOMATION_DEFINITIONS,
    get_active_automation_definitions,
)


class DesktopAppTest(unittest.TestCase):
    def test_desktop_app_entrypoint_imports_safely(self) -> None:
        self.assertTrue(callable(app.main))
        self.assertTrue(callable(app.launch_desktop_app))
        self.assertTrue(callable(app.build_desktop_app_spec))

    def test_desktop_app_spec_uses_production_facing_naming(self) -> None:
        shell_spec = app.build_desktop_app_spec()

        self.assertEqual("FH6 Farm Tool", shell_spec.window_title)
        self.assertNotIn("Prototype", shell_spec.window_title)
        self.assertEqual(640, shell_spec.window_width)
        self.assertEqual(864, shell_spec.window_height)
        self.assertTrue(shell_spec.is_fixed_size)

    def test_desktop_app_represents_visible_workflow_states(self) -> None:
        shell_spec = app.build_desktop_app_spec()

        self.assertEqual("Prepare a Run", shell_spec.home_concept.primary_action_label)
        self.assertEqual("Commit to Supervision", shell_spec.commitment_layer.title)
        self.assertEqual((3, 2, 1), shell_spec.commitment_layer.countdown_values)
        self.assertEqual("Companion Mode", shell_spec.companion_mode.title)
        self.assertEqual("Post-Run State", shell_spec.completion_lifecycle.title)
        self.assertTrue(shell_spec.completion_lifecycle.always_returns_to_preparation)

    def test_desktop_app_keeps_auto4_inactive(self) -> None:
        active_automation_ids = {
            definition.automation_id for definition in get_active_automation_definitions()
        }

        self.assertFalse(AUTOMATION_DEFINITIONS["auto4"].is_active)
        self.assertNotIn("auto4", active_automation_ids)

    def test_desktop_app_execution_boundary_is_auto1_guarded_only(self) -> None:
        shell_spec = app.build_desktop_app_spec()
        wiring = shell_spec.execution_wiring

        self.assertEqual(("auto1",), wiring.enabled_automation_ids)
        self.assertEqual(("auto2", "auto3"), wiring.refused_automation_ids)
        self.assertTrue(wiring.uses_existing_guarded_auto1_path)
        self.assertTrue(wiring.preserves_f8_stop)
        self.assertTrue(wiring.fail_closed_for_unsupported_automations)

    def test_desktop_app_does_not_directly_import_real_input_backend(self) -> None:
        source = inspect.getsource(app)

        self.assertNotIn("RealKeyboardBackend", source)
        self.assertNotIn("core.input.real_keyboard_backend", source)


if __name__ == "__main__":
    unittest.main()
