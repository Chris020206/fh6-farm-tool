import unittest

from desktop.pyside6_shell_prototype import build_prototype_shell_spec
from ui.automation_environment import AutomationEnvironmentSectionId
from ui.shell import ScreenId, SidebarDestinationId, ZoneRole


class PySide6ShellPrototypeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.shell_spec = build_prototype_shell_spec()

    def test_sidebar_maps_to_stable_destinations(self) -> None:
        destination_ids = tuple(
            destination.destination_id
            for destination in self.shell_spec.sidebar_destinations
        )

        self.assertEqual(
            (
                SidebarDestinationId.HOME,
                SidebarDestinationId.PROFILES,
                SidebarDestinationId.HISTORY,
                SidebarDestinationId.HELP,
                SidebarDestinationId.SETTINGS,
            ),
            destination_ids,
        )

    def test_placeholder_screens_match_sidebar_destinations(self) -> None:
        sidebar_screen_ids = tuple(
            destination.screen_id
            for destination in self.shell_spec.sidebar_destinations
        )
        prototype_screen_ids = tuple(
            screen.screen_id
            for screen in self.shell_spec.screens
        )

        self.assertEqual(sidebar_screen_ids, prototype_screen_ids)
        self.assertNotIn(ScreenId.AUTOMATION_ENVIRONMENT, prototype_screen_ids)

    def test_weighted_zones_are_represented_for_each_screen(self) -> None:
        for screen in self.shell_spec.screens:
            zone_roles = tuple(zone.role for zone in screen.zones)

            self.assertEqual(
                (
                    ZoneRole.PRIMARY,
                    ZoneRole.SECONDARY,
                    ZoneRole.TERTIARY,
                ),
                zone_roles,
            )

    def test_smoke_spec_does_not_require_gui_launch(self) -> None:
        self.assertEqual(
            "FH6 Farm Tool - PySide6 Shell Prototype",
            self.shell_spec.window_title,
        )
        self.assertEqual(5, len(self.shell_spec.screens))

    def test_automation_environment_renders_six_section_structure(self) -> None:
        section_ids = tuple(
            section.section_id
            for section in self.shell_spec.automation_environment.sections
        )

        self.assertEqual(
            (
                AutomationEnvironmentSectionId.OVERVIEW,
                AutomationEnvironmentSectionId.PROFILE,
                AutomationEnvironmentSectionId.READINESS,
                AutomationEnvironmentSectionId.CONTEXTUAL_WARNINGS,
                AutomationEnvironmentSectionId.ADVANCED,
                AutomationEnvironmentSectionId.RUN,
            ),
            section_ids,
        )

    def test_automation_environment_represents_weighted_zones(self) -> None:
        sections_by_id = {
            section.section_id: section
            for section in self.shell_spec.automation_environment.sections
        }

        self.assertEqual(
            ZoneRole.PRIMARY,
            sections_by_id[AutomationEnvironmentSectionId.OVERVIEW].zone_role,
        )
        self.assertEqual(
            ZoneRole.SECONDARY,
            sections_by_id[
                AutomationEnvironmentSectionId.CONTEXTUAL_WARNINGS
            ].zone_role,
        )
        self.assertEqual(
            ZoneRole.TERTIARY,
            sections_by_id[AutomationEnvironmentSectionId.ADVANCED].zone_role,
        )

    def test_automation_environment_keeps_advanced_secondary_and_run_deliberate(self) -> None:
        sections_by_id = {
            section.section_id: section
            for section in self.shell_spec.automation_environment.sections
        }
        advanced = sections_by_id[AutomationEnvironmentSectionId.ADVANCED]
        run = sections_by_id[AutomationEnvironmentSectionId.RUN]

        self.assertTrue(advanced.is_collapsed_feeling)
        self.assertIn("Run plan is prepared", run.summary)
        self.assertNotIn("execute", run.summary.lower())
        self.assertNotIn("start automation", run.summary.lower())


if __name__ == "__main__":
    unittest.main()
