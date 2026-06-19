"""Offline licensing foundation for Forza Automation Assist."""

from licensing.entitlements import COMMUNITY_AUTO1_MAX_RUNS, community_entitlements
from licensing.execution_boundary import (
    EntitlementDeniedError,
    ExecutionEntitlementService,
    consume_auto1_execution_entitlement,
    require_execution_entitlement,
)
from licensing.models import (
    EntitlementDecision,
    EntitlementProfile,
    LicenseImportResult,
    LicensePayload,
    LicenseState,
    SignedLicense,
)
from licensing.service import LicenseService

__all__ = [
    "COMMUNITY_AUTO1_MAX_RUNS",
    "EntitlementDecision",
    "EntitlementDeniedError",
    "EntitlementProfile",
    "ExecutionEntitlementService",
    "LicenseImportResult",
    "LicensePayload",
    "LicenseService",
    "LicenseState",
    "SignedLicense",
    "community_entitlements",
    "consume_auto1_execution_entitlement",
    "require_execution_entitlement",
]
