from dataclasses import dataclass
from enum import Enum

from product.automation_definition import AutomationDefinition
from product.profile_metadata import ProfileMetadata
from product.readiness_model import ReadinessModel


class HelpSectionId(str, Enum):
    COMMON_QUESTIONS = "common_questions"
    CONTEXTUAL_GUIDANCE = "contextual_guidance"
    TROUBLESHOOTING = "troubleshooting"


class HelpTopicType(str, Enum):
    BASELINE = "baseline"
    GUIDE = "guide"
    READINESS = "readiness"
    PROFILE = "profile"
    RESULT = "result"
    SAFETY = "safety"
    TROUBLESHOOTING = "troubleshooting"


@dataclass(frozen=True)
class HelpQuestion:
    question: str
    answer: str
    topic_type: HelpTopicType
    related_automation_id: str | None = None
    supporting_context: tuple[str, ...] = ()


@dataclass(frozen=True)
class AutomationGuide:
    automation_id: str
    title: str
    purpose: str
    required_starting_position: str
    target_or_vehicle_requirement: str | None
    details: tuple[str, ...]
    screenshot_placeholder: str
    what_happens_when_run: str
    before_you_press_run: tuple[str, ...]
    common_mistakes: tuple[str, ...]
    recovery_guidance: tuple[str, ...]
    safety_notes: tuple[str, ...]


@dataclass(frozen=True)
class CommonQuestionsSection:
    section_id: HelpSectionId
    purpose: str
    questions: tuple[HelpQuestion, ...]
    is_primary: bool = True


@dataclass(frozen=True)
class ContextualGuidanceSection:
    section_id: HelpSectionId
    purpose: str
    questions: tuple[HelpQuestion, ...]
    guides: tuple[AutomationGuide, ...]
    is_secondary: bool = True


@dataclass(frozen=True)
class TroubleshootingSection:
    section_id: HelpSectionId
    purpose: str
    questions: tuple[HelpQuestion, ...]
    is_tertiary: bool = True


@dataclass(frozen=True)
class HelpScreen:
    primary_intention: str
    common_questions: CommonQuestionsSection
    contextual_guidance: ContextualGuidanceSection
    troubleshooting: TroubleshootingSection


def build_help_screen(
    automation_definitions: tuple[AutomationDefinition, ...],
    readiness_models: tuple[ReadinessModel, ...],
    profile_metadata: tuple[ProfileMetadata, ...],
) -> HelpScreen:
    readiness_by_automation_id = {
        readiness_model.automation_id: readiness_model
        for readiness_model in readiness_models
    }
    profiles_by_automation_type = _group_profiles_by_automation_type(profile_metadata)

    return HelpScreen(
        primary_intention="Answer common operator questions with calm confidence.",
        common_questions=CommonQuestionsSection(
            section_id=HelpSectionId.COMMON_QUESTIONS,
            purpose="Primary answer-first support for common operator uncertainty.",
            questions=_build_common_questions(),
        ),
        contextual_guidance=ContextualGuidanceSection(
            section_id=HelpSectionId.CONTEXTUAL_GUIDANCE,
            purpose="Secondary automation-specific baseline, readiness, and profile guidance.",
            questions=_build_contextual_guidance(
                automation_definitions,
                readiness_by_automation_id,
                profiles_by_automation_type,
            ),
            guides=_build_operator_guides(),
        ),
        troubleshooting=TroubleshootingSection(
            section_id=HelpSectionId.TROUBLESHOOTING,
            purpose="Tertiary recovery guidance for misalignment or refusal cases.",
            questions=_build_troubleshooting_questions(
                automation_definitions,
                readiness_by_automation_id,
            ),
        ),
    )


def _build_common_questions() -> tuple[HelpQuestion, ...]:
    return (
        HelpQuestion(
            question="What should I check before running automation?",
            answer=(
                "Start from the documented FH6 baseline, keep the game focused, "
                "use a trusted profile, and keep stop control ready."
            ),
            topic_type=HelpTopicType.READINESS,
        ),
        HelpQuestion(
            question="What does a profile mean?",
            answer=(
                "A profile describes trusted execution behavior, not a technical "
                "settings panel."
            ),
            topic_type=HelpTopicType.PROFILE,
        ),
        HelpQuestion(
            question="What does stopped mean?",
            answer=(
                "Stopped means the operator intentionally ended execution and should "
                "review the FH6 baseline before another run."
            ),
            topic_type=HelpTopicType.RESULT,
        ),
        HelpQuestion(
            question="What does refused mean?",
            answer=(
                "Refused means the system blocked a request before execution to "
                "preserve safety boundaries."
            ),
            topic_type=HelpTopicType.RESULT,
        ),
    )


def _build_contextual_guidance(
    automation_definitions: tuple[AutomationDefinition, ...],
    readiness_by_automation_id: dict[str, ReadinessModel],
    profiles_by_automation_type: dict[str, tuple[ProfileMetadata, ...]],
) -> tuple[HelpQuestion, ...]:
    questions: list[HelpQuestion] = []

    for automation_definition in automation_definitions:
        if not automation_definition.is_active:
            continue

        readiness_model = readiness_by_automation_id.get(
            automation_definition.automation_id
        )
        if readiness_model is None:
            continue

        questions.append(
            HelpQuestion(
                question=f"What baseline does {automation_definition.display_name} expect?",
                answer=readiness_model.expected_baseline,
                topic_type=HelpTopicType.BASELINE,
                related_automation_id=automation_definition.automation_id,
                supporting_context=(readiness_model.manual_positioning_assumption,),
            )
        )
        questions.append(
            HelpQuestion(
                question=f"When is {automation_definition.display_name} ready to run?",
                answer=readiness_model.readiness_wording,
                topic_type=HelpTopicType.READINESS,
                related_automation_id=automation_definition.automation_id,
                supporting_context=readiness_model.confidence_notes,
            )
        )

        for profile in _profiles_for_automation(
            automation_definition,
            profiles_by_automation_type,
        ):
            questions.append(
                HelpQuestion(
                    question=f"What behavior does {profile.profile_name} use?",
                    answer=profile.behavior_summary,
                    topic_type=HelpTopicType.PROFILE,
                    related_automation_id=automation_definition.automation_id,
                    supporting_context=(profile.reliability_posture,),
                )
            )

    return tuple(questions)


def _build_operator_guides() -> tuple[AutomationGuide, ...]:
    return (
        AutomationGuide(
            automation_id="auto1",
            title="Auto1 Guide - Race Automation",
            purpose="Repeated race automation.",
            required_starting_position="Post-race Restart screen.",
            target_or_vehicle_requirement=None,
            details=(
                "Complete one race manually first.",
                "Stay on the screen where pressing X restarts the event.",
                "Do not start from freeroam, map, garage, pause menu, or festival menu.",
            ),
            screenshot_placeholder="This is where the Auto1 Restart screen screenshot should be shown.",
            what_happens_when_run=(
                "Auto1 restarts the race, confirms prompts, holds throttle, and repeats for the selected count."
            ),
            before_you_press_run=(
                "One race completed manually",
                "Restart screen visible",
                "X restarts the event",
                "FH6 can receive focus",
                "F8 is ready",
            ),
            common_mistakes=(
                "Starting from freeroam",
                "Starting from pause/map/garage",
                "FH6 not focused",
                "Restart screen not visible",
            ),
            recovery_guidance=(
                "Stop with F8 if needed.",
                "Return to the post-race Restart screen.",
                "Try again only from the required starting position.",
            ),
            safety_notes=(
                "Supervised automation only.",
                "Keep F8 available.",
            ),
        ),
        AutomationGuide(
            automation_id="auto2",
            title="Auto2 Guide - Buy Car Automation",
            purpose="Purchase the validated wheelspin vehicle.",
            required_starting_position="Autoshow at the validated buy-car menu baseline.",
            target_or_vehicle_requirement="Subaru Impreza 22B-STi Version (1998)",
            details=(
                "Auto2 is designed around purchasing this specific validated wheelspin workflow vehicle.",
                "This vehicle is currently the validated/optimal wheelspin workflow target.",
            ),
            screenshot_placeholder="This is where the Auto2 Autoshow starting position screenshot should be shown.",
            what_happens_when_run=(
                "Test mode validates navigation without purchase. Purchase mode navigates the validated path and can spend in-game credits."
            ),
            before_you_press_run=(
                "Autoshow is open",
                "Buy-car menu is at the expected baseline",
                "Credits are available for purchase mode",
                "Test mode was used if alignment is uncertain",
                "F8 is ready",
            ),
            common_mistakes=(
                "Wrong manufacturer selected",
                "Wrong car selected",
                "Purchase mode used before test mode",
                "Unexpected confirmation screen",
                "FH6 not focused",
            ),
            recovery_guidance=(
                "Use F8 if alignment is wrong.",
                "Return to Autoshow.",
                "Use test mode first before spending credits.",
            ),
            safety_notes=(
                "Purchase mode can spend in-game credits.",
            ),
        ),
        AutomationGuide(
            automation_id="auto3",
            title="Auto3 Guide - Skill Tree Automation",
            purpose="Unlock the validated wheelspin perk path.",
            required_starting_position="Garage -> Cars -> My Cars -> Recently Added",
            target_or_vehicle_requirement=(
                "Auto3 operates on the currently selected vehicle. It does not independently verify the car model. "
                "The selected vehicle should be the first newly purchased Subaru Impreza 22B-STi Version (1998)."
            ),
            details=(
                "Sort/order matters.",
                "Start row A only.",
                "Validated traversal: A1 -> B1 -> C1 -> A2.",
                "Current max: 4 cars.",
            ),
            screenshot_placeholder="This is where the Auto3 My Cars / Recently Added starting position screenshot should be shown.",
            what_happens_when_run=(
                "Auto3 opens the selected car, enters Car Mastery, unlocks the validated perk path, exits, and continues through the validated traversal when multiple cars are selected."
            ),
            before_you_press_run=(
                "Garage -> Cars -> My Cars is open",
                "Recently Added sorting is active",
                "Start row is A",
                "Correct newly purchased Subaru is selected",
                "Skill points are available",
                "F8 is ready",
            ),
            common_mistakes=(
                "Wrong car selected",
                "Wrong sort order",
                "Wrong start row",
                "Assuming Auto3 verifies the car model",
                "Running unlock mode while unsure",
                "FH6 not focused",
            ),
            recovery_guidance=(
                "If unsure which car is selected, do not run unlock mode.",
                "Return to My Cars.",
                "Re-sort Recently Added.",
                "Verify the selected Subaru before running again.",
            ),
            safety_notes=(
                "Unlock mode can spend skill points.",
                "Maximum validated cars: 4.",
            ),
        ),
    )


def _build_troubleshooting_questions(
    automation_definitions: tuple[AutomationDefinition, ...],
    readiness_by_automation_id: dict[str, ReadinessModel],
) -> tuple[HelpQuestion, ...]:
    questions: list[HelpQuestion] = []

    for automation_definition in automation_definitions:
        if not automation_definition.is_active:
            continue

        readiness_model = readiness_by_automation_id.get(
            automation_definition.automation_id
        )
        if readiness_model is None:
            continue

        questions.append(
            HelpQuestion(
                question=f"What should I do if {automation_definition.display_name} looks misaligned?",
                answer=(
                    "Stop, return FH6 to the expected baseline, and review the "
                    "readiness guidance before trying again."
                ),
                topic_type=HelpTopicType.TROUBLESHOOTING,
                related_automation_id=automation_definition.automation_id,
                supporting_context=(
                    readiness_model.contextual_warnings
                    + readiness_model.blocked_or_refused_conditions
                ),
            )
        )

    return tuple(questions)


def _group_profiles_by_automation_type(
    profile_metadata: tuple[ProfileMetadata, ...],
) -> dict[str, tuple[ProfileMetadata, ...]]:
    grouped_profiles: dict[str, list[ProfileMetadata]] = {}

    for profile in profile_metadata:
        grouped_profiles.setdefault(profile.automation_type, []).append(profile)

    return {
        automation_type: tuple(profiles)
        for automation_type, profiles in grouped_profiles.items()
    }


def _profiles_for_automation(
    automation_definition: AutomationDefinition,
    profiles_by_automation_type: dict[str, tuple[ProfileMetadata, ...]],
) -> tuple[ProfileMetadata, ...]:
    profile_ids = set(automation_definition.available_profiles)

    return tuple(
        profile
        for profiles in profiles_by_automation_type.values()
        for profile in profiles
        if profile.profile_id in profile_ids
    )
