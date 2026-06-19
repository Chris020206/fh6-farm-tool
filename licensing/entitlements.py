"""Edition-independent feature claims and Community Edition defaults."""

from licensing.constants import (
    FEATURE_AUTO1_FULL,
    FEATURE_AUTO2_NAVIGATION_TEST,
    FEATURE_AUTO3_NAVIGATION_TEST,
    LIMIT_AUTO1_MAX_RUNS,
)
from licensing.models import EntitlementProfile, SignedLicense


COMMUNITY_AUTO1_MAX_RUNS = 5


def community_entitlements() -> EntitlementProfile:
    return EntitlementProfile(
        edition="community",
        features=frozenset(
            {
                FEATURE_AUTO1_FULL,
                FEATURE_AUTO2_NAVIGATION_TEST,
                FEATURE_AUTO3_NAVIGATION_TEST,
            }
        ),
        limits={LIMIT_AUTO1_MAX_RUNS: COMMUNITY_AUTO1_MAX_RUNS},
    )


def entitlements_from_license(signed_license: SignedLicense) -> EntitlementProfile:
    payload = signed_license.payload
    return EntitlementProfile(
        edition=payload.edition,
        features=payload.features,
        limits=payload.limits,
        license_id=payload.license_id,
    )
