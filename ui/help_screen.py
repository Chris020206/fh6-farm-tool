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
    questions: list[HelpQuestion] = list(_build_operator_guides())

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


def _build_operator_guides() -> tuple[HelpQuestion, ...]:
    return (
        HelpQuestion(
            question="Auto1 Guide",
            answer=(
                "What this automation does: repeated race automation. Required "
                "Starting Position: complete one race manually first, then stay on "
                "the post-race Restart screen where pressing X restarts the event. "
                "What happens when you run it: Auto1 repeats the validated race flow. "
                "Common mistakes: do not start from freeroam, map, garage, pause menu, "
                "or festival menu. What to do if unsure: stop, return to the Restart "
                "screen, and keep F8 ready."
            ),
            topic_type=HelpTopicType.GUIDE,
            related_automation_id="auto1",
            supporting_context=(
                "Screenshot placeholder: This is where the Auto1 starting position screenshot should be shown.",
            ),
        ),
        HelpQuestion(
            question="Auto2 Guide",
            answer=(
                "What this automation does: buys the Subaru Impreza 22B-STi Version "
                "(1998), the current validated wheelspin workflow vehicle. Required "
                "Starting Position: Autoshow at the validated buy-car menu baseline. "
                "What happens when you run it: test mode validates navigation; purchase "
                "mode can spend credits. Common mistakes: wrong manufacturer, wrong car, "
                "or unexpected confirmation screen. What to do if unsure: use test mode "
                "first, then stop and re-check if the wrong item appears selected."
            ),
            topic_type=HelpTopicType.GUIDE,
            related_automation_id="auto2",
            supporting_context=(
                "Screenshot placeholder: This is where the Auto2 starting position screenshot should be shown.",
            ),
        ),
        HelpQuestion(
            question="Auto3 Guide",
            answer=(
                "What this automation does: unlocks the validated wheelspin perk path "
                "on the currently selected car. Target / Vehicle requirement: the "
                "selected car should be the first newly purchased Subaru Impreza "
                "22B-STi Version (1998). Required Starting Position: Garage -> Cars "
                "-> My Cars -> Recently Added. Sort/order matters. What happens when "
                "you run it: Auto3 uses start row A and validated traversal A1 -> B1 "
                "-> C1 -> A2, current max 4 cars. Common mistakes: wrong selected car, "
                "wrong row, or unknown sort state. What to do if unsure: do not run "
                "unlock mode; re-check which car is selected. Unlock mode can spend "
                "skill points."
            ),
            topic_type=HelpTopicType.GUIDE,
            related_automation_id="auto3",
            supporting_context=(
                "Screenshot placeholder: This is where the Auto3 starting position screenshot should be shown.",
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
