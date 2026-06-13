from dataclasses import dataclass

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


@dataclass(frozen=True)
class PrototypeNavigationRail:
    collapsed_width: int
    expanded_width: int
    expansion_trigger: str
    animation_duration_ms: int
    item_height: int
    item_spacing: int
    active_state_treatment: str
    overlay_treatment: str
    footer_treatment: str
    is_miniature: bool
    is_low_emphasis: bool
    reserves_collapsed_space: bool
    overlays_main_content: bool
    reflows_main_content_on_hover: bool


@dataclass(frozen=True)
class PrototypeVerticalRhythm:
    content_margin: int
    header_spacing: int
    section_spacing: int
    group_spacing: int
    group_inner_margin: int
    important_element_spacing: int
    is_single_frame: bool
    introduces_scrolling: bool
    density_principle: str


@dataclass(frozen=True)
class PrototypeTypographyHierarchy:
    screen_title_size: int
    opening_statement_size: int
    section_title_size: int
    summary_size: int
    detail_size: int
    navigation_size: int
    footer_size: int
    active_navigation_weight: int
    secondary_detail_treatment: str
    hierarchy_principle: str


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
    vertical_rhythm: PrototypeVerticalRhythm
    typography: PrototypeTypographyHierarchy


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
        vertical_rhythm=_build_prototype_vertical_rhythm(),
        typography=_build_prototype_typography_hierarchy(),
    )


def launch_pyside6_shell_prototype() -> int:
    try:
        from PySide6.QtCore import QPropertyAnimation, QRect
        from PySide6.QtWidgets import (
            QApplication,
            QFrame,
            QGroupBox,
            QHBoxLayout,
            QLabel,
            QListWidget,
            QListWidgetItem,
            QMainWindow,
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
    root_layout.setContentsMargins(0, 0, 0, 0)
    root_layout.setSpacing(0)

    collapsed_rail = QWidget()
    collapsed_rail.setFixedWidth(shell_spec.navigation_rail.collapsed_width)
    collapsed_rail.setSizePolicy(
        QSizePolicy.Policy.Fixed,
        QSizePolicy.Policy.Expanding,
    )
    collapsed_rail.setStyleSheet(
        "background-color: #f5f5f2; border-right: 1px solid #d8d6cf;"
    )
    collapsed_rail_layout = QVBoxLayout(collapsed_rail)
    collapsed_rail_layout.setContentsMargins(8, 14, 8, 12)
    collapsed_rail_layout.setSpacing(12)
    collapsed_rail_label = QLabel("FH6")
    _style_navigation_label(collapsed_rail_label, shell_spec=shell_spec)
    collapsed_rail_layout.addWidget(collapsed_rail_label)

    collapsed_nav_list = QListWidget()
    collapsed_nav_list.setFixedHeight(230)
    collapsed_nav_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    _apply_navigation_list_refinement(
        collapsed_nav_list,
        shell_spec=shell_spec,
        collapsed=True,
    )

    main_area = QWidget()
    main_area_layout = QVBoxLayout(main_area)
    main_area_layout.setContentsMargins(
        shell_spec.vertical_rhythm.content_margin,
        shell_spec.vertical_rhythm.content_margin,
        shell_spec.vertical_rhythm.content_margin,
        shell_spec.vertical_rhythm.content_margin,
    )
    stacked_screens = QStackedWidget()
    main_area_layout.addWidget(stacked_screens)

    for screen in shell_spec.screens:
        item = QListWidgetItem(screen.title)
        item.setData(256, screen.screen_id.value)
        collapsed_item = QListWidgetItem(screen.title[:1])
        collapsed_item.setData(256, screen.screen_id.value)
        collapsed_nav_list.addItem(collapsed_item)
        stacked_screens.addWidget(
            _build_screen_widget(
                screen,
                shell_spec=shell_spec,
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
        _build_automation_environment_widget(
            shell_spec.automation_environment,
            shell_spec=shell_spec,
        )
    )

    overlay_navigation = QWidget(main_area)
    overlay_navigation.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
    overlay_navigation.setGeometry(QRect(0, 0, 0, main_area.height()))
    overlay_navigation.setStyleSheet(
        "background-color: #fbfaf7; border-right: 1px solid #d0cdc5;"
    )
    overlay_navigation.raise_()

    overlay_layout = QVBoxLayout(overlay_navigation)
    overlay_layout.setContentsMargins(14, 16, 14, 14)
    overlay_layout.setSpacing(12)
    overlay_title = QLabel(shell_spec.sidebar_composition.navigation_block_label)
    _style_navigation_label(overlay_title, shell_spec=shell_spec)
    overlay_layout.addWidget(overlay_title)

    overlay_nav_list = QListWidget()
    overlay_nav_list.setFixedHeight(230)
    overlay_nav_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    _apply_navigation_list_refinement(
        overlay_nav_list,
        shell_spec=shell_spec,
        collapsed=False,
    )
    for screen in shell_spec.screens:
        item = QListWidgetItem(screen.title)
        item.setData(256, screen.screen_id.value)
        overlay_nav_list.addItem(item)

    overlay_layout.addWidget(overlay_nav_list)
    overlay_layout.addStretch()
    overlay_footer_status = QLabel(shell_spec.sidebar_composition.footer_status)
    overlay_footer_detail = QLabel(shell_spec.sidebar_composition.footer_detail)
    _style_footer_label(overlay_footer_status, shell_spec=shell_spec)
    _style_footer_label(overlay_footer_detail, shell_spec=shell_spec)
    overlay_layout.addWidget(overlay_footer_status)
    overlay_layout.addWidget(overlay_footer_detail)

    navigation_animation = QPropertyAnimation(overlay_navigation, b"geometry")
    navigation_animation.setDuration(shell_spec.navigation_rail.animation_duration_ms)

    def set_navigation_index(index: int) -> None:
        if index < 0:
            return
        stacked_screens.setCurrentIndex(index)
        if collapsed_nav_list.currentRow() != index:
            collapsed_nav_list.setCurrentRow(index)
        if overlay_nav_list.currentRow() != index:
            overlay_nav_list.setCurrentRow(index)

    def expand_navigation_overlay() -> None:
        navigation_animation.stop()
        overlay_navigation.show()
        overlay_navigation.raise_()
        navigation_animation.setStartValue(overlay_navigation.geometry())
        navigation_animation.setEndValue(
            QRect(
                0,
                0,
                shell_spec.navigation_rail.expanded_width,
                main_area.height(),
            )
        )
        navigation_animation.start()

    def collapse_navigation_overlay() -> None:
        navigation_animation.stop()
        navigation_animation.setStartValue(overlay_navigation.geometry())
        navigation_animation.setEndValue(QRect(0, 0, 0, main_area.height()))
        navigation_animation.start()

    collapsed_nav_list.currentRowChanged.connect(set_navigation_index)
    overlay_nav_list.currentRowChanged.connect(set_navigation_index)
    collapsed_nav_list.setCurrentRow(0)
    overlay_nav_list.setCurrentRow(0)

    collapsed_rail.enterEvent = lambda _event: expand_navigation_overlay()
    overlay_navigation.leaveEvent = lambda _event: collapse_navigation_overlay()

    collapsed_rail_layout.addWidget(collapsed_nav_list)
    collapsed_rail_layout.addStretch()
    footer_label = QLabel(shell_spec.sidebar_composition.footer_status)
    _style_footer_label(footer_label, shell_spec=shell_spec)
    collapsed_rail_layout.addWidget(footer_label)

    root_layout.addWidget(collapsed_rail)
    root_layout.addWidget(_vertical_separator(QFrame))
    root_layout.addWidget(main_area)

    main_area.resizeEvent = lambda _event: overlay_navigation.setGeometry(
        QRect(0, 0, overlay_navigation.width(), main_area.height())
    )

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
        collapsed_width=64,
        expanded_width=184,
        expansion_trigger="hover",
        animation_duration_ms=200,
        item_height=34,
        item_spacing=8,
        active_state_treatment="soft filled selection with clear contrast",
        overlay_treatment="quiet floating panel with restrained hierarchy",
        footer_treatment="low-emphasis operational status",
        is_miniature=True,
        is_low_emphasis=True,
        reserves_collapsed_space=True,
        overlays_main_content=True,
        reflows_main_content_on_hover=False,
    )


def _build_prototype_vertical_rhythm() -> PrototypeVerticalRhythm:
    return PrototypeVerticalRhythm(
        content_margin=18,
        header_spacing=8,
        section_spacing=14,
        group_spacing=10,
        group_inner_margin=10,
        important_element_spacing=16,
        is_single_frame=True,
        introduces_scrolling=False,
        density_principle="restrained but not empty",
    )


def _build_prototype_typography_hierarchy() -> PrototypeTypographyHierarchy:
    return PrototypeTypographyHierarchy(
        screen_title_size=20,
        opening_statement_size=13,
        section_title_size=13,
        summary_size=12,
        detail_size=11,
        navigation_size=12,
        footer_size=10,
        active_navigation_weight=600,
        secondary_detail_treatment="muted supporting text",
        hierarchy_principle="scan first, detail second",
    )


def _apply_navigation_list_refinement(
    navigation_list,
    shell_spec: PrototypeShellSpec,
    collapsed: bool,
) -> None:
    navigation_list.setSpacing(shell_spec.navigation_rail.item_spacing)
    navigation_list.setStyleSheet(
        """
        QListWidget {
            background: transparent;
            border: none;
            outline: none;
        }
        QListWidget::item {
            min-height: 34px;
            border-radius: 6px;
            padding: 4px 8px;
            font-size: 12px;
            color: #3c3933;
        }
        QListWidget::item:selected {
            background: #e3e0d7;
            color: #171510;
            font-weight: 600;
        }
        QListWidget::item:hover {
            background: #eeece5;
        }
        """
    )
    if collapsed:
        navigation_list.setStyleSheet(
            navigation_list.styleSheet()
            + """
            QListWidget::item {
                text-align: center;
                padding: 4px 0;
            }
            """
        )


def _build_screen_widget(
    screen: PrototypeScreen,
    shell_spec: PrototypeShellSpec,
    home_concept: PrototypeHomeConcept | None = None,
    open_automation_environment=None,
):
    from PySide6.QtWidgets import QPushButton, QGroupBox, QLabel, QVBoxLayout, QWidget

    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(shell_spec.vertical_rhythm.header_spacing)
    title_label = QLabel(screen.title)
    primary_intention_label = QLabel(screen.primary_intention)
    _style_screen_title(title_label, shell_spec=shell_spec)
    _style_summary_label(primary_intention_label, shell_spec=shell_spec)
    layout.addWidget(title_label)
    layout.addWidget(primary_intention_label)

    if home_concept is not None:
        philosophy_label = QLabel(home_concept.philosophy_statement)
        opening_feel_label = QLabel(home_concept.opening_feel)
        _style_opening_statement(philosophy_label, shell_spec=shell_spec)
        _style_detail_label(opening_feel_label, shell_spec=shell_spec)
        layout.addWidget(philosophy_label)
        layout.addWidget(opening_feel_label)
        layout.addSpacing(shell_spec.vertical_rhythm.important_element_spacing)

        for signal in home_concept.signals:
            group_box = QGroupBox(f"{signal.zone_role.value.title()} - {signal.title}")
            _style_group_box(group_box, shell_spec=shell_spec)
            signal_layout = QVBoxLayout(group_box)
            signal_layout.setContentsMargins(
                shell_spec.vertical_rhythm.group_inner_margin,
                shell_spec.vertical_rhythm.group_inner_margin,
                shell_spec.vertical_rhythm.group_inner_margin,
                shell_spec.vertical_rhythm.group_inner_margin,
            )
            signal_layout.setSpacing(shell_spec.vertical_rhythm.group_spacing)
            summary_label = QLabel(signal.summary)
            _style_summary_label(summary_label, shell_spec=shell_spec)
            signal_layout.addWidget(summary_label)
            layout.addWidget(group_box)
            layout.addSpacing(shell_spec.vertical_rhythm.section_spacing)

    if open_automation_environment is not None:
        button = QPushButton("Open Automation Environment Prototype")
        button.clicked.connect(open_automation_environment)
        layout.addSpacing(shell_spec.vertical_rhythm.important_element_spacing)
        layout.addWidget(button)

    if home_concept is not None:
        layout.addStretch()
        return container

    for zone in screen.zones:
        group_box = QGroupBox(zone.role.value.title())
        _style_group_box(group_box, shell_spec=shell_spec)
        zone_layout = QVBoxLayout(group_box)
        zone_layout.setContentsMargins(
            shell_spec.vertical_rhythm.group_inner_margin,
            shell_spec.vertical_rhythm.group_inner_margin,
            shell_spec.vertical_rhythm.group_inner_margin,
            shell_spec.vertical_rhythm.group_inner_margin,
        )
        zone_layout.setSpacing(shell_spec.vertical_rhythm.group_spacing)
        zone_label = QLabel(zone.purpose)
        _style_detail_label(zone_label, shell_spec=shell_spec)
        zone_layout.addWidget(zone_label)
        layout.addWidget(group_box)
        layout.addSpacing(shell_spec.vertical_rhythm.section_spacing)

    layout.addStretch()

    return container


def _build_automation_environment_widget(
    automation_environment: PrototypeAutomationEnvironment,
    shell_spec: PrototypeShellSpec,
):
    from PySide6.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QWidget

    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(shell_spec.vertical_rhythm.header_spacing)
    title_label = QLabel(automation_environment.title)
    primary_intention_label = QLabel(automation_environment.primary_intention)
    _style_screen_title(title_label, shell_spec=shell_spec)
    _style_summary_label(primary_intention_label, shell_spec=shell_spec)
    layout.addWidget(title_label)
    layout.addWidget(primary_intention_label)
    layout.addSpacing(shell_spec.vertical_rhythm.important_element_spacing)

    for section in automation_environment.sections:
        title = f"{section.zone_role.value.title()} - {section.title}"
        if section.is_collapsed_feeling:
            title = f"{title} (collapsed placeholder)"

        group_box = QGroupBox(title)
        _style_group_box(group_box, shell_spec=shell_spec)
        section_layout = QVBoxLayout(group_box)
        section_layout.setContentsMargins(
            shell_spec.vertical_rhythm.group_inner_margin,
            shell_spec.vertical_rhythm.group_inner_margin,
            shell_spec.vertical_rhythm.group_inner_margin,
            shell_spec.vertical_rhythm.group_inner_margin,
        )
        section_layout.setSpacing(shell_spec.vertical_rhythm.group_spacing)
        summary_label = QLabel(section.summary)
        _style_summary_label(summary_label, shell_spec=shell_spec)
        section_layout.addWidget(summary_label)

        for detail in section.details:
            detail_label = QLabel(detail)
            _style_detail_label(detail_label, shell_spec=shell_spec)
            section_layout.addWidget(detail_label)

        layout.addWidget(group_box)
        layout.addSpacing(shell_spec.vertical_rhythm.section_spacing)

    layout.addStretch()

    return container


def _style_screen_title(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.screen_title_size}px; "
        "font-weight: 650; color: #171510;"
    )
    label.setWordWrap(True)


def _style_opening_statement(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.opening_statement_size}px; "
        "font-weight: 500; color: #2d2a24;"
    )
    label.setWordWrap(True)


def _style_summary_label(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.summary_size}px; "
        "font-weight: 500; color: #2f2c26;"
    )
    label.setWordWrap(True)


def _style_detail_label(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.detail_size}px; "
        "font-weight: 400; color: #6a665d;"
    )
    label.setWordWrap(True)


def _style_navigation_label(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.navigation_size}px; "
        "font-weight: 600; color: #27241f;"
    )


def _style_footer_label(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.footer_size}px; "
        "font-weight: 400; color: #777267;"
    )
    label.setWordWrap(True)


def _style_group_box(group_box, shell_spec: PrototypeShellSpec) -> None:
    group_box.setStyleSheet(
        f"""
        QGroupBox {{
            font-size: {shell_spec.typography.section_title_size}px;
            font-weight: 600;
            color: #24211c;
            border: 1px solid #dedbd2;
            border-radius: 6px;
            margin-top: 9px;
            background-color: #fffefb;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 9px;
            padding: 0 4px;
        }}
        """
    )


def _vertical_separator(frame_type):
    separator = frame_type()
    separator.setFrameShape(frame_type.Shape.VLine)
    separator.setFrameShadow(frame_type.Shadow.Sunken)
    return separator


def main() -> int:
    return launch_pyside6_shell_prototype()


if __name__ == "__main__":
    raise SystemExit(main())
