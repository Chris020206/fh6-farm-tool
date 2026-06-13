import unittest

from ui.architecture_integration_review import (
    CARRY_FORWARD_NOTES,
    HARD_BOUNDARIES_PRESERVED,
    build_ui_architecture_integration_review,
)


class UIArchitectureIntegrationReviewTest(unittest.TestCase):
    def setUp(self) -> None:
        self.review = build_ui_architecture_integration_review()

    def test_review_passes_as_coherent_system(self) -> None:
        self.assertTrue(self.review.passed)
        self.assertEqual("coherent", self.review.verdict)

    def test_required_integration_checks_exist(self) -> None:
        check_ids = {
            check.check_id
            for check in self.review.checks
        }

        self.assertIn("sidebar_screen_alignment", check_ids)
        self.assertIn("one_primary_intention_per_screen", check_ids)
        self.assertIn("automation_environment_flow_integration", check_ids)
        self.assertIn("companion_mode_running_only", check_ids)
        self.assertIn("secondary_screen_responsibility_separation", check_ids)
        self.assertIn("settings_profiles_separation", check_ids)
        self.assertIn("history_operational_memory", check_ids)
        self.assertIn("help_confidence_support", check_ids)
        self.assertIn("no_raw_execution_details", check_ids)
        self.assertIn("hard_boundaries_preserved", check_ids)

    def test_all_checks_have_clear_summaries(self) -> None:
        for check in self.review.checks:
            self.assertTrue(check.summary.strip())
            self.assertNotIn("panic", check.summary.lower())

    def test_carry_forward_notes_are_preserved(self) -> None:
        notes = " ".join(self.review.carry_forward_notes).lower()

        self.assertEqual(CARRY_FORWARD_NOTES, self.review.carry_forward_notes)
        self.assertIn("operational history", notes)
        self.assertIn("invalid", notes)
        self.assertIn("auto1 acknowledgement", notes)
        self.assertIn("naming consistency", notes)

    def test_hard_boundaries_remain_preserved(self) -> None:
        boundaries = " ".join(self.review.hard_boundaries_preserved).lower()

        self.assertEqual(HARD_BOUNDARIES_PRESERVED, self.review.hard_boundaries_preserved)
        self.assertIn("no visual ui", boundaries)
        self.assertIn("no styling", boundaries)
        self.assertIn("no frontend framework", boundaries)
        self.assertIn("no automation execution wiring", boundaries)
        self.assertIn("no runner calls", boundaries)
        self.assertIn("no timing changes", boundaries)
        self.assertIn("no real input changes", boundaries)
        self.assertIn("no cli behavior changes", boundaries)
        self.assertIn("no safety gate changes", boundaries)


if __name__ == "__main__":
    unittest.main()
