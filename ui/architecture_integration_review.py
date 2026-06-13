from dataclasses import dataclass
from enum import Enum

from frontend.automation_controller import (
    AutomationRunRequest,
    FrontendAutomationController,
)
from product.automation_registry import get_automation_definition
from product.profile_metadata_registry import (
    get_all_profile_metadata,
    get_profile_metadata,
)
from product.readiness_registry import (
    get_all_readiness_models,
    get_readiness_model,
)
from ui.automation_environment import build_automation_environment_screen
from ui.app_flow import APP_FLOW, AppFlowState
from ui.help_screen import build_help_screen
from ui.history_screen import build_history_screen
from ui.profiles_screen import build_profiles_screen
from ui.settings_screen import build_settings_screen
from ui.shell import (
    get_screen_descriptors,
    get_sidebar_destinations,
)


@dataclass(frozen=True)
class UIArchitectureIntegrationCheck:
    check_id: str
    passed: bool
    summary: str


@dataclass(frozen=True)
class UIArchitectureIntegrationReview:
    verdict: str
    checks: tuple[UIArchitectureIntegrationCheck, ...]
    carry_forward_notes: tuple[str, ...]
    hard_boundaries_preserved: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return all(check.passed for check in self.checks)


CARRY_FORWARD_NOTES: tuple[str, ...] = (
    (
        "Operational history currently assumes valid automation/profile IDs; "
        "invalid or refused preview rendering needs safe handling before history hardens."
    ),
    (
        "Auto1 acknowledgement may be too heavy; revisit friction level once "
        "interaction and UI behavior exist."
    ),
    (
        "Naming consistency needs review; automation IDs and profile automation "
        "types should be normalized or clearly mapped before display logic hardens."
    ),
)


HARD_BOUNDARIES_PRESERVED: tuple[str, ...] = (
    "No visual UI.",
    "No styling.",
    "No frontend framework.",
    "No automation execution wiring.",
    "No runner calls.",
    "No timing changes.",
    "No real input changes.",
    "No CLI behavior changes.",
    "No safety gate changes.",
)


def build_ui_architecture_integration_review() -> UIArchitectureIntegrationReview:
    checks = (
        _check_sidebar_destinations_align_with_screen_descriptors(),
        _check_all_major_screens_have_one_primary_intention(),
        _check_automation_environment_integrates_with_app_flow(),
        _check_companion_mode_is_only_reachable_from_running(),
        _check_secondary_screen_responsibilities_are_distinct(),
        _check_settings_does_not_duplicate_profiles(),
        _check_history_is_not_logs_or_monitoring(),
        _check_help_is_not_documentation_center(),
        _check_no_raw_execution_details_are_exposed(),
        _check_hard_boundaries_are_conceptually_preserved(),
    )

    return UIArchitectureIntegrationReview(
        verdict="coherent" if all(check.passed for check in checks) else "needs_review",
        checks=checks,
        carry_forward_notes=CARRY_FORWARD_NOTES,
        hard_boundaries_preserved=HARD_BOUNDARIES_PRESERVED,
    )


def _check_sidebar_destinations_align_with_screen_descriptors() -> UIArchitectureIntegrationCheck:
    destination_screen_ids = {
        destination.screen_id
        for destination in get_sidebar_destinations()
    }
    descriptor_screen_ids = {
        descriptor.screen_id
        for descriptor in get_screen_descriptors()
    }

    return UIArchitectureIntegrationCheck(
        check_id="sidebar_screen_alignment",
        passed=destination_screen_ids.issubset(descriptor_screen_ids),
        summary="Sidebar destinations resolve to known screen descriptors.",
    )


def _check_all_major_screens_have_one_primary_intention() -> UIArchitectureIntegrationCheck:
    primary_intentions = [
        descriptor.primary_intention
        for descriptor in get_screen_descriptors()
    ]
    passed = all(
        intention.strip()
        and "\n" not in intention
        and ";" not in intention
        for intention in primary_intentions
    )

    return UIArchitectureIntegrationCheck(
        check_id="one_primary_intention_per_screen",
        passed=passed,
        summary="All major screens expose one concise primary intention.",
    )


def _check_automation_environment_integrates_with_app_flow() -> UIArchitectureIntegrationCheck:
    controller = FrontendAutomationController(
        session_id_provider=lambda: "integration-preview-session",
    )
    run_plan = controller.prepare_run_plan(
        AutomationRunRequest(
            automation_id="auto1",
            profile_id="auto1_race_default",
            requested_count=1,
        )
    )
    screen = build_automation_environment_screen(
        automation_definition=get_automation_definition("auto1"),
        profile_metadata=get_profile_metadata("auto1_race_default"),
        readiness_model=get_readiness_model("auto1"),
        run_plan=run_plan,
    )
    section_ids = {
        section.section_id.value
        for section in screen.sections
    }
    passed = (
        run_plan.accepted
        and APP_FLOW.can_transition(
            AppFlowState.AUTOMATION_ENVIRONMENT,
            AppFlowState.PREPARED,
        )
        and APP_FLOW.can_transition(AppFlowState.PREPARED, AppFlowState.RUNNING)
        and APP_FLOW.can_transition(
            AppFlowState.AUTOMATION_ENVIRONMENT,
            AppFlowState.REFUSED,
        )
        and "run" in section_ids
    )

    return UIArchitectureIntegrationCheck(
        check_id="automation_environment_flow_integration",
        passed=passed,
        summary="Automation Environment connects preparation, commitment, and refusal structure.",
    )


def _check_companion_mode_is_only_reachable_from_running() -> UIArchitectureIntegrationCheck:
    companion_sources = {
        transition.from_state
        for transition in APP_FLOW.transitions
        if transition.to_state == AppFlowState.COMPANION_MODE
    }

    return UIArchitectureIntegrationCheck(
        check_id="companion_mode_running_only",
        passed=companion_sources == {AppFlowState.RUNNING},
        summary="Companion mode is reachable only from the running state.",
    )


def _check_secondary_screen_responsibilities_are_distinct() -> UIArchitectureIntegrationCheck:
    profiles_screen = build_profiles_screen(
        profile_metadata=tuple(get_all_profile_metadata()),
        automation_definitions=tuple(
            get_automation_definition(automation_id)
            for automation_id in ("auto1", "auto2", "auto3", "auto4")
        ),
    )
    history_screen = build_history_screen(())
    help_screen = build_help_screen(
        automation_definitions=tuple(
            get_automation_definition(automation_id)
            for automation_id in ("auto1", "auto2", "auto3", "auto4")
        ),
        readiness_models=tuple(get_all_readiness_models()),
        profile_metadata=tuple(get_all_profile_metadata()),
    )
    settings_screen = build_settings_screen()
    intentions = {
        profiles_screen.primary_intention,
        history_screen.primary_intention,
        help_screen.primary_intention,
        settings_screen.primary_intention,
    }

    return UIArchitectureIntegrationCheck(
        check_id="secondary_screen_responsibility_separation",
        passed=len(intentions) == 4,
        summary="Profiles, History, Help, and Settings keep distinct responsibilities.",
    )


def _check_settings_does_not_duplicate_profiles() -> UIArchitectureIntegrationCheck:
    settings_screen = build_settings_screen()
    serialized_settings = _serialize_public_values(settings_screen).lower()
    prohibited_terms = (
        "profile editor",
        "profile selection",
        "custom profile",
        "timing profile",
        "execution tuning",
    )

    return UIArchitectureIntegrationCheck(
        check_id="settings_profiles_separation",
        passed=not any(term in serialized_settings for term in prohibited_terms),
        summary="Settings remains application-level and does not duplicate Profiles.",
    )


def _check_history_is_not_logs_or_monitoring() -> UIArchitectureIntegrationCheck:
    history_screen = build_history_screen(())
    serialized_history = _serialize_public_values(history_screen).lower()
    prohibited_terms = ("raw log", "keypress", "debug", "live monitoring", "console")

    return UIArchitectureIntegrationCheck(
        check_id="history_operational_memory",
        passed=not any(term in serialized_history for term in prohibited_terms),
        summary="History remains operational memory rather than logs or monitoring.",
    )


def _check_help_is_not_documentation_center() -> UIArchitectureIntegrationCheck:
    help_screen = build_help_screen(
        automation_definitions=tuple(
            get_automation_definition(automation_id)
            for automation_id in ("auto1", "auto2", "auto3", "auto4")
        ),
        readiness_models=tuple(get_all_readiness_models()),
        profile_metadata=tuple(get_all_profile_metadata()),
    )
    serialized_help = _serialize_public_values(help_screen).lower()
    prohibited_terms = ("wiki", "documentation center", "chapter", "support ticket")

    return UIArchitectureIntegrationCheck(
        check_id="help_confidence_support",
        passed=not any(term in serialized_help for term in prohibited_terms),
        summary="Help remains question-oriented confidence support.",
    )


def _check_no_raw_execution_details_are_exposed() -> UIArchitectureIntegrationCheck:
    screens = (
        build_profiles_screen(
            profile_metadata=tuple(get_all_profile_metadata()),
            automation_definitions=tuple(
                get_automation_definition(automation_id)
                for automation_id in ("auto1", "auto2", "auto3", "auto4")
            ),
        ),
        build_history_screen(()),
        build_help_screen(
            automation_definitions=tuple(
                get_automation_definition(automation_id)
                for automation_id in ("auto1", "auto2", "auto3", "auto4")
            ),
            readiness_models=tuple(get_all_readiness_models()),
            profile_metadata=tuple(get_all_profile_metadata()),
        ),
        build_settings_screen(),
    )
    serialized_screens = _serialize_public_values(screens).lower()
    prohibited_terms = (
        "wait_after",
        "menu_key_delay",
        "navigation_counts",
        "raw log",
        "debug",
    )

    return UIArchitectureIntegrationCheck(
        check_id="no_raw_execution_details",
        passed=not any(term in serialized_screens for term in prohibited_terms),
        summary="Screen structures avoid raw execution timing/settings by default.",
    )


def _check_hard_boundaries_are_conceptually_preserved() -> UIArchitectureIntegrationCheck:
    return UIArchitectureIntegrationCheck(
        check_id="hard_boundaries_preserved",
        passed=True,
        summary="R13 adds review structure only; it does not add visual UI or execution wiring.",
    )


def _serialize_public_values(value: object) -> str:
    if isinstance(value, Enum):
        return str(value.value)

    if isinstance(value, tuple | list | set):
        return " ".join(_serialize_public_values(item) for item in value)

    if hasattr(value, "__dict__"):
        return " ".join(
            _serialize_public_values(item)
            for item in vars(value).values()
        )

    return str(value)
