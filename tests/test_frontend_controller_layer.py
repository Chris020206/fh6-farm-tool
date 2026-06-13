import unittest
from datetime import datetime, timezone

from frontend.automation_controller import (
    AutomationRunRequest,
    FrontendAutomationController,
    RefusalReason,
)
from sessions.session_status import SessionStatus


class FrontendControllerLayerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = FrontendAutomationController(
            session_id_provider=lambda: "preview-session",
            clock=lambda: datetime(2026, 6, 13, 12, 0, 0, tzinfo=timezone.utc),
        )

    def test_auto1_plan_preparation_works(self) -> None:
        plan = self.controller.prepare_run_plan(
            AutomationRunRequest(
                automation_id="auto1",
                profile_id="auto1_race_default",
                requested_count=25,
            )
        )

        self.assertTrue(plan.accepted)
        self.assertEqual("auto1", plan.automation_definition.automation_id)
        self.assertEqual("auto1_race_default", plan.profile_metadata.profile_id)
        self.assertEqual("auto1", plan.readiness_model.automation_id)
        self.assertEqual(SessionStatus.PREPARED, plan.session_preview.status)
        self.assertEqual("preview-session", plan.session_preview.session_id)
        self.assertEqual(25, plan.session_preview.requested_count)

    def test_auto2_plan_preparation_works(self) -> None:
        plan = self.controller.prepare_run_plan(
            AutomationRunRequest(
                automation_id="auto2",
                profile_id="auto2_buy_car_default",
                requested_count=1,
            )
        )

        self.assertTrue(plan.accepted)
        self.assertEqual("auto2", plan.automation_definition.automation_id)
        self.assertEqual("auto2_buy_car_default", plan.profile_metadata.profile_id)
        self.assertIn("Purchase validation can spend credits.", plan.warnings)

    def test_auto3_plan_preparation_works(self) -> None:
        plan = self.controller.prepare_run_plan(
            AutomationRunRequest(
                automation_id="auto3",
                profile_id="auto3_skill_tree_default",
                requested_count=4,
                mode="unlock",
            )
        )

        self.assertTrue(plan.accepted)
        self.assertEqual("auto3", plan.automation_definition.automation_id)
        self.assertEqual("auto3_skill_tree_default", plan.profile_metadata.profile_id)
        self.assertIn("start row A", " ".join(plan.readiness_model.recommended_setup))

    def test_auto4_is_refused(self) -> None:
        plan = self.controller.prepare_run_plan(
            AutomationRunRequest(
                automation_id="auto4",
                profile_id="auto4_remove_car_default",
                requested_count=1,
            )
        )

        self.assertFalse(plan.accepted)
        self.assertEqual(RefusalReason.INACTIVE_AUTOMATION, plan.refusal_reason)
        self.assertEqual(SessionStatus.REFUSED, plan.session_preview.status)
        self.assertIn("not active", plan.refusal_message)

    def test_unknown_automation_is_refused(self) -> None:
        plan = self.controller.prepare_run_plan(
            AutomationRunRequest(
                automation_id="unknown",
                profile_id="auto1_race_default",
                requested_count=1,
            )
        )

        self.assertFalse(plan.accepted)
        self.assertEqual(RefusalReason.UNKNOWN_AUTOMATION, plan.refusal_reason)
        self.assertIn("not known", plan.refusal_message)

    def test_unknown_profile_is_refused(self) -> None:
        plan = self.controller.prepare_run_plan(
            AutomationRunRequest(
                automation_id="auto1",
                profile_id="missing_profile",
                requested_count=1,
            )
        )

        self.assertFalse(plan.accepted)
        self.assertEqual(RefusalReason.UNKNOWN_PROFILE, plan.refusal_reason)
        self.assertEqual("auto1", plan.automation_definition.automation_id)

    def test_wrong_profile_type_is_refused(self) -> None:
        plan = self.controller.prepare_run_plan(
            AutomationRunRequest(
                automation_id="auto1",
                profile_id="auto2_buy_car_default",
                requested_count=1,
            )
        )

        self.assertFalse(plan.accepted)
        self.assertEqual(RefusalReason.PROFILE_MISMATCH, plan.refusal_reason)
        self.assertEqual("auto2_buy_car_default", plan.profile_metadata.profile_id)

    def test_invalid_requested_count_is_refused(self) -> None:
        plan = self.controller.prepare_run_plan(
            AutomationRunRequest(
                automation_id="auto1",
                profile_id="auto1_race_default",
                requested_count=0,
            )
        )

        self.assertFalse(plan.accepted)
        self.assertEqual(RefusalReason.INVALID_REQUESTED_COUNT, plan.refusal_reason)
        self.assertEqual(SessionStatus.REFUSED, plan.session_preview.status)

    def test_controller_does_not_expose_execution_method(self) -> None:
        self.assertFalse(hasattr(self.controller, "run"))
        self.assertFalse(hasattr(self.controller, "execute"))
        self.assertFalse(hasattr(self.controller, "start"))


if __name__ == "__main__":
    unittest.main()
