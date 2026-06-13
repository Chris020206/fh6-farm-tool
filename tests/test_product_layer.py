import unittest

from product.automation_registry import (
    AUTOMATION_DEFINITIONS,
    get_active_automation_definitions,
)
from product.product_states import ProductState
from product.risk_levels import RiskLevel


class ProductLayerTest(unittest.TestCase):
    def test_product_state_contains_expected_values(self) -> None:
        self.assertEqual("ready", ProductState.READY.value)
        self.assertEqual("running", ProductState.RUNNING.value)
        self.assertEqual("failure", ProductState.FAILURE.value)

    def test_risk_level_contains_controlled(self) -> None:
        self.assertEqual("controlled", RiskLevel.CONTROLLED.value)

    def test_auto4_is_not_active(self) -> None:
        self.assertFalse(AUTOMATION_DEFINITIONS["auto4"].is_active)

    def test_active_automations_exclude_auto4(self) -> None:
        automation_ids = {
            automation.automation_id
            for automation in get_active_automation_definitions()
        }

        self.assertIn("auto1", automation_ids)
        self.assertIn("auto2", automation_ids)
        self.assertIn("auto3", automation_ids)
        self.assertNotIn("auto4", automation_ids)


if __name__ == "__main__":
    unittest.main()
