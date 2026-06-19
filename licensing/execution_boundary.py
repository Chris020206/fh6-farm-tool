"""Reusable fail-closed entitlement checks for guarded real-input boundaries."""

from licensing.models import EntitlementDecision
from licensing.service import LicenseService


class EntitlementDeniedError(PermissionError):
    """Raised before real input when the current entitlement refuses execution."""


def require_execution_entitlement(
    automation_id: str,
    mode: str | None = None,
    license_service: LicenseService | None = None,
) -> EntitlementDecision:
    service = license_service or LicenseService()
    decision = service.check_execution(automation_id, mode)
    if not decision.allowed:
        raise EntitlementDeniedError(decision.message)
    return decision
