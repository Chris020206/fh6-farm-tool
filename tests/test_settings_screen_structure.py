import unittest

from ui.settings_screen import (
    SettingCategory,
    SettingImportance,
    SettingsSectionId,
    build_settings_screen,
)


class SettingsScreenStructureTest(unittest.TestCase):
    def setUp(self) -> None:
        self.screen = build_settings_screen()

    def test_expected_application_behavior_is_primary(self) -> None:
        section = self.screen.expected_application_behavior

        self.assertEqual(
            SettingsSectionId.EXPECTED_APPLICATION_BEHAVIOR,
            section.section_id,
        )
        self.assertTrue(section.is_primary)
        self.assertTrue(section.settings)
        self.assertTrue(
            all(setting.importance == SettingImportance.PRIMARY for setting in section.settings)
        )

    def test_safety_and_operational_preferences_are_secondary(self) -> None:
        section = self.screen.safety_and_operational_preferences

        self.assertEqual(
            SettingsSectionId.SAFETY_AND_OPERATIONAL_PREFERENCES,
            section.section_id,
        )
        self.assertTrue(section.is_secondary)
        self.assertTrue(
            all(setting.importance == SettingImportance.SECONDARY for setting in section.settings)
        )

    def test_advanced_system_preferences_are_tertiary(self) -> None:
        section = self.screen.advanced_system_preferences

        self.assertEqual(
            SettingsSectionId.ADVANCED_SYSTEM_PREFERENCES,
            section.section_id,
        )
        self.assertTrue(section.is_tertiary)
        self.assertTrue(
            all(setting.importance == SettingImportance.TERTIARY for setting in section.settings)
        )

    def test_settings_has_one_primary_intention(self) -> None:
        self.assertEqual(
            "Control application-level behavior without editing automation execution.",
            self.screen.primary_intention,
        )

    def test_settings_does_not_include_execution_timing_or_profile_behavior(self) -> None:
        all_settings = _all_settings(self.screen)
        serialized_values = " ".join(
            " ".join(
                (
                    setting.setting_id,
                    setting.label,
                    setting.description,
                    setting.category.value,
                )
            ).lower()
            for setting in all_settings
        )

        self.assertNotIn("timing", serialized_values)
        self.assertNotIn("wait_after", serialized_values)
        self.assertNotIn("menu_key_delay", serialized_values)
        self.assertNotIn("navigation", serialized_values)
        self.assertNotIn("profile editing", serialized_values)
        self.assertNotIn("execution tuning", serialized_values)

    def test_settings_does_not_duplicate_profiles_responsibility(self) -> None:
        all_settings = _all_settings(self.screen)
        setting_ids = {
            setting.setting_id
            for setting in all_settings
        }

        self.assertNotIn("profile_selection", setting_ids)
        self.assertNotIn("profile_editor", setting_ids)
        self.assertNotIn("custom_profile", setting_ids)

    def test_expected_app_settings_are_represented(self) -> None:
        categories = {
            setting.category
            for setting in self.screen.expected_application_behavior.settings
        }

        self.assertIn(SettingCategory.APPEARANCE, categories)
        self.assertIn(SettingCategory.NOTIFICATIONS, categories)
        self.assertIn(SettingCategory.STARTUP, categories)
        self.assertIn(SettingCategory.WINDOW, categories)

    def test_emergency_stop_and_confirmation_preferences_are_safety_settings(self) -> None:
        setting_ids = {
            setting.setting_id
            for setting in self.screen.safety_and_operational_preferences.settings
        }
        categories = {
            setting.category
            for setting in self.screen.safety_and_operational_preferences.settings
        }

        self.assertIn("emergency_stop_visibility", setting_ids)
        self.assertIn("confirmation_preferences", setting_ids)
        self.assertIn(SettingCategory.SAFETY, categories)
        self.assertIn(SettingCategory.CONFIRMATION, categories)

    def test_advanced_system_preferences_are_structurally_secondary(self) -> None:
        section = self.screen.advanced_system_preferences

        self.assertTrue(section.is_tertiary)
        self.assertIn("Tertiary", section.purpose)
        self.assertTrue(
            all(not setting.is_editable_now for setting in section.settings)
        )


def _all_settings(screen) -> tuple:
    return (
        screen.expected_application_behavior.settings
        + screen.safety_and_operational_preferences.settings
        + screen.advanced_system_preferences.settings
    )


if __name__ == "__main__":
    unittest.main()
