import unittest
from dataclasses import replace

from product.automation_definition import AutomationDefinition
from product.automation_registry import get_all_automation_definitions
from product.profile_metadata import PackageTier, RecommendationStatus
from product.profile_metadata_registry import get_all_profile_metadata
from product.risk_levels import RiskLevel
from ui.profiles_screen import (
    ProfileSectionId,
    ProfileSelectionAvailability,
    build_profiles_screen,
)


class ProfilesScreenStructureTest(unittest.TestCase):
    def setUp(self) -> None:
        self.profile_metadata = tuple(get_all_profile_metadata())
        self.automation_definitions = tuple(get_all_automation_definitions())
        self.screen = build_profiles_screen(
            profile_metadata=self.profile_metadata,
            automation_definitions=self.automation_definitions,
        )

    def test_recommended_profiles_appear_first(self) -> None:
        self.assertEqual(
            ProfileSectionId.RECOMMENDED,
            self.screen.recommended_profiles.section_id,
        )
        self.assertEqual(
            ProfileSectionId.ALTERNATIVE,
            self.screen.alternative_profiles.section_id,
        )
        self.assertEqual(ProfileSectionId.CUSTOM, self.screen.custom_profiles.section_id)

    def test_alternatives_are_secondary(self) -> None:
        self.assertIn("Secondary", self.screen.alternative_profiles.purpose)

    def test_custom_section_exists_but_is_tertiary(self) -> None:
        self.assertTrue(self.screen.custom_profiles.is_tertiary)
        self.assertIn("custom", self.screen.custom_profiles.purpose.lower())

    def test_curated_profiles_are_prioritized(self) -> None:
        recommended_statuses = {
            profile.recommendation_status
            for profile in self.screen.recommended_profiles.profiles
        }

        self.assertEqual({RecommendationStatus.CURATED}, recommended_statuses)
        self.assertGreaterEqual(len(self.screen.recommended_profiles.profiles), 3)

    def test_future_inactive_restricted_profile_states_are_supported(self) -> None:
        restricted_metadata = replace(
            self.profile_metadata[0],
            profile_id="restricted_plus_profile",
            profile_name="Restricted Plus Profile",
            package_tier=PackageTier.PLUS,
            recommendation_status=RecommendationStatus.SUPPORTED,
        )
        screen = build_profiles_screen(
            profile_metadata=self.profile_metadata + (restricted_metadata,),
            automation_definitions=self.automation_definitions,
        )
        restricted_profile = next(
            profile
            for profile in screen.alternative_profiles.profiles
            if profile.profile_id == "restricted_plus_profile"
        )

        self.assertEqual(
            ProfileSelectionAvailability.RESTRICTED,
            restricted_profile.availability,
        )
        self.assertFalse(restricted_profile.is_selectable)

        future_metadata = replace(
            self.profile_metadata[0],
            profile_id="future_auto4_profile",
            profile_name="Future Auto4 Profile",
            package_tier=PackageTier.PLUS,
            recommendation_status=RecommendationStatus.SUPPORTED,
        )
        future_automation = AutomationDefinition(
            automation_id="auto4",
            display_name="Auto4",
            short_purpose="Future automation.",
            long_purpose="Future automation.",
            risk_level=RiskLevel.HIGH,
            validated_scope="Not active.",
            expected_baseline="Unavailable.",
            available_profiles=["future_auto4_profile"],
            is_active=False,
        )
        future_screen = build_profiles_screen(
            profile_metadata=(future_metadata,),
            automation_definitions=(future_automation,),
        )
        future_profile = future_screen.alternative_profiles.profiles[0]

        self.assertEqual(
            ProfileSelectionAvailability.FUTURE,
            future_profile.availability,
        )
        self.assertFalse(future_profile.is_selectable)

    def test_custom_profiles_are_supported_without_encouraging_them(self) -> None:
        custom_metadata = replace(
            self.profile_metadata[0],
            profile_id="auto1_custom_safe",
            profile_name="Auto1 Custom Safe",
            recommendation_status=RecommendationStatus.CUSTOM,
        )
        screen = build_profiles_screen(
            profile_metadata=self.profile_metadata + (custom_metadata,),
            automation_definitions=self.automation_definitions,
        )

        self.assertEqual(1, len(screen.custom_profiles.profiles))
        self.assertEqual(
            "auto1_custom_safe",
            screen.custom_profiles.profiles[0].profile_id,
        )

    def test_no_raw_timing_or_settings_data_is_exposed(self) -> None:
        all_profiles = (
            self.screen.recommended_profiles.profiles
            + self.screen.alternative_profiles.profiles
            + self.screen.custom_profiles.profiles
        )

        for profile in all_profiles:
            serialized_values = " ".join(str(value) for value in profile.__dict__.values())
            self.assertNotIn("wait_after", serialized_values)
            self.assertNotIn("menu_key_delay", serialized_values)
            self.assertNotIn("timings", serialized_values)
            self.assertNotIn("settings", serialized_values)

    def test_screen_has_one_primary_intention(self) -> None:
        self.assertEqual(
            "Choose trusted execution behavior.",
            self.screen.primary_intention,
        )


if __name__ == "__main__":
    unittest.main()
