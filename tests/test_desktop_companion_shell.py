import unittest

from desktop.companion_shell import (
    AUTO1_RACE_DURATION_MAX_SECONDS,
    AUTO1_RACE_DURATION_MIN_SECONDS,
    DEFAULT_FH6_TARGET_TITLE,
    _build_commitment_readiness_details,
    _build_auto1_ui_execution_profile,
    _completion_state_id_for_auto1_status,
    _desktop_execution_confirmation_summary,
    _desktop_execution_refusal_details,
    _format_ui_focus_failure_message,
    _format_auto1_race_duration_for_display,
    _is_desktop_execution_supported,
    _is_real_auto1_execution_state,
    _parse_auto1_race_duration_override,
    _request_auto1_ui_stop,
    _should_show_auto1_runtime_adjustment,
    _summarize_auto1_ui_execution_error,
    build_desktop_app_spec,
)
from core.stop import StopManager
from integrations.windows_focus_handoff import (
    FocusHandoffResult,
    FocusHandoffStatus,
    WindowCandidate,
)
from ui.automation_environment import AutomationEnvironmentSectionId
from ui.shell import ScreenId, SidebarDestinationId, ZoneRole


class DesktopCompanionShellTest(unittest.TestCase):
    def setUp(self) -> None:
        self.shell_spec = build_desktop_app_spec()

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
            "FH6 Farm Tool",
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

    def test_execution_wiring_is_auto1_only_and_fails_closed(self) -> None:
        execution_wiring = self.shell_spec.execution_wiring

        self.assertEqual(("auto1",), execution_wiring.enabled_automation_ids)
        self.assertEqual(("auto2", "auto3"), execution_wiring.refused_automation_ids)
        self.assertTrue(execution_wiring.uses_existing_guarded_auto1_path)
        self.assertTrue(execution_wiring.preserves_f8_stop)
        self.assertTrue(execution_wiring.fail_closed_for_unsupported_automations)
        self.assertEqual("Forza Horizon 6", DEFAULT_FH6_TARGET_TITLE)

    def test_auto1_race_duration_override_is_single_bounded_basic_runtime_value(self) -> None:
        self.assertEqual(5.0, AUTO1_RACE_DURATION_MIN_SECONDS)
        self.assertEqual(180.0, AUTO1_RACE_DURATION_MAX_SECONDS)
        self.assertEqual(40.0, _parse_auto1_race_duration_override("40.0"))
        self.assertEqual("40.0 seconds", _format_auto1_race_duration_for_display("40.0"))

        with self.assertRaises(ValueError):
            _parse_auto1_race_duration_override("4.9")

        with self.assertRaises(ValueError):
            _parse_auto1_race_duration_override("180.1")

        with self.assertRaises(ValueError):
            _parse_auto1_race_duration_override("not-a-number")

    def test_auto1_runtime_adjustment_is_visible_only_for_auto1(self) -> None:
        self.assertTrue(_should_show_auto1_runtime_adjustment("auto1"))
        self.assertFalse(_should_show_auto1_runtime_adjustment("auto2"))
        self.assertFalse(_should_show_auto1_runtime_adjustment("auto3"))

    def test_desktop_execution_support_is_auto1_only(self) -> None:
        self.assertTrue(_is_desktop_execution_supported("auto1"))
        self.assertFalse(_is_desktop_execution_supported("auto2"))
        self.assertFalse(_is_desktop_execution_supported("auto3"))
        self.assertFalse(_is_desktop_execution_supported("auto4"))
        self.assertFalse(_is_desktop_execution_supported("unknown"))

    def test_auto2_desktop_refusal_mentions_guarded_confirmations(self) -> None:
        details = " ".join(_desktop_execution_refusal_details("auto2"))
        summary = _desktop_execution_confirmation_summary("auto2")

        self.assertIn("Auto2 desktop execution is not wired", details)
        self.assertIn("test-mode navigation", details)
        self.assertIn("one-car purchase validation", details)
        self.assertIn("real-input and purchase confirmations", details)
        self.assertIn("guarded manual confirmations", summary)

    def test_auto3_desktop_refusal_mentions_guarded_confirmations(self) -> None:
        details = " ".join(_desktop_execution_refusal_details("auto3"))
        summary = _desktop_execution_confirmation_summary("auto3")

        self.assertIn("Auto3 desktop execution is not wired", details)
        self.assertIn("test-mode traversal", details)
        self.assertIn("bounded unlock validation", details)
        self.assertIn("real-input and unlock confirmations", details)
        self.assertIn("guarded manual confirmations", summary)

    def test_unknown_desktop_execution_refuses_without_enabling_real_input(self) -> None:
        details = " ".join(_desktop_execution_refusal_details("auto4"))
        summary = _desktop_execution_confirmation_summary("auto4")

        self.assertIn("Desktop execution is not available", details)
        self.assertIn("No operation will start", details)
        self.assertIn("Execution is unavailable", summary)

    def test_auto1_commitment_readiness_includes_runtime_focus_stop_and_baseline(self) -> None:
        details = _build_commitment_readiness_details(
            {
                "automation_id": "auto1",
                "race_duration_seconds": "55.0",
            }
        )

        joined = " ".join(details)
        self.assertIn("Auto1 selected", joined)
        self.assertIn("Race drive duration: 55.0 seconds", joined)
        self.assertIn("Expected baseline", joined)
        self.assertIn("F8 emergency stop", joined)

    def test_auto1_commitment_readiness_refuses_invalid_runtime_value(self) -> None:
        with self.assertRaises(ValueError):
            _build_commitment_readiness_details(
                {
                    "automation_id": "auto1",
                    "race_duration_seconds": "invalid",
                }
            )

    def test_non_auto1_commitment_readiness_remains_refused(self) -> None:
        details = _build_commitment_readiness_details(
            {
                "automation_id": "auto2",
                "race_duration_seconds": "55.0",
            }
        )

        joined = " ".join(details)
        self.assertIn("Only Auto1 can execute", joined)
        self.assertIn("Auto2 and Auto3 remain refused", joined)

    def test_auto1_ui_execution_profile_overrides_only_race_duration(self) -> None:
        profile = _build_auto1_ui_execution_profile(
            {"race_duration_seconds": "55.0"}
        )

        self.assertEqual(55.0, profile["timings"]["race_duration"])
        self.assertEqual(5.0, profile["timings"]["startup_delay"])
        self.assertEqual(2.0, profile["timings"]["wait_after_restart"])
        self.assertEqual(10.0, profile["timings"]["wait_after_first_confirm"])
        self.assertEqual(3.0, profile["timings"]["post_cycle_delay"])

    def test_auto1_execution_status_mapping_fails_closed(self) -> None:
        self.assertEqual("completed", _completion_state_id_for_auto1_status("completed"))
        self.assertEqual("stopped", _completion_state_id_for_auto1_status("stopped"))
        self.assertEqual("refused", _completion_state_id_for_auto1_status("failed"))
        self.assertEqual("refused", _completion_state_id_for_auto1_status("unknown"))

    def test_real_auto1_execution_state_is_explicit(self) -> None:
        self.assertTrue(
            _is_real_auto1_execution_state(
                {"automation_id": "auto1", "execution_active": "true"}
            )
        )
        self.assertFalse(
            _is_real_auto1_execution_state(
                {"automation_id": "auto1", "execution_active": "false"}
            )
        )
        self.assertFalse(
            _is_real_auto1_execution_state(
                {"automation_id": "auto2", "execution_active": "true"}
            )
        )

    def test_ui_stop_request_uses_stop_manager_for_active_auto1(self) -> None:
        stop_manager = StopManager()

        message = _request_auto1_ui_stop(
            stop_manager,
            {"automation_id": "auto1", "execution_active": "true"},
        )

        self.assertTrue(stop_manager.should_stop())
        self.assertIn("Stop requested", message)
        self.assertIn("guarded Auto1 cleanup", message)

    def test_ui_stop_request_refuses_without_active_auto1(self) -> None:
        stop_manager = StopManager()

        message = _request_auto1_ui_stop(
            stop_manager,
            {"automation_id": "auto2", "execution_active": "true"},
        )

        self.assertFalse(stop_manager.should_stop())
        self.assertIn("No active Auto1", message)

    def test_ui_stop_request_refuses_when_execution_flag_is_missing(self) -> None:
        stop_manager = StopManager()

        message = _request_auto1_ui_stop(
            stop_manager,
            {"automation_id": "auto1"},
        )

        self.assertFalse(stop_manager.should_stop())
        self.assertIn("No active Auto1", message)

    def test_auto1_execution_error_summary_includes_exact_exception_context(self) -> None:
        summary = _summarize_auto1_ui_execution_error(
            RuntimeError("real input dependency unavailable")
        )

        self.assertIn("Auto1 manual run unavailable", summary)
        self.assertIn("RuntimeError", summary)
        self.assertIn("real input dependency unavailable", summary)

    def test_focus_failure_message_exposes_target_active_status_and_attempts(self) -> None:
        message = _format_ui_focus_failure_message(
            FocusHandoffResult(
                status=FocusHandoffStatus.FOCUS_FAILED,
                message="Focus handoff was attempted, but success could not be confirmed.",
                selected_candidate=WindowCandidate(handle=2, title="Forza Horizon 6"),
                active_candidate=WindowCandidate(handle=9, title="Browser"),
                confirmation_attempts=4,
                focus_attempted=True,
            )
        )

        self.assertIn("Forza Horizon 6", message)
        self.assertIn("Browser", message)
        self.assertIn("focus_failed", message)
        self.assertIn("Confirmation attempts: 4", message)

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
