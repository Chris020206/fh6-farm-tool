from dataclasses import dataclass
from enum import Enum

from product.automation_definition import AutomationDefinition
from product.profile_metadata import (
    PackageTier,
    ProfileMetadata,
    RecommendationStatus,
    ValidationConfidence,
)


class ProfileSelectionAvailability(str, Enum):
    AVAILABLE = "available"
    RESTRICTED = "restricted"
    FUTURE = "future"


class ProfileSectionId(str, Enum):
    RECOMMENDED = "recommended"
    ALTERNATIVE = "alternative"
    CUSTOM = "custom"


@dataclass(frozen=True)
class ProfileSelectionState:
    profile_id: str
    profile_name: str
    automation_id: str | None
    automation_name: str | None
    package_tier: PackageTier
    recommendation_status: RecommendationStatus
    validation_confidence: ValidationConfidence
    behavior_summary: str
    reliability_posture: str
    customization_status: str
    availability: ProfileSelectionAvailability
    is_selectable: bool


@dataclass(frozen=True)
class RecommendedProfilesSection:
    section_id: ProfileSectionId
    purpose: str
    profiles: tuple[ProfileSelectionState, ...]


@dataclass(frozen=True)
class AlternativeProfilesSection:
    section_id: ProfileSectionId
    purpose: str
    profiles: tuple[ProfileSelectionState, ...]


@dataclass(frozen=True)
class CustomProfilesSection:
    section_id: ProfileSectionId
    purpose: str
    profiles: tuple[ProfileSelectionState, ...]
    is_tertiary: bool = True


@dataclass(frozen=True)
class ProfilesScreen:
    primary_intention: str
    recommended_profiles: RecommendedProfilesSection
    alternative_profiles: AlternativeProfilesSection
    custom_profiles: CustomProfilesSection


def build_profiles_screen(
    profile_metadata: tuple[ProfileMetadata, ...],
    automation_definitions: tuple[AutomationDefinition, ...],
) -> ProfilesScreen:
    automation_by_profile_id = _map_automations_by_profile_id(automation_definitions)
    selection_states = tuple(
        _build_profile_selection_state(metadata, automation_by_profile_id)
        for metadata in profile_metadata
    )

    recommended_profiles = tuple(
        state
        for state in selection_states
        if state.recommendation_status == RecommendationStatus.CURATED
        and state.availability == ProfileSelectionAvailability.AVAILABLE
    )
    alternative_profiles = tuple(
        state
        for state in selection_states
        if state.recommendation_status
        in {RecommendationStatus.SUPPORTED, RecommendationStatus.EXPERIMENTAL}
        or state.availability
        in {
            ProfileSelectionAvailability.RESTRICTED,
            ProfileSelectionAvailability.FUTURE,
        }
    )
    custom_profiles = tuple(
        state
        for state in selection_states
        if state.recommendation_status == RecommendationStatus.CUSTOM
    )

    return ProfilesScreen(
        primary_intention="Choose trusted execution behavior.",
        recommended_profiles=RecommendedProfilesSection(
            section_id=ProfileSectionId.RECOMMENDED,
            purpose="Curated trusted recommendations for normal selection.",
            profiles=_sort_profiles(recommended_profiles),
        ),
        alternative_profiles=AlternativeProfilesSection(
            section_id=ProfileSectionId.ALTERNATIVE,
            purpose="Secondary validated or restricted options for controlled flexibility.",
            profiles=_sort_profiles(alternative_profiles),
        ),
        custom_profiles=CustomProfilesSection(
            section_id=ProfileSectionId.CUSTOM,
            purpose="Earned custom profiles for advanced operators.",
            profiles=_sort_profiles(custom_profiles),
        ),
    )


def _map_automations_by_profile_id(
    automation_definitions: tuple[AutomationDefinition, ...],
) -> dict[str, AutomationDefinition]:
    automations_by_profile_id: dict[str, AutomationDefinition] = {}

    for automation_definition in automation_definitions:
        for profile_id in automation_definition.available_profiles:
            automations_by_profile_id[profile_id] = automation_definition

    return automations_by_profile_id


def _build_profile_selection_state(
    metadata: ProfileMetadata,
    automation_by_profile_id: dict[str, AutomationDefinition],
) -> ProfileSelectionState:
    automation_definition = automation_by_profile_id.get(metadata.profile_id)
    availability = _determine_availability(metadata, automation_definition)

    return ProfileSelectionState(
        profile_id=metadata.profile_id,
        profile_name=metadata.profile_name,
        automation_id=automation_definition.automation_id
        if automation_definition is not None
        else None,
        automation_name=automation_definition.display_name
        if automation_definition is not None
        else None,
        package_tier=metadata.package_tier,
        recommendation_status=metadata.recommendation_status,
        validation_confidence=metadata.validation_confidence,
        behavior_summary=metadata.behavior_summary,
        reliability_posture=metadata.reliability_posture,
        customization_status=metadata.customization_status,
        availability=availability,
        is_selectable=availability == ProfileSelectionAvailability.AVAILABLE,
    )


def _determine_availability(
    metadata: ProfileMetadata,
    automation_definition: AutomationDefinition | None,
) -> ProfileSelectionAvailability:
    if automation_definition is None:
        return ProfileSelectionAvailability.RESTRICTED

    if not automation_definition.is_active:
        return ProfileSelectionAvailability.FUTURE

    if metadata.recommendation_status == RecommendationStatus.EXPERIMENTAL:
        return ProfileSelectionAvailability.RESTRICTED

    return ProfileSelectionAvailability.AVAILABLE


def _sort_profiles(
    profiles: tuple[ProfileSelectionState, ...],
) -> tuple[ProfileSelectionState, ...]:
    return tuple(
        sorted(
            profiles,
            key=lambda profile: (
                profile.package_tier.value,
                profile.profile_name,
            ),
        )
    )
