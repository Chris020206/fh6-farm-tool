"""Locked licensing identifiers shared by desktop verification and gating."""

PRODUCT_ID = "forza_automation_assist"
SUPPORTED_LICENSE_VERSION = 1
DEFAULT_SIGNING_KEY_ID = "FAA_KEY_2026_01"

FEATURE_AUTO1_FULL = "FAA.Auto1.Full"
FEATURE_AUTO1_UNLIMITED = "FAA.Auto1.Unlimited"
FEATURE_AUTO2_NAVIGATION_TEST = "FAA.Auto2.NavigationTest"
FEATURE_AUTO2_FULL = "FAA.Auto2.Full"
FEATURE_AUTO3_NAVIGATION_TEST = "FAA.Auto3.NavigationTest"
FEATURE_AUTO3_FULL = "FAA.Auto3.Full"
FEATURE_AUTO4_FULL = "FAA.Auto4.Full"
FEATURE_PROFILES_BASIC = "FAA.Profiles.Basic"
FEATURE_PROFILES_PLUS = "FAA.Profiles.Plus"

LIMIT_AUTO1_MAX_RUNS = "FAA.Auto1.MaxRuns"

SUPPORTED_EDITIONS = frozenset(
    {"basic", "plus", "founding", "developer_admin"}
)

EDITION_RANKS = {
    "community": 0,
    "basic": 1,
    "plus": 2,
    "founding": 3,
    "developer_admin": 4,
}
