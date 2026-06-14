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
        self.assertEqual(230, navigation_rail.expanded_width)
        self.assertEqual("hover", navigation_rail.expansion_trigger)

    def test_navigation_rail_visual_refinement_is_restrained(self) -> None:
        navigation_rail = self.shell_spec.navigation_rail

        self.assertEqual(42, navigation_rail.item_height)
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
            self.assertEqual(3, len(screen.zones))

    def test_smoke_spec_does_not_require_gui_launch(self) -> None:
        self.assertEqual(
            "FH6 Farm Tool - PySide6 Shell Prototype",
            self.shell_spec.window_title,
        )
        self.assertEqual(5, len(self.shell_spec.screens))
        self.assertEqual(63, self.shell_spec.top_bar.height)
        self.assertTrue(self.shell_spec.top_bar.reserves_identity_space)

    def test_prototype_window_is_vertical_companion_and_fixed(self) -> None:
        self.assertEqual(640, self.shell_spec.window_width)
        self.assertEqual(864, self.shell_spec.window_height)
        self.assertLess(self.shell_spec.window_width, self.shell_spec.window_height)
        self.assertTrue(self.shell_spec.is_fixed_size)

    def test_companion_mode_represents_running_supervision_without_execution(self) -> None:
        companion_mode = self.shell_spec.companion_mode

        self.assertEqual("Companion Mode", companion_mode.title)
        self.assertIn("Supervise", companion_mode.primary_intention)
        self.assertEqual("Running", companion_mode.status_label)
        self.assertEqual("Supervised operation", companion_mode.operation_label)
        self.assertEqual("FH6 focus handoff ready", companion_mode.focus_label)
        self.assertEqual("F8 emergency stop available", companion_mode.stop_label)
        self.assertTrue(companion_mode.is_simpler_than_automation_environment)
        self.assertFalse(companion_mode.introduces_execution)

    def test_commitment_layer_is_last_safe_checkpoint_without_execution(self) -> None:
        commitment = self.shell_spec.commitment_layer

        self.assertEqual("Commit to Supervision", commitment.title)
        self.assertIn("Confirm readiness", commitment.primary_intention)
        self.assertEqual((3, 2, 1), commitment.countdown_values)
        self.assertLess(len(commitment.countdown_values), 4)
        self.assertTrue(commitment.is_last_safe_exit)
        self.assertFalse(commitment.introduces_execution)
        self.assertIn("FH6 focus handoff", commitment.focus_label)
        self.assertIn("F8", commitment.stop_label)

    def test_completion_lifecycle_represents_calm_post_run_outcomes(self) -> None:
        completion = self.shell_spec.completion_lifecycle
        state_ids = tuple(state.state_id for state in completion.states)

        self.assertEqual("Post-Run State", completion.title)
        self.assertIn("Conclude calmly", completion.primary_intention)
        self.assertEqual(("completed", "stopped", "refused"), state_ids)
        self.assertTrue(completion.always_returns_to_preparation)
        self.assertFalse(completion.introduces_execution)

    def test_completion_states_keep_stop_and_refusal_trust_first(self) -> None:
        states_by_id = {
            state.state_id: state for state in self.shell_spec.completion_lifecycle.states
        }

        self.assertEqual("Run completed", states_by_id["completed"].title)
        self.assertEqual("Stopped safely", states_by_id["stopped"].title)
        self.assertIn("not a failure", states_by_id["stopped"].reassurance)
        self.assertEqual("Operation paused", states_by_id["refused"].title)
        self.assertIn("trust-first", states_by_id["refused"].reassurance)
        for state in states_by_id.values():
            self.assertNotIn("panic", state.emotional_treatment.lower())
            self.assertNotIn("crash", state.emotional_treatment.lower())

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

    def test_visual_composition_moves_beyond_default_widgets(self) -> None:
        visual_composition = self.shell_spec.visual_composition

        self.assertTrue(visual_composition.uses_custom_cards)
        self.assertEqual(
            "dark quiet launch surface",
            visual_composition.home_hero_treatment,
        )
        self.assertEqual(
            "layered dark utility card",
            visual_composition.card_treatment,
        )
        self.assertEqual(
            "recessed contextual support",
            visual_composition.secondary_treatment,
        )
        self.assertEqual(
            "restrained pink commitment",
            visual_composition.commitment_treatment,
        )
        self.assertEqual(
            "brief-aligned graphite companion surface",
            visual_composition.composition_principle,
        )
        self.assertEqual("dark companion canvas", visual_composition.background_treatment)
        self.assertEqual(
            "ordered launch surface with dominant recommended action",
            visual_composition.home_layout_treatment,
        )
        self.assertEqual(
            "preparation flow with deliberate commitment",
            visual_composition.automation_layout_treatment,
        )

    def test_home_concept_is_single_frame_and_not_dashboard_like(self) -> None:
        home = self.shell_spec.home_concept

        self.assertTrue(home.is_single_frame)
        self.assertFalse(home.is_dashboard_like)
        self.assertIn("baseline", home.philosophy_statement)
        self.assertIn("supervised", home.opening_feel)
        self.assertEqual("recommended next step first", home.composition_principle)
        self.assertEqual("Prepare a Run", home.primary_action_label)

    def test_home_concept_preserves_restrained_signal_set(self) -> None:
        signal_titles = tuple(signal.title for signal in self.shell_spec.home_concept.signals)
        signal_roles = tuple(signal.zone_role for signal in self.shell_spec.home_concept.signals)

        self.assertEqual(
            (
                "RECOMMENDED NEXT STEP",
                "REVIEW & PLAN",
                "RECENT CONTEXT",
                "QUIET STATUS",
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
        self.assertEqual(
            "Orient, confirm, then commit.",
            self.shell_spec.automation_environment.primary_intention,
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

    def test_automation_environment_readability_treatments_reduce_equal_weight(self) -> None:
        sections_by_id = {
            section.section_id: section
            for section in self.shell_spec.automation_environment.sections
        }

        self.assertEqual(
            "primary orientation",
            sections_by_id[
                AutomationEnvironmentSectionId.OVERVIEW
            ].readability_treatment,
        )
        self.assertEqual(
            "primary confidence check",
            sections_by_id[
                AutomationEnvironmentSectionId.READINESS
            ].readability_treatment,
        )
        self.assertEqual(
            "secondary contextual support",
            sections_by_id[
                AutomationEnvironmentSectionId.CONTEXTUAL_WARNINGS
            ].readability_treatment,
        )
        self.assertEqual(
            "tertiary collapsed refinement",
            sections_by_id[
                AutomationEnvironmentSectionId.ADVANCED
            ].readability_treatment,
        )

    def test_automation_environment_keeps_details_digestible(self) -> None:
        sections_by_id = {
            section.section_id: section
            for section in self.shell_spec.automation_environment.sections
        }

        self.assertLessEqual(
            len(sections_by_id[AutomationEnvironmentSectionId.OVERVIEW].details),
            2,
        )
        self.assertLessEqual(
            len(sections_by_id[AutomationEnvironmentSectionId.PROFILE].details),
            2,
        )
        self.assertLessEqual(
            len(sections_by_id[AutomationEnvironmentSectionId.READINESS].details),
            3,
        )
        self.assertLessEqual(
            len(sections_by_id[AutomationEnvironmentSectionId.RUN].details),
            2,
        )


if __name__ == "__main__":
    unittest.main()
