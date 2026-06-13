import unittest

from ui.app_flow import (
    APP_FLOW,
    AppFlowState,
    AppFlowTrigger,
)


class AppFlowArchitectureTest(unittest.TestCase):
    def test_core_transitions_are_defined(self) -> None:
        self.assertTrue(
            APP_FLOW.can_transition(
                AppFlowState.HOME,
                AppFlowState.AUTOMATION_ENVIRONMENT,
            )
        )
        self.assertTrue(
            APP_FLOW.can_transition(
                AppFlowState.PREPARED,
                AppFlowState.RUNNING,
            )
        )
        self.assertTrue(
            APP_FLOW.can_transition(
                AppFlowState.RUNNING,
                AppFlowState.COMPLETED,
            )
        )
        self.assertTrue(
            APP_FLOW.can_transition(
                AppFlowState.RUNNING,
                AppFlowState.STOPPED,
            )
        )
        self.assertTrue(
            APP_FLOW.can_transition(
                AppFlowState.RUNNING,
                AppFlowState.INTERRUPTED,
            )
        )

    def test_invalid_transitions_are_unavailable(self) -> None:
        self.assertFalse(
            APP_FLOW.can_transition(
                AppFlowState.HOME,
                AppFlowState.RUNNING,
            )
        )
        self.assertFalse(
            APP_FLOW.can_transition(
                AppFlowState.REFUSED,
                AppFlowState.RUNNING,
            )
        )
        self.assertFalse(
            APP_FLOW.can_transition(
                AppFlowState.COMPLETED,
                AppFlowState.RUNNING,
            )
        )

    def test_companion_mode_is_tied_to_running_state(self) -> None:
        self.assertTrue(
            APP_FLOW.can_transition(
                AppFlowState.RUNNING,
                AppFlowState.COMPANION_MODE,
            )
        )
        self.assertTrue(
            APP_FLOW.can_transition(
                AppFlowState.COMPANION_MODE,
                AppFlowState.RUNNING,
            )
        )
        self.assertFalse(
            APP_FLOW.can_transition(
                AppFlowState.HOME,
                AppFlowState.COMPANION_MODE,
            )
        )
        self.assertFalse(
            APP_FLOW.can_transition(
                AppFlowState.PREPARED,
                AppFlowState.COMPANION_MODE,
            )
        )

    def test_completed_stopped_interrupted_expose_calm_recovery_paths(self) -> None:
        for state in (
            AppFlowState.COMPLETED,
            AppFlowState.STOPPED,
            AppFlowState.INTERRUPTED,
        ):
            transitions = APP_FLOW.available_transitions(state)
            destinations = {
                transition.to_state
                for transition in transitions
            }

            self.assertIn(AppFlowState.HOME, destinations)
            self.assertIn(AppFlowState.AUTOMATION_ENVIRONMENT, destinations)

    def test_running_outcome_transitions_have_recovery_or_next_step_language(self) -> None:
        outcome_transitions = [
            transition
            for transition in APP_FLOW.available_transitions(AppFlowState.RUNNING)
            if transition.to_state
            in {
                AppFlowState.COMPLETED,
                AppFlowState.STOPPED,
                AppFlowState.INTERRUPTED,
            }
        ]

        self.assertEqual(3, len(outcome_transitions))
        for transition in outcome_transitions:
            self.assertIsNotNone(transition.recovery_path)
            self.assertNotIn("panic", transition.product_meaning.lower())

    def test_refused_state_does_not_imply_execution_happened(self) -> None:
        refusal_transition = next(
            transition
            for transition in APP_FLOW.available_transitions(
                AppFlowState.AUTOMATION_ENVIRONMENT
            )
            if transition.to_state == AppFlowState.REFUSED
        )

        self.assertEqual(AppFlowTrigger.HANDLE_REFUSAL, refusal_transition.trigger)
        self.assertIn("before execution", refusal_transition.user_intent)
        self.assertIn("protective clarity", refusal_transition.product_meaning)
        self.assertFalse(APP_FLOW.can_transition(AppFlowState.REFUSED, AppFlowState.RUNNING))

    def test_flow_model_has_no_execution_method(self) -> None:
        self.assertFalse(hasattr(APP_FLOW, "run"))
        self.assertFalse(hasattr(APP_FLOW, "execute"))
        self.assertFalse(hasattr(APP_FLOW, "start"))


if __name__ == "__main__":
    unittest.main()
