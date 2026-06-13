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

    def test_sidebar_composition_is_compact_and_closed(self) -> None:
        sidebar = self.shell_spec.sidebar_composition

        self.assertTrue(sidebar.is_compact_navigation)
        self.assertTrue(sidebar.has_structural_closure)
        self.assertEqual("FH6 Farm Tool", sidebar.navigation_block_label)
        self.assertEqual("Controlled MVP", sidebar.footer_status)
        self.assertEqual("Manual operation ready", sidebar.footer_detail)

    def test_navigation_rail_is_hover_overlay_only(self) -> None:
        navigation_rail = self.shell_spec.navigation_rail

        self.assertTrue(navigation_rail.is_miniature)
        self.assertTrue(navigation_rail.is_low_emphasis)
        self.assertEqual(64, navigation_rail.collapsed_width)
        self.assertEqual(184, navigation_rail.expanded_width)
        self.assertEqual("hover", navigation_rail.expansion_trigger)

    def test_navigation_rail_visual_refinement_is_restrained(self) -> None:
        navigation_rail = self.shell_spec.navigation_rail

        self.assertEqual(34, navigation_rail.item_height)
        self.assertEqual(8, navigation_rail.item_spacing)
        self.assertEqual(
            "soft filled selection with clear contrast",
            navigation_rail.active_state_treatment,
        )
        self.assertEqual(
            "quiet floating panel with restrained hierarchy",
            navigation_rail.overlay_treatment,
        )
        self.assertEqual(
            "low-emphasis operational status",
            navigation_rail.footer_treatment,
        )

    def test_navigation_rail_reserves_space_and_overlays_without_reflow(self) -> None:
        navigation_rail = self.shell_spec.navigation_rail

        self.assertTrue(navigation_rail.reserves_collapsed_space)
        self.assertTrue(navigation_rail.overlays_main_content)
        self.assertFalse(navigation_rail.reflows_main_content_on_hover)
        self.assertGreaterEqual(navigation_rail.animation_duration_ms, 180)
        self.assertLessEqual(navigation_rail.animation_duration_ms, 220)
        self.assertLess(navigation_rail.animation_duration_ms, 1000)

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

    def test_vertical_rhythm_supports_digestible_single_frame_layout(self) -> None:
        rhythm = self.shell_spec.vertical_rhythm

        self.assertEqual(18, rhythm.content_margin)
        self.assertEqual(8, rhythm.header_spacing)
        self.assertEqual(14, rhythm.section_spacing)
        self.assertEqual(10, rhythm.group_spacing)
        self.assertEqual(10, rhythm.group_inner_margin)
        self.assertEqual(16, rhythm.important_element_spacing)
        self.assertTrue(rhythm.is_single_frame)
        self.assertFalse(rhythm.introduces_scrolling)
        self.assertEqual("restrained but not empty", rhythm.density_principle)

    def test_typography_hierarchy_supports_scan_first_reading(self) -> None:
        typography = self.shell_spec.typography

        self.assertEqual(20, typography.screen_title_size)
        self.assertEqual(13, typography.opening_statement_size)
        self.assertEqual(13, typography.section_title_size)
        self.assertEqual(12, typography.summary_size)
        self.assertEqual(11, typography.detail_size)
        self.assertEqual(12, typography.navigation_size)
        self.assertEqual(10, typography.footer_size)
        self.assertEqual(600, typography.active_navigation_weight)
        self.assertGreater(typography.screen_title_size, typography.summary_size)
        self.assertGreater(typography.summary_size, typography.detail_size)
        self.assertEqual("muted supporting text", typography.secondary_detail_treatment)
        self.assertEqual("scan first, detail second", typography.hierarchy_principle)

    def test_home_concept_is_single_frame_and_not_dashboard_like(self) -> None:
        home = self.shell_spec.home_concept

        self.assertTrue(home.is_single_frame)
        self.assertFalse(home.is_dashboard_like)
        self.assertIn("Quiet confidence", home.philosophy_statement)
        self.assertIn("launchpad", home.opening_feel)
        self.assertEqual("recommended next step first", home.composition_principle)
        self.assertEqual("Prepare Automation", home.primary_action_label)

    def test_home_concept_preserves_restrained_signal_set(self) -> None:
        signal_titles = tuple(signal.title for signal in self.shell_spec.home_concept.signals)
        signal_roles = tuple(signal.zone_role for signal in self.shell_spec.home_concept.signals)

        self.assertEqual(
            (
                "Recommended Next Step",
                "Prepare A Run",
                "Recent Context",
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
