from dataclasses import dataclass
from enum import Enum

from frontend.automation_controller import (
    AutomationRunRequest,
    FrontendAutomationController,
)
from product.automation_registry import get_automation_definition
from product.profile_metadata_registry import get_profile_metadata
from product.readiness_registry import get_readiness_model
from ui.automation_environment import (
    AdvancedSection,
    AutomationEnvironmentScreen,
    AutomationEnvironmentSectionId,
    ContextualWarningsSection,
    OverviewSection,
    ProfileSection,
    ReadinessSection,
    RunSection,
    build_automation_environment_screen,
)
from ui.shell import (
    ScreenDescriptor,
    ScreenId,
    SidebarDestination,
    ZoneRole,
    get_screen_descriptor,
    get_sidebar_destinations,
)


@dataclass(frozen=True)
class PrototypeZone:
    role: ZoneRole
    purpose: str


@dataclass(frozen=True)
class PrototypeScreen:
    screen_id: ScreenId
    title: str
    primary_intention: str
    zones: tuple[PrototypeZone, PrototypeZone, PrototypeZone]


@dataclass(frozen=True)
class PrototypeAutomationEnvironmentSection:
    section_id: AutomationEnvironmentSectionId
    title: str
    summary: str
    details: tuple[str, ...]
    zone_role: ZoneRole
    is_collapsed_feeling: bool = False


@dataclass(frozen=True)
class PrototypeAutomationEnvironment:
    title: str
    primary_intention: str
    sections: tuple[PrototypeAutomationEnvironmentSection, ...]


@dataclass(frozen=True)
class PrototypeHomeSignal:
    title: str
    summary: str
    zone_role: ZoneRole


@dataclass(frozen=True)
class PrototypeHomeConcept:
    title: str
    philosophy_statement: str
    opening_feel: str
    is_single_frame: bool
    is_dashboard_like: bool
    signals: tuple[PrototypeHomeSignal, ...]


@dataclass(frozen=True)
class PrototypeSidebarComposition:
    navigation_block_label: str
    footer_status: str
    footer_detail: str
    is_compact_navigation: bool
    has_structural_closure: bool


class PrototypeNavigationRailMode(str, Enum):
    TOGGLE = "toggle"
    HOVER = "hover"


@dataclass(frozen=True)
class PrototypeNavigationRail:
    collapsed_width: int
    expanded_width: int
    default_mode: PrototypeNavigationRailMode
    supported_modes: tuple[PrototypeNavigationRailMode, ...]
    is_miniature: bool
    is_low_emphasis: bool


@dataclass(frozen=True)
class PrototypeShellSpec:
    window_title: str
    window_width: int
    window_height: int
    is_fixed_size: bool
    sidebar_destinations: tuple[SidebarDestination, ...]
    screens: tuple[PrototypeScreen, ...]
    automation_environment: PrototypeAutomationEnvironment
    home_concept: PrototypeHomeConcept
    sidebar_composition: PrototypeSidebarComposition
    navigation_rail: PrototypeNavigationRail


def build_prototype_shell_spec() -> PrototypeShellSpec:
    sidebar_destinations = get_sidebar_destinations()

    return PrototypeShellSpec(
        window_title="FH6 Farm Tool - PySide6 Shell Prototype",
        window_width=640,
        window_height=768,
        is_fixed_size=True,
        sidebar_destinations=sidebar_destinations,
        screens=tuple(
            _build_prototype_screen(get_screen_descriptor(destination.screen_id))
            for destination in sidebar_destinations
        ),
        automation_environment=_build_prototype_automation_environment(),
        home_concept=_build_prototype_home_concept(),
        sidebar_composition=_build_prototype_sidebar_composition(),
        navigation_rail=_build_prototype_navigation_rail(),
    )


def launch_pyside6_shell_prototype(
    navigation_mode: PrototypeNavigationRailMode = PrototypeNavigationRailMode.TOGGLE,
) -> int:
    try:
        from PySide6.QtWidgets import (
            QApplication,
            QFrame,
            QGroupBox,
            QHBoxLayout,
            QLabel,
            QListWidget,
            QListWidgetItem,
            QMainWindow,
            QPushButton,
            QSizePolicy,
            QStackedWidget,
            QVBoxLayout,
            QWidget,
        )
    except ImportError as error:
        raise SystemExit(
            "PySide6 is not installed. Install PySide6 before launching the prototype."
        ) from error

    import sys

    shell_spec = build_prototype_shell_spec()
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle(shell_spec.window_title)
    window.setFixedSize(shell_spec.window_width, shell_spec.window_height)

    root = QWidget()
    root_layout = QHBoxLayout(root)

    nav_container = QWidget()
    nav_container.setFixedWidth(shell_spec.navigation_rail.collapsed_width)
    nav_container.setSizePolicy(
        QSizePolicy.Policy.Fixed,
        QSizePolicy.Policy.Expanding,
    )
    nav_layout = QVBoxLayout(nav_container)
    nav_label = QLabel(shell_spec.sidebar_composition.navigation_block_label)
    nav_layout.addWidget(nav_label)

    nav_toggle = QPushButton(">")
    if navigation_mode == PrototypeNavigationRailMode.TOGGLE:
        nav_layout.addWidget(nav_toggle)

    nav_list = QListWidget()
    nav_list.setFixedHeight(190)
    nav_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    stacked_screens = QStackedWidget()

    for screen in shell_spec.screens:
        item = QListWidgetItem(screen.title)
        item.setData(256, screen.screen_id.value)
        nav_list.addItem(item)
        stacked_screens.addWidget(
            _build_screen_widget(
                screen,
                home_concept=shell_spec.home_concept
                if screen.screen_id == ScreenId.HOME
                else None,
                open_automation_environment=(
                    lambda: stacked_screens.setCurrentIndex(len(shell_spec.screens))
                )
                if screen.screen_id == ScreenId.HOME
                else None,
            )
        )

    stacked_screens.addWidget(
        _build_automation_environment_widget(shell_spec.automation_environment)
    )

    nav_list.currentRowChanged.connect(stacked_screens.setCurrentIndex)
    nav_list.setCurrentRow(0)

    _set_navigation_rail_expanded(
        nav_container=nav_container,
        nav_list=nav_list,
        nav_label=nav_label,
        shell_spec=shell_spec,
        expanded=False,
    )

    if navigation_mode == PrototypeNavigationRailMode.TOGGLE:
        expanded_state = {"expanded": False}

        def toggle_navigation_rail() -> None:
            expanded_state["expanded"] = not expanded_state["expanded"]
            _set_navigation_rail_expanded(
                nav_container=nav_container,
                nav_list=nav_list,
                nav_label=nav_label,
                shell_spec=shell_spec,
                expanded=expanded_state["expanded"],
            )
            nav_toggle.setText("<" if expanded_state["expanded"] else ">")

        nav_toggle.clicked.connect(toggle_navigation_rail)

    if navigation_mode == PrototypeNavigationRailMode.HOVER:
        nav_container.enterEvent = lambda _event: _set_navigation_rail_expanded(
            nav_container=nav_container,
            nav_list=nav_list,
            nav_label=nav_label,
            shell_spec=shell_spec,
            expanded=True,
        )
        nav_container.leaveEvent = lambda _event: _set_navigation_rail_expanded(
            nav_container=nav_container,
            nav_list=nav_list,
            nav_label=nav_label,
            shell_spec=shell_spec,
            expanded=False,
        )

    nav_layout.addWidget(nav_list)
    nav_layout.addStretch()
    nav_layout.addWidget(QLabel(shell_spec.sidebar_composition.footer_status))
    nav_layout.addWidget(QLabel(shell_spec.sidebar_composition.footer_detail))

    root_layout.addWidget(nav_container)
    root_layout.addWidget(_vertical_separator(QFrame))
    root_layout.addWidget(stacked_screens)

    window.setCentralWidget(root)
    window.show()

    return app.exec()


def _build_prototype_screen(screen_descriptor: ScreenDescriptor) -> PrototypeScreen:
    return PrototypeScreen(
        screen_id=screen_descriptor.screen_id,
        title=screen_descriptor.title,
        primary_intention=screen_descriptor.primary_intention,
        zones=tuple(
            PrototypeZone(role=zone.role, purpose=zone.purpose)
            for zone in screen_descriptor.zones.as_tuple()
        ),
    )


def _build_prototype_automation_environment() -> PrototypeAutomationEnvironment:
    controller = FrontendAutomationController(
        session_id_provider=lambda: "prototype-preview-session",
    )
    run_plan = controller.prepare_run_plan(
        AutomationRunRequest(
            automation_id="auto1",
            profile_id="auto1_race_default",
            requested_count=1,
        )
    )
    automation_environment_screen = build_automation_environment_screen(
        automation_definition=get_automation_definition("auto1"),
        profile_metadata=get_profile_metadata("auto1_race_default"),
        readiness_model=get_readiness_model("auto1"),
        run_plan=run_plan,
    )

    return _build_automation_environment_prototype_screen(
        automation_environment_screen
    )


def _build_automation_environment_prototype_screen(
    screen: AutomationEnvironmentScreen,
) -> PrototypeAutomationEnvironment:
    return PrototypeAutomationEnvironment(
        title="Automation Environment",
        primary_intention="Orientation -> Confidence Formation -> Commitment",
        sections=tuple(_build_automation_section(section) for section in screen.sections),
    )


def _build_automation_section(
    section: (
        OverviewSection
        | ProfileSection
        | ReadinessSection
        | ContextualWarningsSection
        | AdvancedSection
        | RunSection
    ),
) -> PrototypeAutomationEnvironmentSection:
    if isinstance(section, OverviewSection):
        return PrototypeAutomationEnvironmentSection(
            section_id=section.section_id,
            title="Overview",
            summary=section.display_name,
            details=(
                section.short_purpose,
                section.validated_scope,
                section.expected_baseline,
            ),
            zone_role=ZoneRole.PRIMARY,
        )

    if isinstance(section, ProfileSection):
        return PrototypeAutomationEnvironmentSection(
            section_id=section.section_id,
            title="Profile",
            summary=section.profile_name,
            details=(
                section.behavior_summary,
                section.reliability_posture,
                section.customization_status,
            ),
            zone_role=ZoneRole.PRIMARY,
        )

    if isinstance(section, ReadinessSection):
        return PrototypeAutomationEnvironmentSection(
            section_id=section.section_id,
            title="Readiness",
            summary=section.readiness_wording,
            details=(
                section.expected_baseline,
                section.manual_positioning_assumption,
                section.focus_requirement,
            )
            + section.recommended_setup
            + section.confidence_notes,
            zone_role=ZoneRole.PRIMARY,
        )

    if isinstance(section, ContextualWarningsSection):
        return PrototypeAutomationEnvironmentSection(
            section_id=section.section_id,
            title="Contextual Warnings",
            summary="Warnings remain contextual and secondary.",
            details=section.warnings or ("No contextual warnings for this placeholder.",),
            zone_role=ZoneRole.SECONDARY,
        )

    if isinstance(section, AdvancedSection):
        return PrototypeAutomationEnvironmentSection(
            section_id=section.section_id,
            title="Advanced / Refinement",
            summary=section.purpose,
            details=section.available_refinements or ("Collapsed placeholder only.",),
            zone_role=ZoneRole.TERTIARY,
            is_collapsed_feeling=section.is_collapsed_by_default,
        )

    return PrototypeAutomationEnvironmentSection(
        section_id=section.section_id,
        title="Run",
        summary=section.commitment_message,
        details=(
            f"Status: {section.status_label}",
            f"Requested count: {section.requested_count}",
            f"Acknowledgement: {section.acknowledgement_level.value}",
        ),
        zone_role=ZoneRole.PRIMARY,
    )


def _build_prototype_home_concept() -> PrototypeHomeConcept:
    return PrototypeHomeConcept(
        title="Home",
        philosophy_statement="Quiet confidence before operational commitment.",
        opening_feel="A restrained launchpad with a slight premium control-room feeling.",
        is_single_frame=True,
        is_dashboard_like=False,
        signals=(
            PrototypeHomeSignal(
                title="Recommended Next Step",
                summary="Choose an automation only when the FH6 baseline is ready.",
                zone_role=ZoneRole.PRIMARY,
            ),
            PrototypeHomeSignal(
                title="Quick Automation Access",
                summary="Open the Automation Environment for focused preparation.",
                zone_role=ZoneRole.PRIMARY,
            ),
            PrototypeHomeSignal(
                title="Relevant Activity",
                summary="Recent operational context stays lightweight and reassuring.",
                zone_role=ZoneRole.SECONDARY,
            ),
            PrototypeHomeSignal(
                title="Quiet Status",
                summary="Controlled MVP ready for supervised developer/manual use.",
                zone_role=ZoneRole.TERTIARY,
            ),
        ),
    )


def _build_prototype_sidebar_composition() -> PrototypeSidebarComposition:
    return PrototypeSidebarComposition(
        navigation_block_label="FH6 Farm Tool",
        footer_status="Controlled MVP",
        footer_detail="Manual operation ready",
        is_compact_navigation=True,
        has_structural_closure=True,
    )


def _build_prototype_navigation_rail() -> PrototypeNavigationRail:
    return PrototypeNavigationRail(
        collapsed_width=72,
        expanded_width=168,
        default_mode=PrototypeNavigationRailMode.TOGGLE,
        supported_modes=(
            PrototypeNavigationRailMode.TOGGLE,
            PrototypeNavigationRailMode.HOVER,
        ),
        is_miniature=True,
        is_low_emphasis=True,
    )


def _set_navigation_rail_expanded(
    nav_container,
    nav_list,
    nav_label,
    shell_spec: PrototypeShellSpec,
    expanded: bool,
) -> None:
    nav_container.setFixedWidth(
        shell_spec.navigation_rail.expanded_width
        if expanded
        else shell_spec.navigation_rail.collapsed_width
    )
    nav_label.setText(
        shell_spec.sidebar_composition.navigation_block_label if expanded else "FH6"
    )

    for index, destination in enumerate(shell_spec.sidebar_destinations):
        nav_list.item(index).setText(destination.label if expanded else destination.label[:1])


def _build_screen_widget(
    screen: PrototypeScreen,
    home_concept: PrototypeHomeConcept | None = None,
    open_automation_environment=None,
):
    from PySide6.QtWidgets import QPushButton, QGroupBox, QLabel, QVBoxLayout, QWidget

    container = QWidget()
    layout = QVBoxLayout(container)
    layout.addWidget(QLabel(screen.title))
    layout.addWidget(QLabel(screen.primary_intention))

    if home_concept is not None:
        layout.addWidget(QLabel(home_concept.philosophy_statement))
        layout.addWidget(QLabel(home_concept.opening_feel))

        for signal in home_concept.signals:
            group_box = QGroupBox(f"{signal.zone_role.value.title()} - {signal.title}")
            signal_layout = QVBoxLayout(group_box)
            signal_layout.addWidget(QLabel(signal.summary))
            layout.addWidget(group_box)

    if open_automation_environment is not None:
        button = QPushButton("Open Automation Environment Prototype")
        button.clicked.connect(open_automation_environment)
        layout.addWidget(button)

    if home_concept is not None:
        return container

    for zone in screen.zones:
        group_box = QGroupBox(zone.role.value.title())
        zone_layout = QVBoxLayout(group_box)
        zone_layout.addWidget(QLabel(zone.purpose))
        layout.addWidget(group_box)

    return container


def _build_automation_environment_widget(
    automation_environment: PrototypeAutomationEnvironment,
):
    from PySide6.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QWidget

    container = QWidget()
    layout = QVBoxLayout(container)
    layout.addWidget(QLabel(automation_environment.title))
    layout.addWidget(QLabel(automation_environment.primary_intention))

    for section in automation_environment.sections:
        title = f"{section.zone_role.value.title()} - {section.title}"
        if section.is_collapsed_feeling:
            title = f"{title} (collapsed placeholder)"

        group_box = QGroupBox(title)
        section_layout = QVBoxLayout(group_box)
        section_layout.addWidget(QLabel(section.summary))

        for detail in section.details:
            section_layout.addWidget(QLabel(detail))

        layout.addWidget(group_box)

    return container


def _vertical_separator(frame_type):
    separator = frame_type()
    separator.setFrameShape(frame_type.Shape.VLine)
    separator.setFrameShadow(frame_type.Shadow.Sunken)
    return separator


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Launch the PySide6 vertical companion prototype."
    )
    parser.add_argument(
        "--navigation-mode",
        choices=tuple(mode.value for mode in PrototypeNavigationRailMode),
        default=PrototypeNavigationRailMode.TOGGLE.value,
        help="Prototype navigation rail behavior to compare.",
    )
    args = parser.parse_args()

    return launch_pyside6_shell_prototype(
        navigation_mode=PrototypeNavigationRailMode(args.navigation_mode)
    )


if __name__ == "__main__":
    raise SystemExit(main())
