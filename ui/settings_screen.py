"""Product-facing structure for the locked desktop Settings screen."""

from dataclasses import dataclass
from enum import Enum

from licensing.constants import (
    FEATURE_AUTO1_FULL,
    FEATURE_AUTO1_UNLIMITED,
    FEATURE_AUTO2_FULL,
    FEATURE_AUTO2_NAVIGATION_TEST,
    FEATURE_AUTO3_FULL,
    FEATURE_AUTO3_NAVIGATION_TEST,
    FEATURE_PROFILES_BASIC,
    FEATURE_PROFILES_PLUS,
)
from licensing.entitlements import community_entitlements
from licensing.models import LicenseState
from product.support import OFFICIAL_DISCORD_URL
from settings.execution_preferences import ExecutionPreferences


class SettingsSectionId(str, Enum):
    LICENSE_AND_EDITION = "license_and_edition"
    EXECUTION = "execution"
    ABOUT = "about"


@dataclass(frozen=True)
class EditionFeature:
    feature_id: str
    label: str


@dataclass(frozen=True)
class LicenseStatusItem:
    label: str
    value: str


@dataclass(frozen=True)
class LicenseAndEditionSection:
    section_id: SettingsSectionId
    edition_name: str
    description: str
    included_features: tuple[EditionFeature, ...]
    status_items: tuple[LicenseStatusItem, ...]
    is_primary: bool = True


@dataclass(frozen=True)
class ExecutionSafetySetting:
    setting_id: str
    label: str
    description: str
    enabled: bool


@dataclass(frozen=True)
class ExecutionSection:
    section_id: SettingsSectionId
    title: str
    description: str
    settings: tuple[ExecutionSafetySetting, ...]


@dataclass(frozen=True)
class AboutSection:
    section_id: SettingsSectionId
    product: str
    version: str
    edition_name: str
    platform: str
    discord_url: str
    is_secondary: bool = True


@dataclass(frozen=True)
class SettingsScreen:
    primary_intention: str
    license_and_edition: LicenseAndEditionSection
    execution: ExecutionSection
    about: AboutSection


def build_settings_screen(
    license_state: LicenseState | None = None,
    *,
    version: str = "v0.2.0-beta",
    execution_preferences: ExecutionPreferences | None = None,
) -> SettingsScreen:
    license_state = license_state or LicenseState(
        status="community",
        entitlements=community_entitlements(),
        message="Community Edition is active.",
    )
    execution_preferences = execution_preferences or ExecutionPreferences()
    edition_name = product_facing_edition_name(license_state.entitlements.edition)
    return SettingsScreen(
        primary_intention=(
            "Review your edition, execution safety preferences, and product information."
        ),
        license_and_edition=LicenseAndEditionSection(
            section_id=SettingsSectionId.LICENSE_AND_EDITION,
            edition_name=edition_name,
            description=(
                "Your current edition determines which automation features are available "
                "in FAA. Manage your license below."
            ),
            included_features=_included_features(license_state),
            status_items=_status_items(license_state, edition_name),
        ),
        execution=ExecutionSection(
            section_id=SettingsSectionId.EXECUTION,
            title="Execution Safety",
            description=(
                "Configure confirmation dialogs shown before resource-spending "
                "automation modes."
            ),
            settings=(
                ExecutionSafetySetting(
                    setting_id="show_auto2_purchase_confirmation",
                    label="Show Auto2 Purchase confirmation",
                    description=(
                        "Warn before Auto2 Purchase Mode spends in-game credits."
                    ),
                    enabled=execution_preferences.show_auto2_purchase_confirmation,
                ),
                ExecutionSafetySetting(
                    setting_id="show_auto3_unlock_confirmation",
                    label="Show Auto3 Unlock confirmation",
                    description="Warn before Auto3 Unlock Mode spends Skill Points.",
                    enabled=execution_preferences.show_auto3_unlock_confirmation,
                ),
            ),
        ),
        about=AboutSection(
            section_id=SettingsSectionId.ABOUT,
            product="FAA Desktop",
            version=version,
            edition_name=edition_name,
            platform="Windows",
            discord_url=OFFICIAL_DISCORD_URL,
        ),
    )


def product_facing_edition_name(edition: str) -> str:
    names = {
        "community": "Community Edition",
        "basic": "Basic Edition",
        "plus": "Plus Edition",
        "founding": "Founding Tester Edition",
        "developer_admin": "Developer/Admin Edition",
    }
    return names.get(edition, "Community Edition")


def version_information_text(about: AboutSection) -> str:
    return (
        f"{about.product}\n"
        f"Version: {about.version}\n"
        f"Edition: {about.edition_name}\n"
        f"Platform: {about.platform}"
    )


def _included_features(state: LicenseState) -> tuple[EditionFeature, ...]:
    entitlements = state.entitlements
    features: list[EditionFeature] = []

    if entitlements.allows(FEATURE_AUTO1_UNLIMITED):
        features.append(EditionFeature(FEATURE_AUTO1_UNLIMITED, "Auto1 Unlimited"))
    elif entitlements.allows(FEATURE_AUTO1_FULL):
        features.append(EditionFeature(FEATURE_AUTO1_FULL, "Auto1 Community"))

    if entitlements.allows(FEATURE_AUTO2_FULL):
        features.append(EditionFeature(FEATURE_AUTO2_FULL, "Auto2 Full Automation"))
    elif entitlements.allows(FEATURE_AUTO2_NAVIGATION_TEST):
        features.append(
            EditionFeature(FEATURE_AUTO2_NAVIGATION_TEST, "Auto2 Navigation Test")
        )

    if entitlements.allows(FEATURE_AUTO3_FULL):
        features.append(EditionFeature(FEATURE_AUTO3_FULL, "Auto3 Full Automation"))
    elif entitlements.allows(FEATURE_AUTO3_NAVIGATION_TEST):
        features.append(
            EditionFeature(FEATURE_AUTO3_NAVIGATION_TEST, "Auto3 Navigation Test")
        )

    if entitlements.allows(FEATURE_PROFILES_PLUS):
        features.append(EditionFeature(FEATURE_PROFILES_PLUS, "Plus Profile Library"))
    elif entitlements.allows(FEATURE_PROFILES_BASIC):
        features.append(EditionFeature(FEATURE_PROFILES_BASIC, "Basic Profiles"))

    return tuple(features)


def _status_items(
    state: LicenseState,
    edition_name: str,
) -> tuple[LicenseStatusItem, ...]:
    if state.is_licensed:
        expires_at = state.license.payload.expires_at
        access = "Lifetime" if expires_at is None else f"Until {expires_at.date().isoformat()}"
        status = "Licensed"
        license_type = "Offline"
    else:
        access = "Community access"
        status = "No license required" if state.status == "community" else "Community fallback"
        license_type = "No license required"

    return (
        LicenseStatusItem("Status", status),
        LicenseStatusItem("Edition", edition_name),
        LicenseStatusItem("Access", access),
        LicenseStatusItem("License Type", license_type),
    )
