from dataclasses import dataclass
from enum import Enum


class SidebarDestinationId(str, Enum):
    HOME = "home"
    AUTOMATION_ENVIRONMENT = "automation_environment"
    PROFILES = "profiles"
    HISTORY = "history"
    HELP = "help"
    SETTINGS = "settings"


class ScreenId(str, Enum):
    HOME = "home"
    AUTOMATION_ENVIRONMENT = "automation_environment"
    HISTORY = "history"
    PROFILES = "profiles"
    HELP = "help"
    SETTINGS = "settings"


class ScreenType(str, Enum):
    OPERATIONAL_FOCUS = "operational_focus"
    OPERATIONAL_MEMORY = "operational_memory"
    TRUST_SELECTION = "trust_selection"
    CONFIDENCE_SUPPORT = "confidence_support"
    SYSTEM_CONTROL = "system_control"


class ZoneRole(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"


@dataclass(frozen=True)
class SidebarDestination:
    destination_id: SidebarDestinationId
    label: str
    screen_id: ScreenId
    purpose: str


@dataclass(frozen=True)
class ContentZone:
    role: ZoneRole
    purpose: str


@dataclass(frozen=True)
class WeightedContentZones:
    primary: ContentZone
    secondary: ContentZone
    tertiary: ContentZone

    def as_tuple(self) -> tuple[ContentZone, ContentZone, ContentZone]:
        return (self.primary, self.secondary, self.tertiary)


@dataclass(frozen=True)
class ScreenDescriptor:
    screen_id: ScreenId
    title: str
    screen_type: ScreenType
    primary_intention: str
    zones: WeightedContentZones


@dataclass(frozen=True)
class AppShell:
    sidebar_destinations: tuple[SidebarDestination, ...]
    screen_descriptors: tuple[ScreenDescriptor, ...]
    default_screen_id: ScreenId


SIDEBAR_DESTINATIONS: tuple[SidebarDestination, ...] = (
    SidebarDestination(
        destination_id=SidebarDestinationId.HOME,
        label="Home",
        screen_id=ScreenId.HOME,
        purpose="Focused launch environment for automation intent.",
    ),
    SidebarDestination(
        destination_id=SidebarDestinationId.AUTOMATION_ENVIRONMENT,
        label="Automation Environment",
        screen_id=ScreenId.AUTOMATION_ENVIRONMENT,
        purpose="Prepare and review a supervised operation.",
    ),
    SidebarDestination(
        destination_id=SidebarDestinationId.HISTORY,
        label="History",
        screen_id=ScreenId.HISTORY,
        purpose="Operational memory and post-run clarity.",
    ),
    SidebarDestination(
        destination_id=SidebarDestinationId.HELP,
        label="Help",
        screen_id=ScreenId.HELP,
        purpose="Confidence support for common operator uncertainty.",
    ),
    SidebarDestination(
        destination_id=SidebarDestinationId.SETTINGS,
        label="Settings",
        screen_id=ScreenId.SETTINGS,
        purpose="Quiet system-level control.",
    ),
)


SCREEN_DESCRIPTORS: tuple[ScreenDescriptor, ...] = (
    ScreenDescriptor(
        screen_id=ScreenId.HOME,
        title="Home",
        screen_type=ScreenType.OPERATIONAL_FOCUS,
        primary_intention="Show automations as the product and orient launch intent.",
        zones=WeightedContentZones(
            primary=ContentZone(
                role=ZoneRole.PRIMARY,
                purpose="Automation destinations and current operational focus.",
            ),
            secondary=ContentZone(
                role=ZoneRole.SECONDARY,
                purpose="Recent run reassurance and readiness reminders.",
            ),
            tertiary=ContentZone(
                role=ZoneRole.TERTIARY,
                purpose="Low-priority continuity details.",
            ),
        ),
    ),
    ScreenDescriptor(
        screen_id=ScreenId.AUTOMATION_ENVIRONMENT,
        title="Automation Environment",
        screen_type=ScreenType.OPERATIONAL_FOCUS,
        primary_intention="Build confidence before a specific automation run.",
        zones=WeightedContentZones(
            primary=ContentZone(
                role=ZoneRole.PRIMARY,
                purpose="Automation overview, quick settings, readiness, and run commitment.",
            ),
            secondary=ContentZone(
                role=ZoneRole.SECONDARY,
                purpose="Supporting confidence notes.",
            ),
            tertiary=ContentZone(
                role=ZoneRole.TERTIARY,
                purpose="Advanced or refinement details that do not dominate the screen.",
            ),
        ),
    ),
    ScreenDescriptor(
        screen_id=ScreenId.HISTORY,
        title="Operational History",
        screen_type=ScreenType.OPERATIONAL_MEMORY,
        primary_intention="Recent operational history and session outcomes.",
        zones=WeightedContentZones(
            primary=ContentZone(
                role=ZoneRole.PRIMARY,
                purpose="Recent operational session summaries.",
            ),
            secondary=ContentZone(
                role=ZoneRole.SECONDARY,
                purpose="Outcome context, confidence notes, and recovery guidance.",
            ),
            tertiary=ContentZone(
                role=ZoneRole.TERTIARY,
                purpose="Expandable session details without raw log dominance.",
            ),
        ),
    ),
    ScreenDescriptor(
        screen_id=ScreenId.HELP,
        title="Help",
        screen_type=ScreenType.CONFIDENCE_SUPPORT,
        primary_intention="Reduce uncertainty through concise operational guidance.",
        zones=WeightedContentZones(
            primary=ContentZone(
                role=ZoneRole.PRIMARY,
                purpose="Common operator questions and baseline expectations.",
            ),
            secondary=ContentZone(
                role=ZoneRole.SECONDARY,
                purpose="Automation-specific guidance and result meanings.",
            ),
            tertiary=ContentZone(
                role=ZoneRole.TERTIARY,
                purpose="Additional support references.",
            ),
        ),
    ),
    ScreenDescriptor(
        screen_id=ScreenId.SETTINGS,
        title="Settings",
        screen_type=ScreenType.SYSTEM_CONTROL,
        primary_intention=(
            "Review your edition, execution safety preferences, and product information."
        ),
        zones=WeightedContentZones(
            primary=ContentZone(
                role=ZoneRole.PRIMARY,
                purpose="Appearance, window behavior, and system preferences.",
            ),
            secondary=ContentZone(
                role=ZoneRole.SECONDARY,
                purpose="Safety and notification preferences.",
            ),
            tertiary=ContentZone(
                role=ZoneRole.TERTIARY,
                purpose="Future advanced system controls.",
            ),
        ),
    ),
)


APP_SHELL = AppShell(
    sidebar_destinations=SIDEBAR_DESTINATIONS,
    screen_descriptors=SCREEN_DESCRIPTORS,
    default_screen_id=ScreenId.HOME,
)


def get_sidebar_destinations() -> tuple[SidebarDestination, ...]:
    return SIDEBAR_DESTINATIONS


def get_screen_descriptors() -> tuple[ScreenDescriptor, ...]:
    return SCREEN_DESCRIPTORS


def get_screen_descriptor(screen_id: ScreenId) -> ScreenDescriptor:
    for screen_descriptor in SCREEN_DESCRIPTORS:
        if screen_descriptor.screen_id == screen_id:
            return screen_descriptor

    raise KeyError(screen_id)
