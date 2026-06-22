import inspect
import unittest

from desktop.companion_shell import (
    AUTO1_LOOP_COUNT_MAX,
    AUTO1_LOOP_COUNT_MIN,
    AUTO1_RACE_DURATION_EXECUTION_BUFFER_SECONDS,
    AUTO1_RACE_DURATION_MAX_SECONDS,
    AUTO1_RACE_DURATION_MIN_SECONDS,
    DEFAULT_FH6_TARGET_TITLE,
    DESKTOP_BRAND_LOGO_MAX_HEIGHT,
    DESKTOP_BRAND_LOGO_MAX_WIDTH,
    DESKTOP_BRAND_LOGO_PATH,
    DESKTOP_APP_ICON_FALLBACK_PATH,
    DESKTOP_APP_ICON_PATH,
    DESKTOP_APP_USER_MODEL_ID,
    DESKTOP_APP_BUILD_TYPE,
    DESKTOP_APP_VERSION,
    DESKTOP_ABOUT_TITLE,
    DESKTOP_TRAY_ACTION_LABELS,
    DESKTOP_TRAY_TOOLTIP,
    NAVIGATION_ICON_SLOT_WIDTH,
    _baseline_preparation_content,
    _desktop_about_text,
    _desktop_app_icon_path,
    _desktop_baseline_details,
    _desktop_baseline_summary,
    _desktop_visible_version_text,
    _build_commitment_readiness_details,
    _build_commitment_layer_widget,
    _build_community_support_card,
    _build_automation_environment_widget,
    _build_home_screen_content,
    _build_history_screen_content,
    _build_help_screen_content,
    _build_auto1_ui_execution_profile,
    _completion_state_id_for_auto1_status,
    _commitment_readiness_content,
    _auto1_execution_race_duration,
    _desktop_execution_confirmation_summary,
    _desktop_execution_refusal_details,
    _format_ui_focus_failure_message,
    _format_auto1_loop_count_for_display,
    _format_auto1_race_duration_for_display,
    _has_specialized_desktop_screen_content,
    _is_desktop_preparation_available,
    _is_desktop_execution_supported,
    _is_real_auto1_execution_state,
    _parse_auto1_race_duration_override,
    _parse_auto1_loop_count,
    _parse_auto2_purchase_count,
    _request_auto1_ui_stop,
    _request_supervision_transition,
    _resource_spending_confirmation_for,
    _record_operational_history_entry,
    _session_status_for_completion_state,
    _should_show_auto1_runtime_adjustment,
    _should_show_community_feature_dialog,
    _summarize_auto1_ui_execution_error,
    _wrap_in_page_scroll_area,
    build_desktop_app_spec,
    launch_pyside6_shell_prototype,
)
from core.stop import StopManager
from licensing.models import EntitlementDecision
from sessions.session_status import SessionStatus
from settings.execution_preferences import ExecutionPreferences
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

    def test_desktop_history_does_not_construct_fake_session_data(self) -> None:
        source = inspect.getsource(_build_history_screen_content)

        self.assertNotIn("Desktop UI session is active", source)
        self.assertNotIn("No persisted run profile", source)
        self.assertNotIn("current-desktop-session", source)
        self.assertIn("history_entries_provider", source)

    def test_completed_run_appends_session_local_history_entry(self) -> None:
        entries = []

        entry = _record_operational_history_entry(
            entries,
            state_id="completed",
            companion_state={
                "automation_id": "auto1",
                "automation_name": "Auto1 - Race Automation",
                "profile_id": "auto1_race_default",
                "profile_name": "Auto1 Race Default",
                "requested_cycles": "3",
            },
            execution_message="Auto1 completed normally.",
            session_id="desktop-test-session",
        )

        self.assertEqual([entry], entries)
        self.assertEqual(SessionStatus.COMPLETED, entry.outcome)
        self.assertEqual((3, 3), (entry.requested_count, entry.completed_count))
        self.assertEqual(("Auto1 completed normally.",), entry.expandable_details)

    def test_stopped_and_refused_completion_states_map_honestly(self) -> None:
        self.assertEqual(
            SessionStatus.STOPPED,
            _session_status_for_completion_state("stopped"),
        )
        self.assertEqual(
            SessionStatus.REFUSED,
            _session_status_for_completion_state("refused"),
        )
        self.assertEqual(
            SessionStatus.INTERRUPTED,
            _session_status_for_completion_state("interrupted"),
        )
        self.assertEqual(
            SessionStatus.FAILURE,
            _session_status_for_completion_state("failure"),
        )

    def test_only_denied_community_decisions_show_edition_guidance(self) -> None:
        denied = EntitlementDecision(False, "Denied", "community", "test.feature")
        allowed = EntitlementDecision(True, "Allowed", "community", "test.feature")
        licensed_denied = EntitlementDecision(False, "Denied", "basic", "test.feature")

        self.assertTrue(_should_show_community_feature_dialog(denied))
        self.assertFalse(_should_show_community_feature_dialog(allowed))
        self.assertFalse(_should_show_community_feature_dialog(licensed_denied))

    def test_auto2_purchase_requires_resource_spending_confirmation(self) -> None:
        confirmation = _resource_spending_confirmation_for(
            {"automation_id": "auto2", "auto2_mode": "purchase"}
        )

        self.assertIsNotNone(confirmation)
        self.assertEqual("Auto2 Purchase Mode", confirmation.title)
        self.assertIn("spend in-game credits", confirmation.body)
        self.assertIn("Autoshow starting position", confirmation.body)

    def test_auto3_unlock_requires_resource_spending_confirmation(self) -> None:
        confirmation = _resource_spending_confirmation_for(
            {"automation_id": "auto3", "auto3_mode": "unlock"}
        )

        self.assertIsNotNone(confirmation)
        self.assertEqual("Auto3 Unlock Mode", confirmation.title)
        self.assertIn("spend in-game Skill Points", confirmation.body)
        self.assertIn("Subaru Impreza 22B-STI", confirmation.body)

    def test_auto2_confirmation_can_be_disabled(self) -> None:
        companion_state = {"automation_id": "auto2", "auto2_mode": "purchase"}
        confirmations = []
        opened_states = []

        transitioned = _request_supervision_transition(
            companion_state,
            confirm_resource_spending=lambda confirmation: (
                confirmations.append(confirmation) or False
            ),
            open_commitment_layer=opened_states.append,
            preferences=ExecutionPreferences(
                show_auto2_purchase_confirmation=False
            ),
        )

        self.assertTrue(transitioned)
        self.assertEqual([], confirmations)
        self.assertEqual([companion_state], opened_states)

    def test_auto3_confirmation_can_be_disabled(self) -> None:
        companion_state = {"automation_id": "auto3", "auto3_mode": "unlock"}
        confirmations = []
        opened_states = []

        transitioned = _request_supervision_transition(
            companion_state,
            confirm_resource_spending=lambda confirmation: (
                confirmations.append(confirmation) or False
            ),
            open_commitment_layer=opened_states.append,
            preferences=ExecutionPreferences(
                show_auto3_unlock_confirmation=False
            ),
        )

        self.assertTrue(transitioned)
        self.assertEqual([], confirmations)
        self.assertEqual([companion_state], opened_states)

    def test_auto2_navigation_test_does_not_require_confirmation(self) -> None:
        self.assertIsNone(
            _resource_spending_confirmation_for(
                {"automation_id": "auto2", "auto2_mode": "test"}
            )
        )

    def test_auto3_navigation_test_does_not_require_confirmation(self) -> None:
        self.assertIsNone(
            _resource_spending_confirmation_for(
                {"automation_id": "auto3", "auto3_mode": "test"}
            )
        )

    def test_auto1_does_not_require_resource_spending_confirmation(self) -> None:
        self.assertIsNone(
            _resource_spending_confirmation_for({"automation_id": "auto1"})
        )

    def test_resource_spending_cancel_keeps_preparation_state(self) -> None:
        companion_state = {"automation_id": "auto2", "auto2_mode": "purchase"}
        opened_states = []

        transitioned = _request_supervision_transition(
            companion_state,
            confirm_resource_spending=lambda _confirmation: False,
            open_commitment_layer=opened_states.append,
        )

        self.assertFalse(transitioned)
        self.assertEqual([], opened_states)
        self.assertEqual("purchase", companion_state["auto2_mode"])

    def test_resource_spending_continue_opens_commitment_checkpoint(self) -> None:
        companion_state = {"automation_id": "auto3", "auto3_mode": "unlock"}
        opened_states = []

        transitioned = _request_supervision_transition(
            companion_state,
            confirm_resource_spending=lambda _confirmation: True,
            open_commitment_layer=opened_states.append,
        )

        self.assertTrue(transitioned)
        self.assertEqual([companion_state], opened_states)

    def test_sidebar_maps_to_stable_destinations(self) -> None:
        destination_ids = tuple(
            destination.destination_id
            for destination in self.shell_spec.sidebar_destinations
        )

        self.assertEqual(
            (
                SidebarDestinationId.HOME,
                SidebarDestinationId.AUTOMATION_ENVIRONMENT,
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
        self.assertEqual("Forza Automation Assist", sidebar.navigation_block_label)
        self.assertEqual("", sidebar.footer_status)
        self.assertEqual("", sidebar.footer_detail)

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
        self.assertEqual(42, NAVIGATION_ICON_SLOT_WIDTH)
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

    def test_sidebar_screens_match_sidebar_destinations(self) -> None:
        sidebar_screen_ids = tuple(
            destination.screen_id
            for destination in self.shell_spec.sidebar_destinations
        )
        prototype_screen_ids = tuple(
            screen.screen_id
            for screen in self.shell_spec.screens
        )

        self.assertEqual(sidebar_screen_ids, prototype_screen_ids)
        self.assertEqual(1, prototype_screen_ids.count(ScreenId.AUTOMATION_ENVIRONMENT))

    def test_sidebar_reuses_existing_automation_environment_page(self) -> None:
        source = inspect.getsource(launch_pyside6_shell_prototype)

        self.assertIn("stack_index_by_screen_id", source)
        self.assertIn(
            "if screen.screen_id == ScreenId.AUTOMATION_ENVIRONMENT:",
            source,
        )
        self.assertEqual(1, source.count("_build_automation_environment_widget("))

    def test_sidebar_support_screens_have_real_desktop_content_paths(self) -> None:
        self.assertTrue(_has_specialized_desktop_screen_content(ScreenId.HOME))
        self.assertFalse(_has_specialized_desktop_screen_content(ScreenId.PROFILES))
        self.assertTrue(_has_specialized_desktop_screen_content(ScreenId.HISTORY))
        self.assertTrue(_has_specialized_desktop_screen_content(ScreenId.HELP))
        self.assertTrue(_has_specialized_desktop_screen_content(ScreenId.SETTINGS))
        self.assertFalse(
            _has_specialized_desktop_screen_content(ScreenId.AUTOMATION_ENVIRONMENT)
        )

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
            "Forza Automation Assist",
            self.shell_spec.window_title,
        )
        self.assertEqual(5, len(self.shell_spec.screens))
        self.assertEqual(63, self.shell_spec.top_bar.height)
        self.assertTrue(self.shell_spec.top_bar.reserves_identity_space)

    def test_desktop_brand_logo_asset_contract(self) -> None:
        self.assertTrue(DESKTOP_BRAND_LOGO_PATH.exists())
        self.assertEqual("fh6_farm_tool_logo.png", DESKTOP_BRAND_LOGO_PATH.name)
        self.assertEqual(252, DESKTOP_BRAND_LOGO_MAX_WIDTH)
        self.assertEqual(46, DESKTOP_BRAND_LOGO_MAX_HEIGHT)

    def test_desktop_app_icon_asset_contract(self) -> None:
        self.assertTrue(DESKTOP_APP_ICON_PATH.exists())
        self.assertEqual("app_icon.ico", DESKTOP_APP_ICON_PATH.name)
        self.assertTrue(DESKTOP_APP_ICON_FALLBACK_PATH.exists())
        self.assertEqual("tray_icon.png", DESKTOP_APP_ICON_FALLBACK_PATH.name)
        self.assertEqual(DESKTOP_APP_ICON_PATH, _desktop_app_icon_path())
        self.assertEqual("FH6FarmTool.Desktop", DESKTOP_APP_USER_MODEL_ID)

    def test_desktop_tray_menu_contract_is_minimal_and_non_automation(self) -> None:
        self.assertEqual("Forza Automation Assist", DESKTOP_TRAY_TOOLTIP)
        self.assertEqual(
            (
                "Show Forza Automation Assist",
                "Hide to Tray",
                "About Forza Automation Assist",
                "Exit",
            ),
            DESKTOP_TRAY_ACTION_LABELS,
        )
        self.assertFalse(
            any(
                "start" in label.lower() or "stop" in label.lower()
                for label in DESKTOP_TRAY_ACTION_LABELS
            )
        )

    def test_about_dialog_text_contract_includes_beta_and_safety_context(self) -> None:
        about_text = _desktop_about_text()

        self.assertEqual("About Forza Automation Assist", DESKTOP_ABOUT_TITLE)
        self.assertEqual("v0.2.0-beta", DESKTOP_APP_VERSION)
        self.assertEqual("Founding Tester Beta", DESKTOP_APP_BUILD_TYPE)
        self.assertIn("Forza Automation Assist", about_text)
        self.assertIn("Version: v0.2.0-beta", about_text)
        self.assertIn("Build type: Founding Tester Beta", about_text)
        self.assertIn("supervised desktop automation utility", about_text)
        self.assertIn("Controlled/manual beta. Not unattended automation.", about_text)
        self.assertIn("Keep F8 available during automation.", about_text)
        self.assertIn("Support: https://discord.gg/SgARD8YenU", about_text)

    def test_visible_desktop_version_uses_about_metadata(self) -> None:
        self.assertEqual(DESKTOP_APP_VERSION, _desktop_visible_version_text())
        self.assertEqual("v0.2.0-beta", _desktop_visible_version_text())

    def test_prototype_window_is_vertical_companion_and_fixed(self) -> None:
        self.assertEqual(670, self.shell_spec.window_width)
        self.assertEqual(870, self.shell_spec.window_height)
        self.assertLess(self.shell_spec.window_width, self.shell_spec.window_height)
        self.assertTrue(self.shell_spec.is_fixed_size)

    def test_tall_desktop_pages_use_shared_scroll_wrapper(self) -> None:
        source = inspect.getsource(_wrap_in_page_scroll_area)

        self.assertIn("setWidgetResizable(True)", source)
        self.assertIn("ScrollBarAlwaysOff", source)
        self.assertIn("ScrollBarAsNeeded", source)

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
        self.assertEqual(("Automatic Focus", "Manual Focus"), commitment.focus_method_labels)
        self.assertTrue(commitment.focus_methods_share_countdown)
        self.assertTrue(commitment.is_last_safe_exit)
        self.assertFalse(commitment.introduces_execution)
        self.assertIn("FH6 focus handoff", commitment.focus_label)
        self.assertIn("F8", commitment.stop_label)

    def test_commitment_layer_uses_shared_page_spacing(self) -> None:
        source = inspect.getsource(_build_commitment_layer_widget)

        self.assertIn(
            "layout.setSpacing(shell_spec.vertical_rhythm.card_spacing)",
            source,
        )
        self.assertNotIn("layout.addSpacing(", source)
        self.assertIn(
            "action_row.setSpacing(shell_spec.vertical_rhythm.group_spacing)",
            source,
        )
        self.assertIn("action_row.addWidget(automatic_focus_button, 1)", source)
        self.assertIn("action_row.addWidget(manual_focus_button, 1)", source)
        self.assertIn("action_row.addWidget(return_button, 1)", source)

    def test_commitment_layer_has_no_user_facing_profile_content(self) -> None:
        source = inspect.getsource(_build_commitment_layer_widget).lower()

        self.assertNotIn('eyebrow="profile"', source)
        self.assertNotIn("profile_card", source)
        self.assertNotIn("profile_name", source)
        self.assertNotIn("profile_label", source)

    def test_execution_wiring_supports_mvp_automations_and_fails_closed_for_auto4(self) -> None:
        execution_wiring = self.shell_spec.execution_wiring

        self.assertEqual(("auto1", "auto2", "auto3"), execution_wiring.enabled_automation_ids)
        self.assertEqual(("auto4",), execution_wiring.refused_automation_ids)
        self.assertTrue(execution_wiring.uses_existing_guarded_paths)
        self.assertTrue(execution_wiring.preserves_f8_stop)
        self.assertTrue(execution_wiring.fail_closed_for_unsupported_automations)
        self.assertEqual("Forza Horizon 6", DEFAULT_FH6_TARGET_TITLE)

    def test_auto1_race_duration_override_is_single_bounded_basic_runtime_value(self) -> None:
        self.assertEqual(5.0, AUTO1_RACE_DURATION_MIN_SECONDS)
        self.assertEqual(180.0, AUTO1_RACE_DURATION_MAX_SECONDS)
        self.assertEqual(5.0, AUTO1_RACE_DURATION_EXECUTION_BUFFER_SECONDS)
        self.assertEqual(40.0, _parse_auto1_race_duration_override("40.0"))
        self.assertEqual("40.0 seconds", _format_auto1_race_duration_for_display("40.0"))
        self.assertEqual(45.0, _auto1_execution_race_duration(40.0))

        with self.assertRaises(ValueError):
            _parse_auto1_race_duration_override("4.9")

        with self.assertRaises(ValueError):
            _parse_auto1_race_duration_override("180.1")

        with self.assertRaises(ValueError):
            _parse_auto1_race_duration_override("not-a-number")

    def test_auto1_loop_count_is_bounded_basic_runtime_value(self) -> None:
        self.assertEqual(1, AUTO1_LOOP_COUNT_MIN)
        self.assertEqual(25, AUTO1_LOOP_COUNT_MAX)
        self.assertEqual(1, _parse_auto1_loop_count("1"))
        self.assertEqual(25, _parse_auto1_loop_count("25"))
        self.assertEqual("1 loop", _format_auto1_loop_count_for_display("1"))
        self.assertEqual("3 loops", _format_auto1_loop_count_for_display("3"))

        with self.assertRaises(ValueError):
            _parse_auto1_loop_count("0")

        with self.assertRaises(ValueError):
            _parse_auto1_loop_count("26")

        with self.assertRaises(ValueError):
            _parse_auto1_loop_count("not-a-number")

    def test_auto2_purchase_count_is_bounded_runtime_value(self) -> None:
        self.assertEqual(1, _parse_auto2_purchase_count("1"))
        self.assertEqual(25, _parse_auto2_purchase_count("25"))

        with self.assertRaises(ValueError):
            _parse_auto2_purchase_count("0")

        with self.assertRaises(ValueError):
            _parse_auto2_purchase_count("26")

        with self.assertRaises(ValueError):
            _parse_auto2_purchase_count("not-a-number")

    def test_auto1_runtime_adjustment_is_visible_only_for_auto1(self) -> None:
        self.assertTrue(_should_show_auto1_runtime_adjustment("auto1"))
        self.assertFalse(_should_show_auto1_runtime_adjustment("auto2"))
        self.assertFalse(_should_show_auto1_runtime_adjustment("auto3"))

    def test_desktop_execution_supports_mvp_automations_only(self) -> None:
        self.assertTrue(_is_desktop_execution_supported("auto1"))
        self.assertTrue(_is_desktop_execution_supported("auto2"))
        self.assertTrue(_is_desktop_execution_supported("auto3"))
        self.assertFalse(_is_desktop_execution_supported("auto4"))
        self.assertFalse(_is_desktop_execution_supported("unknown"))

    def test_desktop_preparation_supports_mvp_automations_only(self) -> None:
        self.assertTrue(_is_desktop_preparation_available("auto1"))
        self.assertTrue(_is_desktop_preparation_available("auto2"))
        self.assertTrue(_is_desktop_preparation_available("auto3"))
        self.assertFalse(_is_desktop_preparation_available("auto4"))
        self.assertFalse(_is_desktop_preparation_available("unknown"))

    def test_auto2_desktop_boundary_mentions_guarded_bounded_execution(self) -> None:
        details = " ".join(_desktop_execution_refusal_details("auto2"))
        summary = _desktop_execution_confirmation_summary("auto2")

        self.assertIn("Auto2 is available", details)
        self.assertIn("bounded", details)
        self.assertIn("F8 stop", details)
        self.assertIn("guarded Auto2", summary)

    def test_auto3_desktop_boundary_mentions_guarded_bounded_execution(self) -> None:
        details = " ".join(_desktop_execution_refusal_details("auto3"))
        summary = _desktop_execution_confirmation_summary("auto3")

        self.assertIn("Auto3 is available", details)
        self.assertIn("validated car limit", details)
        self.assertIn("F8 stop", details)
        self.assertIn("guarded Auto3", summary)

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
                "requested_cycles": "4",
            }
        )

        joined = " ".join(details)
        self.assertIn("Auto1 selected", joined)
        self.assertIn("Race drive duration: 55.0 seconds", joined)
        self.assertIn("Requested loops: 4 loops", joined)
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

    def test_auto2_commitment_readiness_is_real_input_ready(self) -> None:
        details = _build_commitment_readiness_details(
            {
                "automation_id": "auto2",
                "automation_name": "Auto2 Buy Car",
                "auto2_mode": "purchase",
                "auto2_purchase_count": "6",
                "race_duration_seconds": "55.0",
            }
        )

        joined = " ".join(details)
        self.assertIn("Auto2 selected", joined)
        self.assertIn("Purchase cars", joined)
        self.assertIn("Purchases: 6", joined)
        self.assertIn("Expected baseline", joined)
        self.assertIn("F8 emergency stop", joined)

    def test_auto3_commitment_readiness_is_real_input_ready(self) -> None:
        details = _build_commitment_readiness_details(
            {
                "automation_id": "auto3",
                "automation_name": "Auto3 Skill Tree",
                "auto3_mode": "unlock",
                "auto3_cars": "4",
            }
        )

        joined = " ".join(details)
        self.assertIn("Auto3 selected", joined)
        self.assertIn("Multi-car unlock", joined)
        self.assertIn("Cars: 4", joined)
        self.assertIn("A1 -> B1 -> C1 -> A2", joined)

    def test_operator_guidance_readiness_cards_name_required_starting_positions(self) -> None:
        auto1 = " ".join(("auto1", _desktop_baseline_summary("auto1"), * _desktop_baseline_details("auto1", object())))
        auto2 = " ".join(("auto2", _desktop_baseline_summary("auto2"), * _desktop_baseline_details("auto2", object())))
        auto3 = " ".join(("auto3", _desktop_baseline_summary("auto3"), * _desktop_baseline_details("auto3", object())))

        self.assertIn("Post-race Restart screen", auto1)
        self.assertIn("pressing X should restart", auto1)
        self.assertIn("Help -> Auto1 Guide", auto1)
        self.assertIn("Autoshow", auto2)
        self.assertIn("Subaru Impreza 22B-STi Version (1998)", auto2)
        self.assertIn("Help -> Auto2 Guide", auto2)
        self.assertIn("Garage -> Cars -> My Cars -> Recently Added", auto3)
        self.assertIn("currently selected vehicle", auto3)
        self.assertIn("newly purchased Subaru", auto3)
        self.assertIn("A1 -> B1 -> C1 -> A2", auto3)
        self.assertIn("Help -> Auto3 Guide", auto3)

    def test_auto1_ui_execution_profile_adds_hidden_race_duration_buffer(self) -> None:
        profile = _build_auto1_ui_execution_profile(
            {"race_duration_seconds": "55.0"}
        )

        self.assertEqual(60.0, profile["timings"]["race_duration"])
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

        self.assertIn("Auto1 guarded run unavailable", summary)
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
        self.assertEqual(8, rhythm.card_spacing)
        self.assertEqual(14, rhythm.section_spacing)
        self.assertEqual(10, rhythm.group_spacing)
        self.assertEqual(12, rhythm.card_horizontal_padding)
        self.assertEqual(10, rhythm.card_vertical_padding)
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
                "COMMUNITY & SUPPORT",
            ),
            signal_titles,
        )
        self.assertEqual(
            (
                ZoneRole.PRIMARY,
                ZoneRole.SECONDARY,
            ),
            signal_roles,
        )

    def test_home_uses_single_community_support_footer_card(self) -> None:
        source = inspect.getsource(_build_home_screen_content)
        card_source = inspect.getsource(_build_community_support_card)

        self.assertIn("_build_community_support_card", source)
        self.assertNotIn("RECENT CONTEXT", source)
        self.assertNotIn("QUIET STATUS", source)
        for label in ("Community & Support", "Discord", "YouTube"):
            self.assertIn(label, card_source)
        self.assertNotIn("Documentation", card_source)
        self.assertIn("button_row.addWidget(button, 1)", card_source)
        self.assertIn("layout.addStretch(1)", source)

    def test_home_has_no_review_and_plan_card(self) -> None:
        source = inspect.getsource(_build_home_screen_content)

        self.assertNotIn("Review & Plan", source)
        self.assertNotIn("Review Profiles", source)
        self.assertNotIn("open_profiles", source)

    def test_home_identity_card_uses_final_product_copy(self) -> None:
        source = inspect.getsource(_build_home_screen_content)

        self.assertIn('title="Forza Automation Assist"', source)
        self.assertIn("farming Super", source)
        self.assertIn("purchasing the Subaru Impreza", source)
        self.assertIn("validated behavior, supervised", source)
        self.assertIn('"System ready."', source)
        self.assertNotIn('title="Ready when the baseline is clear"', source)

    def test_desktop_automation_environment_hides_profile_and_warnings_cards(self) -> None:
        source = inspect.getsource(_build_automation_environment_widget)

        self.assertNotIn('eyebrow="ACTIVE PROFILE"', source)
        self.assertNotIn('eyebrow="CONTEXTUAL WARNINGS"', source)

    def test_automation_environment_uses_dynamic_baseline_preparation_card(self) -> None:
        source = inspect.getsource(_build_automation_environment_widget)

        self.assertIn('eyebrow="BASELINE PREPARATION"', source)
        self.assertIn("_baseline_preparation_content(automation_id)", source)
        self.assertNotIn("definition.expected_baseline", source)
        self.assertNotIn(
            "Prepared state only. Supervision is available after commitment.",
            source,
        )
        self.assertNotIn(
            "No operation begins until focus handoff and commitment.",
            source,
        )

    def test_baseline_preparation_content_matches_each_automation(self) -> None:
        auto1 = " ".join(
            (
                _baseline_preparation_content("auto1")[0],
                _baseline_preparation_content("auto1")[1],
                *_baseline_preparation_content("auto1")[2],
            )
        )
        auto2 = " ".join(
            (
                _baseline_preparation_content("auto2")[0],
                _baseline_preparation_content("auto2")[1],
                *_baseline_preparation_content("auto2")[2],
            )
        )
        auto3 = " ".join(
            (
                _baseline_preparation_content("auto3")[0],
                _baseline_preparation_content("auto3")[1],
                *_baseline_preparation_content("auto3")[2],
            )
        )

        self.assertIn("validated EventLab farm race", auto1)
        self.assertIn("Help -> Auto1 Guide", auto1)
        self.assertIn("official FAA Discord", auto1)
        self.assertIn("validated Autoshow baseline", auto2)
        self.assertIn("Help -> Auto2 Guide", auto2)
        self.assertNotIn("Discord", auto2)
        self.assertIn("validated Garage baseline", auto3)
        self.assertIn("Help -> Auto3 Guide", auto3)
        self.assertNotIn("Discord", auto3)

    def test_auto1_guide_starts_with_validated_farm_race_guidance(self) -> None:
        source = inspect.getsource(_build_help_screen_content)
        auto1_start = source.index("def build_auto1_content")
        purpose_position = source.index("Purpose:", auto1_start)
        validated_position = source.index("Validated Farm Race", auto1_start)

        self.assertLess(validated_position, purpose_position)
        self.assertIn("EventLab share codes may change", source)
        self.assertIn('QPushButton("Open Discord")', source)
        self.assertIn("open_official_discord()", source)

    def test_automation_environment_renders_preparation_only_structure(self) -> None:
        section_ids = tuple(
            section.section_id
            for section in self.shell_spec.automation_environment.sections
        )

        self.assertEqual(
            (
                AutomationEnvironmentSectionId.OVERVIEW,
                AutomationEnvironmentSectionId.PROFILE,
                AutomationEnvironmentSectionId.CONTEXTUAL_WARNINGS,
                AutomationEnvironmentSectionId.ADVANCED,
                AutomationEnvironmentSectionId.RUN,
            ),
            section_ids,
        )
        self.assertEqual("", self.shell_spec.automation_environment.primary_intention)

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
            len(sections_by_id[AutomationEnvironmentSectionId.RUN].details),
            2,
        )

    def test_readiness_is_rendered_only_in_commitment_stage(self) -> None:
        automation_source = inspect.getsource(_build_automation_environment_widget)
        commitment_source = inspect.getsource(_build_commitment_layer_widget)

        self.assertNotIn('eyebrow="READINESS"', automation_source)
        self.assertEqual(1, commitment_source.count('eyebrow="READINESS"'))
        self.assertIn("_commitment_readiness_content", commitment_source)

    def test_commitment_readiness_handles_neutral_startup_state(self) -> None:
        title, summary, details = _commitment_readiness_content("")

        self.assertEqual("No automation prepared", title)
        self.assertEqual(
            "Prepare a supervised operation before reviewing readiness.",
            summary,
        )
        self.assertTrue(details)

    def test_commitment_readiness_resolves_all_supported_automations(self) -> None:
        for automation_id in ("auto1", "auto2", "auto3"):
            with self.subTest(automation_id=automation_id):
                title, summary, details = _commitment_readiness_content(
                    automation_id
                )

                self.assertEqual("Required Starting Position", title)
                self.assertNotEqual("No automation prepared", summary)
                self.assertTrue(details)


if __name__ == "__main__":
    unittest.main()
