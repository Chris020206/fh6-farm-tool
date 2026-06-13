from dataclasses import dataclass, field

from product.risk_levels import RiskLevel


@dataclass(frozen=True)
class AutomationDefinition:
    automation_id: str
    display_name: str
    short_purpose: str
    long_purpose: str
    risk_level: RiskLevel
    validated_scope: str
    expected_baseline: str
    available_profiles: list[str] = field(default_factory=list)
    supported_modes: list[str] = field(default_factory=list)
    package_tier: str = "basic"
    maturity_status: str = "validated"
    contextual_warnings: list[str] = field(default_factory=list)
    suggested_next_step: str | None = None
    is_active: bool = True
