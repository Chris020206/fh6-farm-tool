from dataclasses import dataclass
from enum import Enum


class SettingsSectionId(str, Enum):
    EXPECTED_APPLICATION_BEHAVIOR = "expected_application_behavior"
    SAFETY_AND_OPERATIONAL_PREFERENCES = "safety_and_operational_preferences"
    ADVANCED_SYSTEM_PREFERENCES = "advanced_system_preferences"


class SettingCategory(str, Enum):
    APPEARANCE = "appearance"
    NOTIFICATIONS = "notifications"
    STARTUP = "startup"
    WINDOW = "window"
    SAFETY = "safety"
    CONFIRMATION = "confirmation"
    SYSTEM = "system"


class SettingImportance(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"


@dataclass(frozen=True)
class SettingItem:
    setting_id: str
    label: str
    description: str
    category: SettingCategory
    importance: SettingImportance
    is_editable_now: bool = False


@dataclass(frozen=True)
class ExpectedApplicationBehaviorSection:
    section_id: SettingsSectionId
    purpose: str
    settings: tuple[SettingItem, ...]
    is_primary: bool = True


@dataclass(frozen=True)
class SafetyAndOperationalPreferencesSection:
    section_id: SettingsSectionId
    purpose: str
    settings: tuple[SettingItem, ...]
    is_secondary: bool = True


@dataclass(frozen=True)
class AdvancedSystemPreferencesSection:
    section_id: SettingsSectionId
    purpose: str
    settings: tuple[SettingItem, ...]
    is_tertiary: bool = True


@dataclass(frozen=True)
class SettingsScreen:
    primary_intention: str
    expected_application_behavior: ExpectedApplicationBehaviorSection
    safety_and_operational_preferences: SafetyAndOperationalPreferencesSection
    advanced_system_preferences: AdvancedSystemPreferencesSection


def build_settings_screen() -> SettingsScreen:
    return SettingsScreen(
        primary_intention="Control application-level behavior without editing automation execution.",
        expected_application_behavior=ExpectedApplicationBehaviorSection(
            section_id=SettingsSectionId.EXPECTED_APPLICATION_BEHAVIOR,
            purpose="Primary system behavior settings for how the app presents and starts.",
            settings=_build_expected_application_behavior_settings(),
        ),
        safety_and_operational_preferences=SafetyAndOperationalPreferencesSection(
            section_id=SettingsSectionId.SAFETY_AND_OPERATIONAL_PREFERENCES,
            purpose="Secondary safety preferences that support guarded manual operation.",
            settings=_build_safety_settings(),
        ),
        advanced_system_preferences=AdvancedSystemPreferencesSection(
            section_id=SettingsSectionId.ADVANCED_SYSTEM_PREFERENCES,
            purpose="Tertiary future system preferences that should remain quiet.",
            settings=_build_advanced_system_settings(),
        ),
    )


def _build_expected_application_behavior_settings() -> tuple[SettingItem, ...]:
    return (
        SettingItem(
            setting_id="theme",
            label="Theme",
            description="Expected visual preference for the application shell.",
            category=SettingCategory.APPEARANCE,
            importance=SettingImportance.PRIMARY,
        ),
        SettingItem(
            setting_id="notifications",
            label="Notifications",
            description="Expected notification behavior for calm operational updates.",
            category=SettingCategory.NOTIFICATIONS,
            importance=SettingImportance.PRIMARY,
        ),
        SettingItem(
            setting_id="startup_behavior",
            label="Startup Behavior",
            description="Expected app startup posture without launching automation.",
            category=SettingCategory.STARTUP,
            importance=SettingImportance.PRIMARY,
        ),
        SettingItem(
            setting_id="window_behavior",
            label="Window Behavior",
            description="Expected window and companion-mode presentation behavior.",
            category=SettingCategory.WINDOW,
            importance=SettingImportance.PRIMARY,
        ),
    )


def _build_safety_settings() -> tuple[SettingItem, ...]:
    return (
        SettingItem(
            setting_id="emergency_stop_visibility",
            label="Emergency Stop Visibility",
            description="Expected visibility of stop guidance during guarded operation.",
            category=SettingCategory.SAFETY,
            importance=SettingImportance.SECONDARY,
        ),
        SettingItem(
            setting_id="confirmation_preferences",
            label="Confirmation Preferences",
            description="Expected handling for risk-sensitive confirmation reminders.",
            category=SettingCategory.CONFIRMATION,
            importance=SettingImportance.SECONDARY,
        ),
    )


def _build_advanced_system_settings() -> tuple[SettingItem, ...]:
    return (
        SettingItem(
            setting_id="update_behavior",
            label="Update Behavior",
            description="Future system-level update preference placeholder.",
            category=SettingCategory.SYSTEM,
            importance=SettingImportance.TERTIARY,
        ),
        SettingItem(
            setting_id="environment_detection",
            label="Environment Detection",
            description="Future system-level environment awareness placeholder.",
            category=SettingCategory.SYSTEM,
            importance=SettingImportance.TERTIARY,
        ),
    )
