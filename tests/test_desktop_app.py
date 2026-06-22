import inspect
import unittest

from desktop import app
from frontend.automation_controller import (
    AutomationRunRequest,
    FrontendAutomationController,
)
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

        self.assertEqual("Forza Automation Assist", shell_spec.window_title)
        self.assertNotIn("Prototype", shell_spec.window_title)
        self.assertEqual(640, shell_spec.window_width)
        self.assertEqual(760, shell_spec.window_height)
        self.assertTrue(shell_spec.is_fixed_size)

    def test_desktop_app_represents_visible_workflow_states(self) -> None:
        shell_spec = app.build_desktop_app_spec()

        self.assertEqual("Prepare a Run", shell_spec.home_concept.primary_action_label)
        self.assertEqual("Commit to Supervision", shell_spec.commitment_layer.title)
        self.assertEqual((3, 2, 1), shell_spec.commitment_layer.countdown_values)
        self.assertEqual("Companion Mode", shell_spec.companion_mode.title)
        self.assertEqual("Post-Run State", shell_spec.completion_lifecycle.title)
        self.assertTrue(shell_spec.completion_lifecycle.always_returns_to_preparation)

    def test_desktop_app_workflow_contract_covers_primary_transitions(self) -> None:
        workflow = app.build_desktop_app_spec().workflow_contract

        self.assertEqual(
            (
                ("home", "automation_environment"),
                ("automation_environment", "commitment"),
                ("commitment", "countdown"),
                ("countdown", "companion_mode"),
                ("companion_mode", "completion"),
                ("completion", "automation_environment"),
                ("completion", "home"),
            ),
            workflow.transitions,
        )
        self.assertIn("visible controls", workflow.dead_button_policy)
        self.assertIn("clears prepared", workflow.state_reset_policy)

    def test_desktop_app_workflow_contract_has_no_orphan_states(self) -> None:
        workflow = app.build_desktop_app_spec().workflow_contract
        expected_states = {
            "home",
            "automation_environment",
            "commitment",
            "countdown",
            "companion_mode",
            "completion",
        }
        transition_states = {
            state
            for transition in workflow.transitions
            for state in transition
        }

        self.assertEqual(expected_states, transition_states)

    def test_desktop_app_contract_keeps_failure_recovery_explicit(self) -> None:
        workflow = app.build_desktop_app_spec().workflow_contract

        self.assertIn("clears prepared", workflow.state_reset_policy)
        self.assertIn("Auto4 is inactive", workflow.unsupported_execution_policy)
        self.assertIn("Auto1, Auto2, and Auto3", workflow.real_input_boundary)
        self.assertIn("F8", workflow.stop_policy)

    def test_desktop_app_keeps_auto4_inactive(self) -> None:
        active_automation_ids = {
            definition.automation_id for definition in get_active_automation_definitions()
        }

        self.assertEqual({"auto1", "auto2", "auto3"}, active_automation_ids)
        self.assertFalse(AUTOMATION_DEFINITIONS["auto4"].is_active)
        self.assertNotIn("auto4", active_automation_ids)

    def test_desktop_preparation_accepts_auto1_auto2_and_auto3(self) -> None:
        controller = FrontendAutomationController(
            session_id_provider=lambda: "desktop-navigation-test-session"
        )

        for automation_id in ("auto1", "auto2", "auto3"):
            definition = AUTOMATION_DEFINITIONS[automation_id]
            plan = controller.prepare_run_plan(
                AutomationRunRequest(
                    automation_id=automation_id,
                    profile_id=definition.available_profiles[0],
                    requested_count=1,
                )
            )

            self.assertTrue(plan.accepted, automation_id)
            self.assertEqual(automation_id, plan.automation_definition.automation_id)

    def test_desktop_app_execution_boundary_supports_mvp_guarded_paths(self) -> None:
        shell_spec = app.build_desktop_app_spec()
        wiring = shell_spec.execution_wiring

        self.assertEqual(("auto1", "auto2", "auto3"), wiring.enabled_automation_ids)
        self.assertEqual(("auto4",), wiring.refused_automation_ids)
        self.assertTrue(wiring.uses_existing_guarded_paths)
        self.assertTrue(wiring.preserves_f8_stop)
        self.assertTrue(wiring.fail_closed_for_unsupported_automations)
        self.assertIn("Auto4 is inactive", shell_spec.workflow_contract.unsupported_execution_policy)
        self.assertIn("Auto1, Auto2, and Auto3", shell_spec.workflow_contract.real_input_boundary)
        self.assertIn("F8", shell_spec.workflow_contract.stop_policy)

    def test_desktop_app_does_not_directly_import_real_input_backend(self) -> None:
        source = inspect.getsource(app)

        self.assertNotIn("RealKeyboardBackend", source)
        self.assertNotIn("core.input.real_keyboard_backend", source)


if __name__ == "__main__":
    unittest.main()
