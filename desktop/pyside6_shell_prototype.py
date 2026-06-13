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
    readability_treatment: str
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
    composition_principle: str
    primary_action_label: str
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
class PrototypeVisualComposition:
    uses_custom_cards: bool
    home_hero_treatment: str
    card_treatment: str
    secondary_treatment: str
    commitment_treatment: str
    background_treatment: str
    composition_principle: str
    home_layout_treatment: str
    automation_layout_treatment: str


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
    visual_composition: PrototypeVisualComposition


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
        visual_composition=_build_prototype_visual_composition(),
    )


def launch_pyside6_shell_prototype() -> int:
    try:
        from PySide6.QtCore import QPropertyAnimation, QRect
        from PySide6.QtWidgets import (
            QApplication,
            QFrame,
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
    app.setStyleSheet(
        """
        QWidget {
            font-family: "Segoe UI";
        }
        QMainWindow {
            background-color: #111315;
        }
        QStackedWidget {
            background: transparent;
            border: none;
        }
        """
    )
    window = QMainWindow()
    window.setWindowTitle(shell_spec.window_title)
    window.setFixedSize(shell_spec.window_width, shell_spec.window_height)

    root = QWidget()
    root.setStyleSheet("background-color: #111315;")
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
        "background-color: #101214; border-right: 1px solid #282b2d;"
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
    main_area.setStyleSheet("background-color: #17191b;")
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
        "background-color: #151719; border-right: 1px solid #333638;"
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
        primary_intention="Orient, confirm, then commit.",
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
                section.expected_baseline,
            ),
            zone_role=ZoneRole.PRIMARY,
            readability_treatment="primary orientation",
        )

    if isinstance(section, ProfileSection):
        return PrototypeAutomationEnvironmentSection(
            section_id=section.section_id,
            title="Profile",
            summary=section.profile_name,
            details=(
                section.behavior_summary,
                section.reliability_posture,
            ),
            zone_role=ZoneRole.PRIMARY,
            readability_treatment="primary behavior summary",
        )

    if isinstance(section, ReadinessSection):
        return PrototypeAutomationEnvironmentSection(
            section_id=section.section_id,
            title="Readiness",
            summary=section.readiness_wording,
            details=(
                section.expected_baseline,
                section.focus_requirement,
            )
            + section.confidence_notes[:1],
            zone_role=ZoneRole.PRIMARY,
            readability_treatment="primary confidence check",
        )

    if isinstance(section, ContextualWarningsSection):
        return PrototypeAutomationEnvironmentSection(
            section_id=section.section_id,
            title="Contextual Warnings",
            summary="Warnings remain contextual and secondary.",
            details=section.warnings or ("No contextual warnings for this placeholder.",),
            zone_role=ZoneRole.SECONDARY,
            readability_treatment="secondary contextual support",
        )

    if isinstance(section, AdvancedSection):
        return PrototypeAutomationEnvironmentSection(
            section_id=section.section_id,
            title="Advanced / Refinement",
            summary=section.purpose,
            details=section.available_refinements or ("Collapsed placeholder only.",),
            zone_role=ZoneRole.TERTIARY,
            readability_treatment="tertiary collapsed refinement",
            is_collapsed_feeling=section.is_collapsed_by_default,
        )

    return PrototypeAutomationEnvironmentSection(
        section_id=section.section_id,
        title="Run",
        summary=section.commitment_message,
        details=(
            f"Status: {section.status_label}",
            f"Requested count: {section.requested_count}",
        ),
        zone_role=ZoneRole.PRIMARY,
        readability_treatment="primary deliberate commitment",
    )


def _build_prototype_home_concept() -> PrototypeHomeConcept:
    return PrototypeHomeConcept(
        title="Home",
        philosophy_statement="Quiet confidence before operational commitment.",
        opening_feel="A restrained launchpad that presents what matters now.",
        composition_principle="recommended next step first",
        primary_action_label="Prepare Automation",
        is_single_frame=True,
        is_dashboard_like=False,
        signals=(
            PrototypeHomeSignal(
                title="Recommended Next Step",
                summary="Prepare a supervised run when FH6 is at a known baseline.",
                zone_role=ZoneRole.PRIMARY,
            ),
            PrototypeHomeSignal(
                title="Prepare A Run",
                summary="Review profile, readiness, warnings, and commitment in one focused place.",
                zone_role=ZoneRole.PRIMARY,
            ),
            PrototypeHomeSignal(
                title="Recent Context",
                summary="Recent activity stays lightweight: reassurance, not a dashboard.",
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


def _build_prototype_visual_composition() -> PrototypeVisualComposition:
    return PrototypeVisualComposition(
        uses_custom_cards=True,
        home_hero_treatment="dark quiet launch surface",
        card_treatment="layered dark utility card",
        secondary_treatment="recessed contextual support",
        commitment_treatment="restrained amber commitment",
        background_treatment="dark companion canvas",
        composition_principle="mvp-coherent dark companion surface",
        home_layout_treatment="launch surface with paired operational signals",
        automation_layout_treatment="preparation flow with deliberate commitment",
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
            color: #bdb6aa;
        }
        QListWidget::item:selected {
            background: #303337;
            color: #f2e7d2;
            font-weight: 600;
        }
        QListWidget::item:hover {
            background: #25282b;
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
    from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

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
        _build_home_screen_content(
            layout=layout,
            home_concept=home_concept,
            shell_spec=shell_spec,
            open_automation_environment=open_automation_environment,
        )
        layout.addStretch()
        return container

    for zone in screen.zones:
        layout.addWidget(
            _build_visual_card(
                title=zone.role.value.title(),
                summary=zone.purpose,
                details=(),
                shell_spec=shell_spec,
                treatment=zone.role.value,
            )
        )
        layout.addSpacing(shell_spec.vertical_rhythm.section_spacing)

    layout.addStretch()

    return container


def _build_automation_environment_widget(
    automation_environment: PrototypeAutomationEnvironment,
    shell_spec: PrototypeShellSpec,
):
    from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

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

    _build_automation_environment_content(
        layout=layout,
        automation_environment=automation_environment,
        shell_spec=shell_spec,
    )

    layout.addStretch()

    return container


def _build_home_screen_content(
    layout,
    home_concept: PrototypeHomeConcept,
    shell_spec: PrototypeShellSpec,
    open_automation_environment,
) -> None:
    from PySide6.QtWidgets import QPushButton

    layout.addWidget(
        _build_visual_card(
            title="Ready when the baseline is clear",
            summary=home_concept.philosophy_statement,
            details=(home_concept.opening_feel,),
            shell_spec=shell_spec,
            treatment="hero",
        )
    )
    layout.addSpacing(shell_spec.vertical_rhythm.important_element_spacing)

    first_row = _build_card_row(
        cards=(
            _build_visual_card(
                title=home_concept.signals[0].title,
                summary=home_concept.signals[0].summary,
                details=(),
                shell_spec=shell_spec,
                treatment="primary",
            ),
            _build_visual_card(
                title=home_concept.signals[1].title,
                summary=home_concept.signals[1].summary,
                details=(),
                shell_spec=shell_spec,
                treatment="primary",
            ),
        ),
        shell_spec=shell_spec,
    )
    layout.addLayout(first_row)
    layout.addSpacing(shell_spec.vertical_rhythm.section_spacing)

    second_row = _build_card_row(
        cards=(
            _build_visual_card(
                title=home_concept.signals[2].title,
                summary=home_concept.signals[2].summary,
                details=(),
                shell_spec=shell_spec,
                treatment="secondary",
            ),
            _build_visual_card(
                title=home_concept.signals[3].title,
                summary=home_concept.signals[3].summary,
                details=(),
                shell_spec=shell_spec,
                treatment="tertiary",
            ),
        ),
        shell_spec=shell_spec,
    )
    layout.addLayout(second_row)

    if open_automation_environment is not None:
        button = QPushButton(home_concept.primary_action_label)
        _style_primary_button(button, shell_spec=shell_spec)
        button.clicked.connect(open_automation_environment)
        layout.addSpacing(shell_spec.vertical_rhythm.important_element_spacing)
        layout.addWidget(button)


def _build_automation_environment_content(
    layout,
    automation_environment: PrototypeAutomationEnvironment,
    shell_spec: PrototypeShellSpec,
) -> None:
    sections_by_id = {
        section.section_id: section
        for section in automation_environment.sections
    }

    overview = sections_by_id[AutomationEnvironmentSectionId.OVERVIEW]
    profile = sections_by_id[AutomationEnvironmentSectionId.PROFILE]
    readiness = sections_by_id[AutomationEnvironmentSectionId.READINESS]
    warnings = sections_by_id[AutomationEnvironmentSectionId.CONTEXTUAL_WARNINGS]
    advanced = sections_by_id[AutomationEnvironmentSectionId.ADVANCED]
    run = sections_by_id[AutomationEnvironmentSectionId.RUN]

    layout.addLayout(
        _build_card_row(
            cards=(
                _build_section_card(overview, shell_spec=shell_spec),
                _build_section_card(profile, shell_spec=shell_spec),
            ),
            shell_spec=shell_spec,
        )
    )
    layout.addSpacing(shell_spec.vertical_rhythm.section_spacing)
    layout.addWidget(_build_section_card(readiness, shell_spec=shell_spec))
    layout.addSpacing(shell_spec.vertical_rhythm.section_spacing)
    layout.addLayout(
        _build_card_row(
            cards=(
                _build_section_card(warnings, shell_spec=shell_spec),
                _build_section_card(advanced, shell_spec=shell_spec),
            ),
            shell_spec=shell_spec,
        )
    )
    layout.addSpacing(shell_spec.vertical_rhythm.section_spacing)
    layout.addWidget(_build_section_card(run, shell_spec=shell_spec))


def _build_section_card(
    section: PrototypeAutomationEnvironmentSection,
    shell_spec: PrototypeShellSpec,
):
    title = section.title
    if section.is_collapsed_feeling:
        title = f"{title} (quiet)"

    return _build_visual_card(
        title=title,
        summary=section.summary,
        details=section.details,
        shell_spec=shell_spec,
        treatment=section.readability_treatment,
    )


def _build_card_row(cards: tuple[object, object], shell_spec: PrototypeShellSpec):
    from PySide6.QtWidgets import QHBoxLayout

    row = QHBoxLayout()
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(shell_spec.vertical_rhythm.group_spacing)
    for card in cards:
        row.addWidget(card)

    return row


def _build_visual_card(
    title: str,
    summary: str,
    details: tuple[str, ...],
    shell_spec: PrototypeShellSpec,
    treatment: str,
):
    from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout

    card = QFrame()
    card.setFrameShape(QFrame.Shape.NoFrame)
    card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    _style_visual_card(card, treatment=treatment)

    card_layout = QVBoxLayout(card)
    card_layout.setContentsMargins(
        shell_spec.vertical_rhythm.group_inner_margin + 2,
        shell_spec.vertical_rhythm.group_inner_margin,
        shell_spec.vertical_rhythm.group_inner_margin + 2,
        shell_spec.vertical_rhythm.group_inner_margin,
    )
    card_layout.setSpacing(6)

    title_label = QLabel(title)
    summary_label = QLabel(summary)
    _style_card_title(title_label, shell_spec=shell_spec, treatment=treatment)
    _style_summary_label(summary_label, shell_spec=shell_spec)
    card_layout.addWidget(title_label)
    card_layout.addWidget(summary_label)

    for detail in details:
        detail_label = QLabel(detail)
        _style_detail_label(detail_label, shell_spec=shell_spec)
        card_layout.addWidget(detail_label)

    return card


def _style_visual_card(card, treatment: str) -> None:
    if treatment == "hero":
        card.setStyleSheet(
            """
            QFrame {
                background-color: #202327;
                border: 1px solid #3e3b34;
                border-left: 4px solid #a9905f;
                border-radius: 8px;
            }
            """
        )
        return

    if "tertiary" in treatment:
        card.setStyleSheet(
            """
            QFrame {
                background-color: #1b1d20;
                border: 1px solid #2d3032;
                border-radius: 7px;
            }
            """
        )
        return

    if "secondary" in treatment:
        card.setStyleSheet(
            """
            QFrame {
                background-color: #1d2023;
                border: 1px solid #313436;
                border-radius: 7px;
            }
            """
        )
        return

    if "commitment" in treatment:
        card.setStyleSheet(
            """
            QFrame {
                background-color: #242018;
                border: 1px solid #514632;
                border-left: 4px solid #b79a63;
                border-radius: 8px;
            }
            """
        )
        return

    card.setStyleSheet(
        """
        QFrame {
            background-color: #202326;
            border: 1px solid #35383a;
            border-radius: 7px;
        }
        """
    )


def _style_card_title(label, shell_spec: PrototypeShellSpec, treatment: str) -> None:
    color = "#f4ead7"
    weight = 620
    if "secondary" in treatment or "tertiary" in treatment:
        color = "#c8beac"
        weight = 560

    label.setStyleSheet(
        f"font-size: {shell_spec.typography.section_title_size}px; "
        f"font-weight: {weight}; color: {color};"
    )
    label.setWordWrap(True)


def _style_screen_title(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.screen_title_size}px; "
        "font-weight: 650; color: #f5ead8;"
    )
    label.setWordWrap(True)


def _style_opening_statement(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.opening_statement_size}px; "
        "font-weight: 500; color: #ddd0ba;"
    )
    label.setWordWrap(True)


def _style_summary_label(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.summary_size}px; "
        "font-weight: 500; color: #d6c9b6;"
    )
    label.setWordWrap(True)


def _style_detail_label(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.detail_size}px; "
        "font-weight: 400; color: #948b7c;"
    )
    label.setWordWrap(True)


def _style_navigation_label(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.navigation_size}px; "
        "font-weight: 600; color: #f0e3ca;"
    )


def _style_footer_label(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.footer_size}px; "
        "font-weight: 400; color: #8f8778;"
    )
    label.setWordWrap(True)


def _style_primary_button(button, shell_spec: PrototypeShellSpec) -> None:
    button.setStyleSheet(
        f"""
        QPushButton {{
            font-size: {shell_spec.typography.summary_size}px;
            font-weight: 620;
            color: #181613;
            background-color: #ad9362;
            border: 1px solid #c2a873;
            border-radius: 7px;
            padding: 8px 10px;
        }}
        QPushButton:hover {{
            background-color: #bca36f;
        }}
        QPushButton:pressed {{
            background-color: #967d50;
        }}
        """
    )


def _vertical_separator(frame_type):
    separator = frame_type()
    separator.setFrameShape(frame_type.Shape.VLine)
    separator.setFrameShadow(frame_type.Shadow.Sunken)
    separator.setStyleSheet("color: #292c2d; background-color: #292c2d;")
    return separator


def main() -> int:
    return launch_pyside6_shell_prototype()


if __name__ == "__main__":
    raise SystemExit(main())
