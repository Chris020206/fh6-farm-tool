import copy
import unittest
from pathlib import Path

from product.profile_metadata import (
    PackageTier,
    RecommendationStatus,
    ValidationConfidence,
)
from product.profile_metadata_registry import (
    PROFILE_METADATA,
    get_profile_metadata,
    get_profile_metadata_for_automation,
)
from profiles.profile_manager import ProfileManager


class ProfileMetadataLayerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.profile_manager = ProfileManager(Path("profiles"))

    def test_official_profiles_have_metadata(self) -> None:
        official_profile_ids = {
            profile_data["profile_id"]
            for profile_data in self.profile_manager.load_official_profiles()
            if profile_data["profile_type"]
            in {"auto1_race", "auto2_buy_car", "auto3_skill_tree"}
        }

        self.assertEqual(
            {
                "auto1_race_default",
                "auto2_buy_car_default",
                "auto3_skill_tree_default",
            },
            official_profile_ids,
        )
        self.assertTrue(official_profile_ids.issubset(PROFILE_METADATA.keys()))

    def test_metadata_uses_product_facing_profile_language(self) -> None:
        metadata = get_profile_metadata("auto3_skill_tree_default")

        self.assertEqual(RecommendationStatus.CURATED, metadata.recommendation_status)
        self.assertEqual(PackageTier.BASIC, metadata.package_tier)
        self.assertEqual(ValidationConfidence.VALIDATED, metadata.validation_confidence)
        self.assertIn("Guarded skill-tree unlock", metadata.behavior_summary)
        self.assertNotIn("wait_after_get_in_next_car", metadata.behavior_summary)
        self.assertNotIn("12.0", metadata.behavior_summary)

    def test_timing_values_remain_execution_profile_data_only(self) -> None:
        profile_data = self.profile_manager.load_profile(
            Path("profiles/official/auto1_race_default.json")
        )
        original_profile_data = copy.deepcopy(profile_data)

        metadata = get_profile_metadata("auto1_race_default")

        self.assertEqual(original_profile_data, profile_data)
        self.assertIn("timings", profile_data)
        self.assertNotIn("timings", metadata.__dict__)
        self.assertIn("timings", metadata.hidden_technical_sections)

    def test_metadata_can_be_filtered_by_automation_type(self) -> None:
        auto2_metadata = get_profile_metadata_for_automation("auto2_buy_car")

        self.assertEqual(1, len(auto2_metadata))
        self.assertEqual("auto2_buy_car_default", auto2_metadata[0].profile_id)

    def test_official_metadata_does_not_encourage_direct_editing(self) -> None:
        for metadata in PROFILE_METADATA.values():
            self.assertEqual((), metadata.editable_fields)
            self.assertIn("Official read-only baseline", metadata.customization_status)


if __name__ == "__main__":
    unittest.main()
