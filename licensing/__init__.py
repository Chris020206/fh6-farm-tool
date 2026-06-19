"""Offline licensing foundation for Forza Automation Assist."""

from licensing.entitlements import COMMUNITY_AUTO1_MAX_RUNS, community_entitlements
from licensing.execution_boundary import EntitlementDeniedError, require_execution_entitlement
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
    "LicenseImportResult",
    "LicensePayload",
    "LicenseService",
    "LicenseState",
    "SignedLicense",
    "community_entitlements",
    "require_execution_entitlement",
]
