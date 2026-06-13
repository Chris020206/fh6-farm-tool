from dataclasses import dataclass, field
from enum import Enum


class AcknowledgementLevel(str, Enum):
    NONE = "none"
    STANDARD = "standard"
    HEIGHTENED = "heightened"
    DOUBLE_CONFIRMATION = "double_confirmation"


@dataclass(frozen=True)
class ReadinessModel:
    automation_id: str
    expected_baseline: str
    manual_positioning_assumption: str
    recommended_setup: tuple[str, ...]
    focus_requirement: str
    cursor_requirement: str | None
    acknowledgement_level: AcknowledgementLevel
    readiness_wording: str
    confidence_notes: tuple[str, ...] = field(default_factory=tuple)
    contextual_warnings: tuple[str, ...] = field(default_factory=tuple)
    blocked_or_refused_conditions: tuple[str, ...] = field(default_factory=tuple)
