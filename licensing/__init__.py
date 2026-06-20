"""Offline licensing foundation for Forza Automation Assist."""

from licensing.entitlements import (
    COMMUNITY_AUTO1_MAX_LOOPS_PER_EXECUTION,
    LICENSED_AUTO1_MAX_LOOPS_PER_EXECUTION,
    community_entitlements,
)
from licensing.execution_boundary import (
    EntitlementDeniedError,
    ExecutionEntitlementService,
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
    "COMMUNITY_AUTO1_MAX_LOOPS_PER_EXECUTION",
    "EntitlementDecision",
    "EntitlementDeniedError",
    "EntitlementProfile",
    "ExecutionEntitlementService",
    "LicenseImportResult",
    "LicensePayload",
    "LicenseService",
    "LicenseState",
    "LICENSED_AUTO1_MAX_LOOPS_PER_EXECUTION",
    "SignedLicense",
    "community_entitlements",
    "require_execution_entitlement",
]
