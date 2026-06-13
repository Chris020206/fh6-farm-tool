from dataclasses import dataclass, field
from enum import Enum


class RecommendationStatus(str, Enum):
    CURATED = "curated"
    SUPPORTED = "supported"
    CUSTOM = "custom"
    EXPERIMENTAL = "experimental"


class PackageTier(str, Enum):
    BASIC = "basic"
    PLUS = "plus"


class ValidationConfidence(str, Enum):
    VALIDATED = "validated"
    CONTROLLED = "controlled"
    UNVALIDATED = "unvalidated"


@dataclass(frozen=True)
class ProfileMetadata:
    profile_id: str
    profile_name: str
    automation_type: str
    recommendation_status: RecommendationStatus
    package_tier: PackageTier
    behavior_summary: str
    reliability_posture: str
    intended_usage: str
    validation_confidence: ValidationConfidence
    customization_status: str
    editable_fields: tuple[str, ...] = field(default_factory=tuple)
    hidden_technical_sections: tuple[str, ...] = field(
        default_factory=lambda: ("keys", "timings", "navigation_counts")
    )
