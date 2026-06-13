from product.profile_metadata import (
    PackageTier,
    ProfileMetadata,
    RecommendationStatus,
    ValidationConfidence,
)


PROFILE_METADATA: dict[str, ProfileMetadata] = {
    "auto1_race_default": ProfileMetadata(
        profile_id="auto1_race_default",
        profile_name="Auto1 Race Default",
        automation_type="auto1_race",
        recommendation_status=RecommendationStatus.CURATED,
        package_tier=PackageTier.BASIC,
        behavior_summary=(
            "Reliability-first race restart flow with conservative startup, "
            "confirmation, driving, and post-cycle spacing."
        ),
        reliability_posture="Validated guarded manual race automation profile.",
        intended_usage="Developer/manual Auto1 race farming from the validated restart baseline.",
        validation_confidence=ValidationConfidence.VALIDATED,
        customization_status=(
            "Official read-only baseline. Duplicate to a custom profile before timing tuning."
        ),
        editable_fields=(),
    ),
    "auto2_buy_car_default": ProfileMetadata(
        profile_id="auto2_buy_car_default",
        profile_name="Auto2 Buy Car Default",
        automation_type="auto2_buy_car",
        recommendation_status=RecommendationStatus.CURATED,
        package_tier=PackageTier.BASIC,
        behavior_summary=(
            "Controlled Autoshow navigation profile with conservative menu spacing, "
            "one-car purchase validation, and reset-to-baseline behavior."
        ),
        reliability_posture="Validated only within guarded test-mode and one-car purchase scope.",
        intended_usage="Developer/manual Auto2 validation where purchase spending risk is understood.",
        validation_confidence=ValidationConfidence.CONTROLLED,
        customization_status=(
            "Official read-only baseline. Duplicate to a custom profile before timing tuning."
        ),
        editable_fields=(),
    ),
    "auto3_skill_tree_default": ProfileMetadata(
        profile_id="auto3_skill_tree_default",
        profile_name="Auto3 Skill Tree Default",
        automation_type="auto3_skill_tree",
        recommendation_status=RecommendationStatus.CURATED,
        package_tier=PackageTier.BASIC,
        behavior_summary=(
            "Guarded skill-tree unlock profile using validated A-start traversal, "
            "later-car recovery, and conservative skill-tree input spacing."
        ),
        reliability_posture=(
            "Validated for guarded/manual multi-car unlock testing up to four cars "
            "from the A-row baseline."
        ),
        intended_usage="Developer/manual Auto3 unlock validation with operator supervision.",
        validation_confidence=ValidationConfidence.VALIDATED,
        customization_status=(
            "Official read-only baseline. Duplicate to a custom profile before timing tuning."
        ),
        editable_fields=(),
    ),
}


def get_profile_metadata(profile_id: str) -> ProfileMetadata:
    return PROFILE_METADATA[profile_id]


def get_all_profile_metadata() -> list[ProfileMetadata]:
    return list(PROFILE_METADATA.values())


def get_profile_metadata_for_automation(automation_type: str) -> list[ProfileMetadata]:
    return [
        metadata
        for metadata in PROFILE_METADATA.values()
        if metadata.automation_type == automation_type
    ]
