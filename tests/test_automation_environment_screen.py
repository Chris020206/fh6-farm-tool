import unittest
from datetime import datetime, timezone

from frontend.automation_controller import (
    AutomationRunRequest,
    FrontendAutomationController,
)
from ui.automation_environment import (
    AdvancedSection,
    AutomationEnvironmentSectionId,
    ContextualWarningsSection,
    OverviewSection,
    ProfileSection,
    RunSection,
    SECTION_ORDER,
    build_automation_environment_screen,
)


class AutomationEnvironmentScreenTest(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = FrontendAutomationController(
            session_id_provider=lambda: "preview-session",
            clock=lambda: datetime(2026, 6, 13, 12, 0, 0, tzinfo=timezone.utc),
        )
        self.accepted_plan = self.controller.prepare_run_plan(
            AutomationRunRequest(
                automation_id="auto3",
                profile_id="auto3_skill_tree_default",
                requested_count=4,
            )
        )
        self.accepted_screen = build_automation_environment_screen(
            automation_definition=self.accepted_plan.automation_definition,
            profile_metadata=self.accepted_plan.profile_metadata,
            readiness_model=self.accepted_plan.readiness_model,
            run_plan=self.accepted_plan,
        )

    def test_five_preparation_sections_exist(self) -> None:
        self.assertEqual(5, len(self.accepted_screen.sections))

    def test_section_order_is_preserved(self) -> None:
        section_order = tuple(
            section.section_id
            for section in self.accepted_screen.sections
        )

        self.assertEqual(SECTION_ORDER, section_order)

    def test_overview_uses_automation_definition(self) -> None:
        overview = self.accepted_screen.sections[0]

        self.assertIsInstance(overview, OverviewSection)
        self.assertEqual(
            self.accepted_plan.automation_definition.display_name,
            overview.display_name,
        )
        self.assertEqual(
            self.accepted_plan.automation_definition.validated_scope,
            overview.validated_scope,
        )

    def test_profile_section_uses_profile_metadata(self) -> None:
        profile = self.accepted_screen.sections[1]

        self.assertIsInstance(profile, ProfileSection)
        self.assertEqual(
            self.accepted_plan.profile_metadata.profile_name,
            profile.profile_name,
        )
        self.assertEqual(
            self.accepted_plan.profile_metadata.behavior_summary,
            profile.behavior_summary,
        )

    def test_warnings_combine_readiness_and_run_plan_warnings_safely(self) -> None:
        warnings = self.accepted_screen.sections[2]

        self.assertIsInstance(warnings, ContextualWarningsSection)
        self.assertEqual(
            len(warnings.warnings),
            len(set(warnings.warnings)),
        )
        self.assertIn(
            "Auto3 real-input unlock commands can spend skill points.",
            warnings.warnings,
        )

    def test_run_section_reflects_accepted_plan(self) -> None:
        run = self.accepted_screen.sections[4]

        self.assertIsInstance(run, RunSection)
        self.assertTrue(run.can_prepare_commitment)
        self.assertEqual("prepared", run.status_label)
        self.assertIsNone(run.refusal_message)
        self.assertEqual(4, run.requested_count)

    def test_run_section_reflects_refused_plan(self) -> None:
        refused_plan = self.controller.prepare_run_plan(
            AutomationRunRequest(
                automation_id="auto4",
                profile_id="auto4_remove_car_default",
                requested_count=1,
            )
        )
        screen = build_automation_environment_screen(
            automation_definition=refused_plan.automation_definition,
            profile_metadata=self.accepted_plan.profile_metadata,
            readiness_model=self.accepted_plan.readiness_model,
            run_plan=refused_plan,
        )
        run = screen.sections[4]

        self.assertFalse(run.can_prepare_commitment)
        self.assertEqual("refused", run.status_label)
        self.assertIn("not active", run.refusal_message)

    def test_advanced_section_is_present_and_collapsed_by_default(self) -> None:
        advanced = self.accepted_screen.sections[3]

        self.assertIsInstance(advanced, AdvancedSection)
        self.assertEqual(AutomationEnvironmentSectionId.ADVANCED, advanced.section_id)
        self.assertTrue(advanced.is_collapsed_by_default)


if __name__ == "__main__":
    unittest.main()
