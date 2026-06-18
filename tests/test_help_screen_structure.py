import unittest

from product.automation_registry import get_all_automation_definitions
from product.profile_metadata_registry import get_all_profile_metadata
from product.readiness_registry import get_all_readiness_models
from ui.help_screen import (
    AutomationGuide,
    HelpSectionId,
    HelpTopicType,
    build_help_screen,
)


class HelpScreenStructureTest(unittest.TestCase):
    def setUp(self) -> None:
        self.screen = build_help_screen(
            automation_definitions=tuple(get_all_automation_definitions()),
            readiness_models=tuple(get_all_readiness_models()),
            profile_metadata=tuple(get_all_profile_metadata()),
        )

    def test_common_questions_are_primary(self) -> None:
        self.assertEqual(
            HelpSectionId.COMMON_QUESTIONS,
            self.screen.common_questions.section_id,
        )
        self.assertTrue(self.screen.common_questions.is_primary)
        self.assertGreater(len(self.screen.common_questions.questions), 0)

    def test_contextual_guidance_is_secondary(self) -> None:
        self.assertEqual(
            HelpSectionId.CONTEXTUAL_GUIDANCE,
            self.screen.contextual_guidance.section_id,
        )
        self.assertTrue(self.screen.contextual_guidance.is_secondary)

    def test_troubleshooting_is_tertiary(self) -> None:
        self.assertEqual(
            HelpSectionId.TROUBLESHOOTING,
            self.screen.troubleshooting.section_id,
        )
        self.assertTrue(self.screen.troubleshooting.is_tertiary)

    def test_help_is_answer_first_not_browse_first(self) -> None:
        for question in self.screen.common_questions.questions:
            self.assertTrue(question.question.strip())
            self.assertTrue(question.answer.strip())

        common_question_text = " ".join(
            question.question.lower()
            for question in self.screen.common_questions.questions
        )

        self.assertIn("what", common_question_text)
        self.assertNotIn("chapter", common_question_text)
        self.assertNotIn("documentation index", common_question_text)

    def test_help_does_not_expose_raw_technical_execution_details(self) -> None:
        all_questions = (
            self.screen.common_questions.questions
            + self.screen.contextual_guidance.questions
            + self.screen.troubleshooting.questions
        )
        all_guides = self.screen.contextual_guidance.guides

        for question in all_questions:
            serialized_values = " ".join(
                (question.question, question.answer, " ".join(question.supporting_context))
            ).lower()
            self.assertNotIn("keypress", serialized_values)
            self.assertNotIn("wait_after", serialized_values)
            self.assertNotIn("menu_key_delay", serialized_values)
            self.assertNotIn("navigation_counts", serialized_values)
            self.assertNotIn("debug", serialized_values)
            self.assertNotIn("raw log", serialized_values)

        for guide in all_guides:
            serialized_values = " ".join(
                (
                    guide.title,
                    guide.purpose,
                    guide.required_starting_position,
                    guide.target_or_vehicle_requirement or "",
                    " ".join(guide.details),
                    guide.screenshot_placeholder,
                    guide.what_happens_when_run,
                    " ".join(guide.before_you_press_run),
                    " ".join(guide.common_mistakes),
                    " ".join(guide.recovery_guidance),
                    " ".join(guide.safety_notes),
                )
            ).lower()
            self.assertNotIn("keypress", serialized_values)
            self.assertNotIn("wait_after", serialized_values)
            self.assertNotIn("menu_key_delay", serialized_values)
            self.assertNotIn("navigation_counts", serialized_values)
            self.assertNotIn("debug", serialized_values)
            self.assertNotIn("raw log", serialized_values)

    def test_help_includes_baseline_readiness_profile_and_result_guidance(self) -> None:
        all_questions = (
            self.screen.common_questions.questions
            + self.screen.contextual_guidance.questions
            + self.screen.troubleshooting.questions
        )
        topic_types = {
            question.topic_type
            for question in all_questions
        }

        self.assertIn(HelpTopicType.BASELINE, topic_types)
        self.assertIn(HelpTopicType.READINESS, topic_types)
        self.assertIn(HelpTopicType.PROFILE, topic_types)
        self.assertIn(HelpTopicType.RESULT, topic_types)

    def test_screen_has_one_primary_intention(self) -> None:
        self.assertEqual(
            "Answer common operator questions with calm confidence.",
            self.screen.primary_intention,
        )

    def test_contextual_guidance_uses_product_facing_automation_data(self) -> None:
        guidance_questions = self.screen.contextual_guidance.questions
        automation_ids = {
            question.related_automation_id
            for question in guidance_questions
            if question.related_automation_id is not None
        }

        self.assertIn("auto1", automation_ids)
        self.assertIn("auto2", automation_ids)
        self.assertIn("auto3", automation_ids)
        self.assertNotIn("auto4", automation_ids)

    def test_help_includes_operator_guides_for_auto1_auto2_and_auto3(self) -> None:
        guides = {
            guide.automation_id: guide
            for guide in self.screen.contextual_guidance.guides
        }

        self.assertEqual({"auto1", "auto2", "auto3"}, set(guides))
        self.assertIsInstance(guides["auto1"], AutomationGuide)
        self.assertIn(
            "post-race restart screen",
            guides["auto1"].required_starting_position.lower(),
        )
        self.assertTrue(
            any("pressing X restarts" in detail for detail in guides["auto1"].details)
        )
        self.assertIn(
            "Subaru Impreza 22B-STi Version (1998)",
            guides["auto2"].target_or_vehicle_requirement or "",
        )
        self.assertTrue(
            any("credits" in note.lower() for note in guides["auto2"].safety_notes)
        )
        self.assertIn(
            "currently selected vehicle",
            guides["auto3"].target_or_vehicle_requirement or "",
        )
        self.assertIn(
            "does not independently verify the car model",
            guides["auto3"].target_or_vehicle_requirement or "",
        )
        self.assertIn(
            "Garage -> Cars -> My Cars -> Recently Added",
            guides["auto3"].required_starting_position,
        )
        self.assertTrue(
            any("A1 -> B1 -> C1 -> A2" in detail for detail in guides["auto3"].details)
        )

        for guide in guides.values():
            self.assertTrue(guide.screenshot_placeholder.strip())
            self.assertIn("screenshot", guide.screenshot_placeholder.lower())

    def test_help_keeps_faq_troubleshooting_and_safety_notes(self) -> None:
        self.assertGreaterEqual(len(self.screen.common_questions.questions), 4)
        self.assertGreaterEqual(len(self.screen.troubleshooting.questions), 3)

        safety_text = " ".join(
            " ".join(guide.safety_notes)
            for guide in self.screen.contextual_guidance.guides
        ).lower()
        self.assertIn("f8", safety_text)
        self.assertIn("skill points", safety_text)
        self.assertIn("credits", safety_text)


if __name__ == "__main__":
    unittest.main()
