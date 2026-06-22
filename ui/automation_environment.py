from dataclasses import dataclass, field
from enum import Enum

from frontend.automation_controller import AutomationRunPlan
from product.automation_definition import AutomationDefinition
from product.profile_metadata import ProfileMetadata
from product.readiness_model import AcknowledgementLevel, ReadinessModel


class AutomationEnvironmentSectionId(str, Enum):
    OVERVIEW = "overview"
    PROFILE = "profile"
    CONTEXTUAL_WARNINGS = "contextual_warnings"
    ADVANCED = "advanced"
    RUN = "run"


@dataclass(frozen=True)
class OverviewSection:
    section_id: AutomationEnvironmentSectionId
    display_name: str
    short_purpose: str
    validated_scope: str
    expected_baseline: str


@dataclass(frozen=True)
class ProfileSection:
    section_id: AutomationEnvironmentSectionId
    profile_id: str
    profile_name: str
    behavior_summary: str
    reliability_posture: str
    customization_status: str


@dataclass(frozen=True)
class ContextualWarningsSection:
    section_id: AutomationEnvironmentSectionId
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class AdvancedSection:
    section_id: AutomationEnvironmentSectionId
    is_collapsed_by_default: bool
    purpose: str
    available_refinements: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RunSection:
    section_id: AutomationEnvironmentSectionId
    can_prepare_commitment: bool
    status_label: str
    commitment_message: str
    refusal_message: str | None
    requested_count: int
    acknowledgement_level: AcknowledgementLevel


@dataclass(frozen=True)
class AutomationEnvironmentScreen:
    automation_id: str
    profile_id: str
    sections: tuple[
        OverviewSection
        | ProfileSection
        | ContextualWarningsSection
        | AdvancedSection
        | RunSection,
        ...,
    ]


SECTION_ORDER: tuple[AutomationEnvironmentSectionId, ...] = (
    AutomationEnvironmentSectionId.OVERVIEW,
    AutomationEnvironmentSectionId.PROFILE,
    AutomationEnvironmentSectionId.CONTEXTUAL_WARNINGS,
    AutomationEnvironmentSectionId.ADVANCED,
    AutomationEnvironmentSectionId.RUN,
)


def build_automation_environment_screen(
    automation_definition: AutomationDefinition,
    profile_metadata: ProfileMetadata,
    readiness_model: ReadinessModel,
    run_plan: AutomationRunPlan,
) -> AutomationEnvironmentScreen:
    warnings = _combine_warnings(
        readiness_model.contextual_warnings,
        run_plan.warnings,
    )

    return AutomationEnvironmentScreen(
        automation_id=automation_definition.automation_id,
        profile_id=profile_metadata.profile_id,
        sections=(
            OverviewSection(
                section_id=AutomationEnvironmentSectionId.OVERVIEW,
                display_name=automation_definition.display_name,
                short_purpose=automation_definition.short_purpose,
                validated_scope=automation_definition.validated_scope,
                expected_baseline=automation_definition.expected_baseline,
            ),
            ProfileSection(
                section_id=AutomationEnvironmentSectionId.PROFILE,
                profile_id=profile_metadata.profile_id,
                profile_name=profile_metadata.profile_name,
                behavior_summary=profile_metadata.behavior_summary,
                reliability_posture=profile_metadata.reliability_posture,
                customization_status=profile_metadata.customization_status,
            ),
            ContextualWarningsSection(
                section_id=AutomationEnvironmentSectionId.CONTEXTUAL_WARNINGS,
                warnings=warnings,
            ),
            AdvancedSection(
                section_id=AutomationEnvironmentSectionId.ADVANCED,
                is_collapsed_by_default=True,
                purpose=(
                    "Controlled refinement area for future options that should remain "
                    "secondary to confidence formation."
                ),
            ),
            RunSection(
                section_id=AutomationEnvironmentSectionId.RUN,
                can_prepare_commitment=run_plan.accepted,
                status_label="prepared" if run_plan.accepted else "refused",
                commitment_message=_build_commitment_message(run_plan),
                refusal_message=run_plan.refusal_message,
                requested_count=run_plan.request.requested_count,
                acknowledgement_level=readiness_model.acknowledgement_level,
            ),
        ),
    )


def _combine_warnings(
    readiness_warnings: tuple[str, ...],
    run_plan_warnings: tuple[str, ...],
) -> tuple[str, ...]:
    combined_warnings: list[str] = []

    for warning in readiness_warnings + run_plan_warnings:
        if warning not in combined_warnings:
            combined_warnings.append(warning)

    return tuple(combined_warnings)


def _build_commitment_message(run_plan: AutomationRunPlan) -> str:
    if not run_plan.accepted:
        return "Run commitment is unavailable until the refusal is resolved."

    return "Run plan is prepared for operator review before execution."
