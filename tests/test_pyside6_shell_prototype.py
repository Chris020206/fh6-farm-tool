import unittest

from desktop.pyside6_shell_prototype import build_prototype_shell_spec
from desktop.pyside6_shell_prototype import PrototypeNavigationRailMode
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

    def test_sidebar_composition_is_compact_and_closed(self) -> None:
        sidebar = self.shell_spec.sidebar_composition

        self.assertTrue(sidebar.is_compact_navigation)
        self.assertTrue(sidebar.has_structural_closure)
        self.assertEqual("FH6 Farm Tool", sidebar.navigation_block_label)
        self.assertEqual("Controlled MVP", sidebar.footer_status)
        self.assertEqual("Manual operation ready", sidebar.footer_detail)

    def test_navigation_rail_is_miniature_and_toggle_first(self) -> None:
        navigation_rail = self.shell_spec.navigation_rail

        self.assertTrue(navigation_rail.is_miniature)
        self.assertTrue(navigation_rail.is_low_emphasis)
        self.assertEqual(72, navigation_rail.collapsed_width)
        self.assertEqual(168, navigation_rail.expanded_width)
        self.assertEqual(
            PrototypeNavigationRailMode.TOGGLE,
            navigation_rail.default_mode,
        )
        self.assertEqual(
            (
                PrototypeNavigationRailMode.TOGGLE,
                PrototypeNavigationRailMode.HOVER,
            ),
            navigation_rail.supported_modes,
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

    def test_prototype_window_is_vertical_companion_and_fixed(self) -> None:
        self.assertEqual(640, self.shell_spec.window_width)
        self.assertEqual(768, self.shell_spec.window_height)
        self.assertLess(self.shell_spec.window_width, self.shell_spec.window_height)
        self.assertTrue(self.shell_spec.is_fixed_size)

    def test_home_concept_is_single_frame_and_not_dashboard_like(self) -> None:
        home = self.shell_spec.home_concept

        self.assertTrue(home.is_single_frame)
        self.assertFalse(home.is_dashboard_like)
        self.assertIn("Quiet confidence", home.philosophy_statement)
        self.assertIn("launchpad", home.opening_feel)

    def test_home_concept_preserves_restrained_signal_set(self) -> None:
        signal_titles = tuple(signal.title for signal in self.shell_spec.home_concept.signals)
        signal_roles = tuple(signal.zone_role for signal in self.shell_spec.home_concept.signals)

        self.assertEqual(
            (
                "Recommended Next Step",
                "Quick Automation Access",
                "Relevant Activity",
                "Quiet Status",
            ),
            signal_titles,
        )
        self.assertEqual(
            (
                ZoneRole.PRIMARY,
                ZoneRole.PRIMARY,
                ZoneRole.SECONDARY,
                ZoneRole.TERTIARY,
            ),
            signal_roles,
        )

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
