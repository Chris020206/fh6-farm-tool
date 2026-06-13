import unittest

from product.automation_registry import get_active_automation_definitions
from product.readiness_model import AcknowledgementLevel, ReadinessModel
from product.readiness_registry import (
    READINESS_MODELS,
    get_all_readiness_models,
    get_readiness_model,
)


FORBIDDEN_CERTAINTY_WORDS = ("Verified", "Guaranteed", "Confirmed")


class ReadinessModelLayerTest(unittest.TestCase):
    def test_active_automations_have_readiness_models(self) -> None:
        active_automation_ids = {
            automation.automation_id
            for automation in get_active_automation_definitions()
        }

        self.assertEqual({"auto1", "auto2", "auto3"}, active_automation_ids)
        self.assertTrue(active_automation_ids.issubset(READINESS_MODELS.keys()))

    def test_readiness_registry_returns_models(self) -> None:
        auto1_readiness = get_readiness_model("auto1")

        self.assertIsInstance(auto1_readiness, ReadinessModel)
        self.assertEqual("auto1", auto1_readiness.automation_id)
        self.assertEqual(
            AcknowledgementLevel.STANDARD,
            auto1_readiness.acknowledgement_level,
        )

    def test_friction_is_proportional_to_risk(self) -> None:
        self.assertEqual(
            AcknowledgementLevel.STANDARD,
            get_readiness_model("auto1").acknowledgement_level,
        )
        self.assertEqual(
            AcknowledgementLevel.DOUBLE_CONFIRMATION,
            get_readiness_model("auto2").acknowledgement_level,
        )
        self.assertEqual(
            AcknowledgementLevel.DOUBLE_CONFIRMATION,
            get_readiness_model("auto3").acknowledgement_level,
        )

    def test_readiness_language_does_not_claim_fake_verification(self) -> None:
        for readiness_model in get_all_readiness_models():
            all_wording = " ".join(
                (
                    readiness_model.expected_baseline,
                    readiness_model.manual_positioning_assumption,
                    " ".join(readiness_model.recommended_setup),
                    readiness_model.focus_requirement,
                    readiness_model.cursor_requirement or "",
                    readiness_model.readiness_wording,
                    " ".join(readiness_model.confidence_notes),
                    " ".join(readiness_model.contextual_warnings),
                    " ".join(readiness_model.blocked_or_refused_conditions),
                )
            )

            for forbidden_word in FORBIDDEN_CERTAINTY_WORDS:
                self.assertNotIn(forbidden_word, all_wording)

            self.assertTrue(
                any(
                    allowed_word in all_wording
                    for allowed_word in (
                        "Expected",
                        "Assumed",
                        "Recommended",
                        "validated",
                    )
                )
            )

    def test_readiness_models_are_assumption_based(self) -> None:
        auto2_readiness = get_readiness_model("auto2")
        auto3_readiness = get_readiness_model("auto3")

        self.assertIn("assumption-based", auto2_readiness.confidence_notes[1])
        self.assertIn(
            "not automatic game-state verification",
            auto3_readiness.confidence_notes[1],
        )

    def test_readiness_layer_has_no_execution_controls(self) -> None:
        readiness_model = get_readiness_model("auto3")

        self.assertFalse(hasattr(readiness_model, "run"))
        self.assertFalse(hasattr(readiness_model, "execute"))
        self.assertFalse(hasattr(readiness_model, "timings"))


if __name__ == "__main__":
    unittest.main()
