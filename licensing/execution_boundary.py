"""Reusable fail-closed entitlement checks for guarded real-input boundaries."""

from typing import Protocol

from licensing.models import EntitlementDecision
from licensing.service import LicenseService


class EntitlementDeniedError(PermissionError):
    """Raised before real input when the current entitlement refuses execution."""


class ExecutionEntitlementService(Protocol):
    def evaluate_execution(
        self,
        automation_id: str,
        mode: str | None = None,
        requested_count: int | None = None,
    ) -> EntitlementDecision: ...


def require_execution_entitlement(
    automation_id: str,
    mode: str | None = None,
    requested_count: int | None = None,
    license_service: ExecutionEntitlementService | None = None,
) -> EntitlementDecision:
    service = license_service or LicenseService()
    if requested_count is None:
        decision = service.evaluate_execution(automation_id, mode)
    else:
        decision = service.evaluate_execution(automation_id, mode, requested_count)
    if not decision.allowed:
        raise EntitlementDeniedError(decision.message)
    return decision
