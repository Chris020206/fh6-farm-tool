import unittest

from product.automation_registry import get_all_automation_definitions
from product.profile_metadata_registry import get_all_profile_metadata
from product.readiness_registry import get_all_readiness_models
from ui.help_screen import (
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


if __name__ == "__main__":
    unittest.main()
