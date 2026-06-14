from dataclasses import dataclass

from frontend.automation_controller import (
    AutomationRunRequest,
    FrontendAutomationController,
)
from product.automation_registry import get_automation_definition
from product.automation_registry import get_active_automation_definitions
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


COLOR_SURFACE_ROOT = "#0F1115"
COLOR_SURFACE_BASE = "#17191E"
COLOR_SURFACE_RAIL = "#111318"
COLOR_SURFACE_TOPBAR = "#101217"
COLOR_SURFACE_CARD = "#1E2128"
COLOR_SURFACE_CARD_RAISED = "#262B35"
COLOR_SURFACE_CARD_SOFT = "#20242C"
COLOR_SURFACE_RECESSED = "#191C22"
COLOR_BORDER_SUBTLE = "#353A46"
COLOR_BORDER_STRONG = "#444B59"
COLOR_ACCENT_PRIMARY = "#F21A87"
COLOR_ACCENT_HOVER = "#FF4FA5"
COLOR_ACCENT_PRESSED = "#C8146D"
COLOR_TEXT_PRIMARY = "#E7E9EE"
COLOR_TEXT_SECONDARY = "#B1B8C4"
COLOR_TEXT_MUTED = "#7C8593"
COLOR_TEXT_FAINT = "#5F6673"


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
class PrototypeTopBar:
    title: str
    height: int
    treatment: str
    reserves_identity_space: bool


@dataclass(frozen=True)
class PrototypeCompanionMode:
    title: str
    primary_intention: str
    status_label: str
    operation_label: str
    focus_label: str
    stop_label: str
    is_simpler_than_automation_environment: bool
    introduces_execution: bool


@dataclass(frozen=True)
class PrototypeCompletionState:
    state_id: str
    title: str
    summary: str
    reassurance: str
    suggested_next_step: str
    emotional_treatment: str


@dataclass(frozen=True)
class PrototypeCompletionLifecycle:
    title: str
    primary_intention: str
    states: tuple[PrototypeCompletionState, ...]
    always_returns_to_preparation: bool
    introduces_execution: bool


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
    top_bar: PrototypeTopBar
    companion_mode: PrototypeCompanionMode
    completion_lifecycle: PrototypeCompletionLifecycle


def build_prototype_shell_spec() -> PrototypeShellSpec:
    sidebar_destinations = get_sidebar_destinations()

    return PrototypeShellSpec(
        window_title="FH6 Farm Tool - PySide6 Shell Prototype",
        window_width=640,
        window_height=864,
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
        top_bar=_build_prototype_top_bar(),
        companion_mode=_build_prototype_companion_mode(),
        completion_lifecycle=_build_prototype_completion_lifecycle(),
    )


def launch_pyside6_shell_prototype() -> int:
    try:
        from PySide6.QtCore import QPropertyAnimation, QRect
        from PySide6.QtWidgets import (
            QApplication,
            QFrame,
            QGraphicsOpacityEffect,
            QHBoxLayout,
            QLabel,
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
    app.setStyleSheet(_global_stylesheet())

    window = QMainWindow()
    window.setWindowTitle(shell_spec.window_title)
    window.setFixedSize(shell_spec.window_width, shell_spec.window_height)

    root = QWidget()
    root.setStyleSheet(f"background-color: {COLOR_SURFACE_ROOT};")
    root_layout = QVBoxLayout(root)
    root_layout.setContentsMargins(0, 0, 0, 0)
    root_layout.setSpacing(0)

    root_layout.addWidget(_build_top_bar_widget(shell_spec, QLabel))

    body = QWidget()
    body_layout = QHBoxLayout(body)
    body_layout.setContentsMargins(0, 0, 0, 0)
    body_layout.setSpacing(0)

    collapsed_rail = QWidget()
    collapsed_rail.setFixedWidth(shell_spec.navigation_rail.collapsed_width)
    collapsed_rail.setSizePolicy(
        QSizePolicy.Policy.Fixed,
        QSizePolicy.Policy.Expanding,
    )
    collapsed_rail.setStyleSheet(f"background-color: {COLOR_SURFACE_RAIL};")
    collapsed_rail_layout = QVBoxLayout(collapsed_rail)
    collapsed_rail_layout.setContentsMargins(8, 12, 8, 12)
    collapsed_rail_layout.setSpacing(10)

    collapsed_nav_container = QWidget()
    collapsed_nav_container.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Fixed,
    )
    collapsed_nav_layout = QVBoxLayout(collapsed_nav_container)
    collapsed_nav_layout.setContentsMargins(0, 0, 0, 0)
    collapsed_nav_layout.setSpacing(shell_spec.navigation_rail.item_spacing)
    collapsed_nav_buttons = []
    overlay_nav_buttons = []
    overlay_text_fade_animations = []

    main_area = QWidget()
    main_area.setStyleSheet(f"background-color: {COLOR_SURFACE_BASE};")
    main_area_layout = QVBoxLayout(main_area)
    main_area_layout.setContentsMargins(
        shell_spec.vertical_rhythm.content_margin,
        shell_spec.vertical_rhythm.content_margin,
        shell_spec.vertical_rhythm.content_margin,
        shell_spec.vertical_rhythm.content_margin,
    )

    stacked_screens = QStackedWidget()
    main_area_layout.addWidget(stacked_screens)
    automation_environment_index = len(shell_spec.screens)
    companion_mode_index = automation_environment_index + 1
    completion_state_index = companion_mode_index + 1

    for index, screen in enumerate(shell_spec.screens):
        collapsed_button = _build_navigation_button(
            screen=screen,
            shell_spec=shell_spec,
            collapsed=True,
        )
        collapsed_button.mousePressEvent = lambda _event, row=index: set_navigation_index(row)
        collapsed_nav_buttons.append(collapsed_button)
        collapsed_nav_layout.addWidget(collapsed_button)
        stacked_screens.addWidget(
            _build_screen_widget(
                screen,
                shell_spec=shell_spec,
                home_concept=shell_spec.home_concept
                if screen.screen_id == ScreenId.HOME
                else None,
                open_automation_environment=(
                    lambda: stacked_screens.setCurrentIndex(automation_environment_index)
                )
                if screen.screen_id == ScreenId.HOME
                else None,
            )
        )

    completion_state_widget, update_completion_state = _build_completion_state_widget(
        shell_spec=shell_spec,
        return_to_preparation=lambda: stacked_screens.setCurrentIndex(
            automation_environment_index
        ),
    )
    companion_mode_widget, update_companion_mode = _build_companion_mode_widget(
        shell_spec=shell_spec,
        return_to_preparation=lambda: stacked_screens.setCurrentIndex(
            automation_environment_index
        ),
        open_completion_state=(
            lambda state_id, companion_state: (
                update_completion_state(state_id, companion_state),
                stacked_screens.setCurrentIndex(completion_state_index),
            )
        ),
    )
    stacked_screens.addWidget(
        _build_automation_environment_widget(
            shell_spec.automation_environment,
            shell_spec=shell_spec,
            open_companion_mode=(
                lambda companion_state: (
                    update_companion_mode(companion_state),
                    stacked_screens.setCurrentIndex(companion_mode_index),
                )
            ),
        )
    )
    stacked_screens.addWidget(companion_mode_widget)
    stacked_screens.addWidget(completion_state_widget)

    overlay_navigation = QWidget(body)
    overlay_navigation.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
    overlay_navigation.setGeometry(QRect(0, 0, 0, body.height()))
    overlay_navigation.setStyleSheet(f"background-color: {COLOR_SURFACE_RAIL};")
    overlay_navigation.raise_()

    overlay_layout = QVBoxLayout(overlay_navigation)
    overlay_layout.setContentsMargins(8, 12, 14, 14)
    overlay_layout.setSpacing(10)

    overlay_nav_container = QWidget()
    overlay_nav_container.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Fixed,
    )
    overlay_nav_layout = QVBoxLayout(overlay_nav_container)
    overlay_nav_layout.setContentsMargins(0, 0, 0, 0)
    overlay_nav_layout.setSpacing(shell_spec.navigation_rail.item_spacing)

    for index, screen in enumerate(shell_spec.screens):
        overlay_button = _build_navigation_button(
            screen=screen,
            shell_spec=shell_spec,
            collapsed=False,
        )
        overlay_button.mousePressEvent = lambda _event, row=index: set_navigation_index(row)
        overlay_nav_buttons.append(overlay_button)
        overlay_nav_layout.addWidget(overlay_button)
        if overlay_button._navigation_text_label is not None:
            opacity_effect = QGraphicsOpacityEffect(overlay_button)
            opacity_effect.setOpacity(0)
            overlay_button._navigation_text_label.setGraphicsEffect(opacity_effect)
            text_animation = QPropertyAnimation(opacity_effect, b"opacity")
            text_animation.setDuration(shell_spec.navigation_rail.animation_duration_ms)
            overlay_text_fade_animations.append(text_animation)

    overlay_layout.addWidget(overlay_nav_container)
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
        for row, button in enumerate(collapsed_nav_buttons):
            _style_navigation_button(
                button,
                shell_spec=shell_spec,
                collapsed=True,
                selected=row == index,
            )
        for row, button in enumerate(overlay_nav_buttons):
            _style_navigation_button(
                button,
                shell_spec=shell_spec,
                collapsed=False,
                selected=row == index,
            )

    def animate_overlay_text_opacity(target_opacity: float) -> None:
        for animation in overlay_text_fade_animations:
            animation.stop()
            animation.setStartValue(animation.targetObject().opacity())
            animation.setEndValue(target_opacity)
            animation.start()

    def expand_navigation_overlay() -> None:
        navigation_animation.stop()
        overlay_navigation.show()
        overlay_navigation.raise_()
        animate_overlay_text_opacity(1)
        navigation_animation.setStartValue(overlay_navigation.geometry())
        navigation_animation.setEndValue(
            QRect(
                0,
                0,
                shell_spec.navigation_rail.expanded_width,
                body.height(),
            )
        )
        navigation_animation.start()

    def collapse_navigation_overlay() -> None:
        navigation_animation.stop()
        animate_overlay_text_opacity(0)
        navigation_animation.setStartValue(overlay_navigation.geometry())
        navigation_animation.setEndValue(QRect(0, 0, 0, body.height()))
        navigation_animation.start()

    set_navigation_index(0)

    collapsed_rail.enterEvent = lambda _event: expand_navigation_overlay()
    overlay_navigation.leaveEvent = lambda _event: collapse_navigation_overlay()
    root.leaveEvent = lambda _event: collapse_navigation_overlay()

    collapsed_rail_layout.addWidget(collapsed_nav_container)
    collapsed_rail_layout.addStretch()
    footer_label = QLabel(shell_spec.sidebar_composition.footer_status)
    _style_footer_label(footer_label, shell_spec=shell_spec)
    collapsed_rail_layout.addWidget(footer_label)

    body_layout.addWidget(collapsed_rail)
    body_layout.addWidget(main_area)
    root_layout.addWidget(body)

    body.resizeEvent = lambda _event: overlay_navigation.setGeometry(
        QRect(0, 0, overlay_navigation.width(), body.height())
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
            details=(section.short_purpose, section.expected_baseline),
            zone_role=ZoneRole.PRIMARY,
            readability_treatment="primary orientation",
        )

    if isinstance(section, ProfileSection):
        return PrototypeAutomationEnvironmentSection(
            section_id=section.section_id,
            title="Profile",
            summary=section.profile_name,
            details=(section.behavior_summary, section.reliability_posture),
            zone_role=ZoneRole.PRIMARY,
            readability_treatment="primary behavior summary",
        )

    if isinstance(section, ReadinessSection):
        return PrototypeAutomationEnvironmentSection(
            section_id=section.section_id,
            title="Readiness",
            summary=section.readiness_wording,
            details=(section.expected_baseline, section.focus_requirement)
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
        philosophy_statement="Ready when the baseline is clear.",
        opening_feel="Controlled preparation before supervised operation.",
        composition_principle="recommended next step first",
        primary_action_label="Prepare a Run",
        is_single_frame=True,
        is_dashboard_like=False,
        signals=(
            PrototypeHomeSignal(
                title="RECOMMENDED NEXT STEP",
                summary="Prepare a supervised run",
                zone_role=ZoneRole.PRIMARY,
            ),
            PrototypeHomeSignal(
                title="REVIEW & PLAN",
                summary="Review profile and readiness",
                zone_role=ZoneRole.PRIMARY,
            ),
            PrototypeHomeSignal(
                title="RECENT CONTEXT",
                summary="Last prepared: Auto1 / supervised baseline",
                zone_role=ZoneRole.SECONDARY,
            ),
            PrototypeHomeSignal(
                title="QUIET STATUS",
                summary="Controlled MVP - Manual operation ready",
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
        expanded_width=230,
        expansion_trigger="hover",
        animation_duration_ms=200,
        item_height=42,
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
        commitment_treatment="restrained pink commitment",
        background_treatment="dark companion canvas",
        composition_principle="brief-aligned graphite companion surface",
        home_layout_treatment="ordered launch surface with dominant recommended action",
        automation_layout_treatment="preparation flow with deliberate commitment",
    )


def _build_prototype_top_bar() -> PrototypeTopBar:
    return PrototypeTopBar(
        title="FH6 Farm Tool",
        height=63,
        treatment="restrained product identity bar",
        reserves_identity_space=True,
    )


def _build_prototype_companion_mode() -> PrototypeCompanionMode:
    return PrototypeCompanionMode(
        title="Companion Mode",
        primary_intention="Supervise confidently during a prepared operation.",
        status_label="Running",
        operation_label="Supervised operation",
        focus_label="FH6 focus handoff ready",
        stop_label="F8 emergency stop available",
        is_simpler_than_automation_environment=True,
        introduces_execution=False,
    )


def _build_prototype_completion_lifecycle() -> PrototypeCompletionLifecycle:
    return PrototypeCompletionLifecycle(
        title="Post-Run State",
        primary_intention="Conclude calmly, recover trust, and choose the next step.",
        states=(
            PrototypeCompletionState(
                state_id="completed",
                title="Run completed",
                summary="The supervised operation reached its requested endpoint.",
                reassurance="No follow-up action is required unless you want another run.",
                suggested_next_step="Prepare another supervised run",
                emotional_treatment="professional completion",
            ),
            PrototypeCompletionState(
                state_id="stopped",
                title="Stopped safely",
                summary="The operation was interrupted intentionally and safely.",
                reassurance="A manual stop is a controlled outcome, not a failure.",
                suggested_next_step="Resume preparation",
                emotional_treatment="reassuring interruption",
            ),
            PrototypeCompletionState(
                state_id="refused",
                title="Operation paused",
                summary="The prepared operation should be reviewed before continuing.",
                reassurance="Protective refusal keeps the system aligned with trust-first use.",
                suggested_next_step="Review Automation Environment",
                emotional_treatment="calm refusal",
            ),
        ),
        always_returns_to_preparation=True,
        introduces_execution=False,
    )


def _global_stylesheet() -> str:
    return f"""
    QWidget {{
        font-family: "Segoe UI";
    }}
    QLabel {{
        background: transparent;
        border: none;
    }}
    QMainWindow {{
        background-color: {COLOR_SURFACE_ROOT};
    }}
    QStackedWidget {{
        background: transparent;
        border: none;
    }}
    """


def _build_top_bar_widget(shell_spec: PrototypeShellSpec, label_type):
    from PySide6.QtWidgets import QHBoxLayout, QWidget

    top_bar = QWidget()
    top_bar.setFixedHeight(shell_spec.top_bar.height)
    top_bar.setStyleSheet(
        f"background-color: {COLOR_SURFACE_TOPBAR}; "
        f"border-bottom: 1px solid {COLOR_BORDER_SUBTLE};"
    )
    layout = QHBoxLayout(top_bar)
    layout.setContentsMargins(18, 0, 18, 0)
    layout.setSpacing(6)

    product_prefix_label = label_type("FH6")
    product_prefix_label.setStyleSheet(
        f"font-size: 14px; font-weight: 700; color: {COLOR_ACCENT_PRIMARY};"
    )
    product_name_label = label_type("Farm Tool")
    product_name_label.setStyleSheet(
        f"font-size: 14px; font-weight: 650; color: {COLOR_TEXT_PRIMARY};"
    )
    layout.addWidget(product_prefix_label)
    layout.addWidget(product_name_label)
    layout.addStretch()

    return top_bar


def _navigation_icon_for_screen(screen_id: ScreenId) -> str:
    icons = {
        ScreenId.HOME: "⌂",
        ScreenId.PROFILES: "◎",
        ScreenId.HISTORY: "◷",
        ScreenId.HELP: "?",
        ScreenId.SETTINGS: "⚙",
    }
    return icons[screen_id]


def _build_navigation_button(
    screen: PrototypeScreen,
    shell_spec: PrototypeShellSpec,
    collapsed: bool,
):
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy

    button = QFrame()
    button.setObjectName("NavigationItem")
    button.setFixedHeight(shell_spec.navigation_rail.item_height)
    button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    layout = QHBoxLayout(button)
    layout.setContentsMargins(0 if collapsed else 10, 0, 0 if collapsed else 12, 0)
    layout.setSpacing(8)

    icon_label = QLabel(_navigation_icon_for_screen(screen.screen_id))
    icon_label.setFixedWidth(shell_spec.navigation_rail.item_height)
    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    icon_label.setObjectName("NavigationIcon")
    layout.addWidget(icon_label)

    text_label = None
    if not collapsed:
        text_label = QLabel(screen.title)
        text_label.setObjectName("NavigationText")
        text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(text_label)

    button._navigation_icon_label = icon_label
    button._navigation_text_label = text_label
    _style_navigation_button(
        button,
        shell_spec=shell_spec,
        collapsed=collapsed,
        selected=False,
    )
    return button


def _style_navigation_button(
    button,
    shell_spec: PrototypeShellSpec,
    collapsed: bool,
    selected: bool,
) -> None:
    icon_size = 24
    label_size = shell_spec.typography.navigation_size + 1
    color = COLOR_ACCENT_PRIMARY if selected else COLOR_TEXT_SECONDARY
    background = "rgba(242, 26, 135, 36)" if selected else "transparent"
    border = (
        f"1px solid rgba(242, 26, 135, 76)"
        if selected
        else "1px solid transparent"
    )
    font_weight = 650 if selected else 500

    button.setStyleSheet(
        f"""
        QFrame#NavigationItem {{
            background-color: {background};
            border: {border};
            border-radius: 12px;
        }}
        QFrame#NavigationItem:hover {{
            background-color: {COLOR_SURFACE_CARD_SOFT};
            border: 1px solid transparent;
        }}
        QLabel#NavigationIcon {{
            color: {color};
            background: transparent;
            border: none;
            font-size: {icon_size}px;
            font-weight: {font_weight};
        }}
        QLabel#NavigationText {{
            color: {color};
            background: transparent;
            border: none;
            font-size: {label_size}px;
            font-weight: {font_weight};
        }}
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
    primary_intention_text = (
        "Overview and next steps for your farming operations."
        if home_concept is not None
        else screen.primary_intention
    )
    primary_intention_label = QLabel(primary_intention_text)
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
    open_companion_mode,
):
    from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

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
    layout.addSpacing(4)

    controller = FrontendAutomationController(
        session_id_provider=lambda: "prototype-prepared-session",
    )
    active_automations = tuple(get_active_automation_definitions())
    selected_automation_id = {"value": active_automations[0].automation_id}
    selected_companion_state = {"value": None}

    selector_label = QLabel("Select supervised operation")
    _style_eyebrow_label(selector_label, primary=False)
    layout.addWidget(selector_label)

    selector_row = QHBoxLayout()
    selector_row.setContentsMargins(0, 0, 0, 0)
    selector_row.setSpacing(shell_spec.vertical_rhythm.group_spacing)
    selector_buttons = {}
    for definition in active_automations:
        button = QPushButton(_automation_selector_label(definition.automation_id))
        _style_automation_selector_button(
            button,
            shell_spec=shell_spec,
            selected=definition.automation_id == selected_automation_id["value"],
        )
        selector_buttons[definition.automation_id] = button
        selector_row.addWidget(button)
    layout.addLayout(selector_row)
    layout.addSpacing(6)

    overview = _build_preparation_text_card(
        eyebrow="SELECTED AUTOMATION",
        shell_spec=shell_spec,
        treatment="primary action",
    )
    profile = _build_preparation_text_card(
        eyebrow="ACTIVE PROFILE",
        shell_spec=shell_spec,
        treatment="primary behavior summary",
    )
    readiness = _build_preparation_text_card(
        eyebrow="READINESS",
        shell_spec=shell_spec,
        treatment="primary confidence check",
    )
    warnings = _build_preparation_text_card(
        eyebrow="CONTEXTUAL WARNINGS",
        shell_spec=shell_spec,
        treatment="secondary contextual support",
    )
    run = _build_preparation_text_card(
        eyebrow="RUN PREPARATION",
        shell_spec=shell_spec,
        treatment="primary action",
    )

    layout.addWidget(overview["card"])
    layout.addSpacing(6)
    layout.addLayout(
        _build_card_row(
            cards=(profile["card"], readiness["card"]),
            shell_spec=shell_spec,
        )
    )
    layout.addSpacing(6)
    layout.addWidget(warnings["card"])
    layout.addSpacing(6)

    prepare_button = QPushButton("Prepare Run")
    _style_primary_button(prepare_button, shell_spec=shell_spec)
    run["layout"].addWidget(prepare_button)
    companion_button = QPushButton("Open Companion Mode Preview")
    companion_button.setEnabled(False)
    _style_secondary_button(companion_button, shell_spec=shell_spec)
    run["layout"].addWidget(companion_button)
    layout.addWidget(run["card"])

    preparation_cards = {
        "overview": overview,
        "profile": profile,
        "readiness": readiness,
        "warnings": warnings,
        "run": run,
    }

    def render_preparation_state(automation_id: str, prepared: bool = False) -> None:
        selected_automation_id["value"] = automation_id
        if not prepared:
            selected_companion_state["value"] = None
            companion_button.setEnabled(False)
        for button_automation_id, button in selector_buttons.items():
            _style_automation_selector_button(
                button,
                shell_spec=shell_spec,
                selected=button_automation_id == automation_id,
            )

        definition = get_automation_definition(automation_id)
        profile_id = definition.available_profiles[0]
        plan = controller.prepare_run_plan(
            AutomationRunRequest(
                automation_id=automation_id,
                profile_id=profile_id,
                requested_count=1,
            )
        )

        if not plan.accepted:
            _set_preparation_card_text(
                preparation_cards["overview"],
                title=f"{definition.display_name} cannot be prepared",
                summary="The request was refused before any operation could begin.",
                details=(plan.refusal_message or "Review readiness before continuing.",),
            )
            return

        profile_metadata = plan.profile_metadata
        readiness_model = plan.readiness_model
        _set_preparation_card_text(
            preparation_cards["overview"],
            title=definition.display_name,
            summary=_compact_text(definition.short_purpose, 96),
            details=(
                f"Validated scope: {_compact_text(definition.validated_scope, 72)}",
                _compact_text(definition.expected_baseline, 112),
            ),
        )
        _set_preparation_card_text(
            preparation_cards["profile"],
            title=profile_metadata.profile_name,
            summary=_compact_text(profile_metadata.behavior_summary, 94),
            details=(
                _compact_text(profile_metadata.reliability_posture, 78),
                f"Confidence: {profile_metadata.validation_confidence.value}",
            ),
        )
        _set_preparation_card_text(
            preparation_cards["readiness"],
            title=_compact_text(readiness_model.readiness_wording, 76),
            summary=_compact_text(readiness_model.focus_requirement, 74),
            details=tuple(_compact_text(note, 78) for note in readiness_model.confidence_notes[:2]),
        )
        _set_preparation_card_text(
            preparation_cards["warnings"],
            title="Contextual warnings",
            summary=_format_warning_summary(plan.warnings),
            details=(
                (
                    plan.warnings[1]
                    if len(plan.warnings) > 1
                    else "Warnings are informational until preparation is confirmed."
                ),
            ),
        )
        _set_preparation_card_text(
            preparation_cards["run"],
            title=(
                "Prepared for supervised operation"
                if prepared
                else "Prepare the run plan"
            ),
            summary=(
                "Ready for focus handoff. No execution has started."
                if prepared
                else "Confirm the selected automation, profile, readiness and warnings."
            ),
            details=(
                f"Selected: {definition.display_name}. Requested cycles: 1.",
                (
                    "Prepared state only. Companion preview is available."
                    if prepared
                    else "Preparation only. No runner or real input is connected."
                ),
            ),
        )
        if prepared:
            selected_companion_state["value"] = {
                "automation_name": definition.display_name,
                "profile_name": profile_metadata.profile_name,
                "status": "Running",
                "progress": "Cycle 1 of 1 - supervision placeholder",
                "focus": "FH6 focus handoff ready",
                "stop": "F8 emergency stop available",
                "summary": "Supervised operation preview. No automation is executing.",
            }
            companion_button.setEnabled(True)

    def select_automation(automation_id: str) -> None:
        render_preparation_state(automation_id, prepared=False)

    for automation_id, button in selector_buttons.items():
        button.clicked.connect(
            lambda _checked=False, selected_id=automation_id: select_automation(selected_id)
        )

    prepare_button.clicked.connect(
        lambda: render_preparation_state(selected_automation_id["value"], prepared=True)
    )
    companion_button.clicked.connect(
        lambda: open_companion_mode(selected_companion_state["value"])
        if selected_companion_state["value"] is not None
        else None
    )
    render_preparation_state(selected_automation_id["value"], prepared=False)

    layout.addStretch()
    return container


def _build_home_screen_content(
    layout,
    home_concept: PrototypeHomeConcept,
    shell_spec: PrototypeShellSpec,
    open_automation_environment,
) -> None:
    layout.addWidget(
        _build_visual_card(
            title="Ready when the baseline is clear",
            summary="Controlled preparation before supervised operation.",
            details=("System ready",),
            shell_spec=shell_spec,
            treatment="hero",
        )
    )
    layout.addSpacing(shell_spec.vertical_rhythm.important_element_spacing)

    layout.addWidget(
        _build_action_card(
            eyebrow=home_concept.signals[0].title,
            title=home_concept.signals[0].summary,
            summary="Review baseline, requirements and environment before starting.",
            button_text=home_concept.primary_action_label,
            shell_spec=shell_spec,
            treatment="primary action",
            primary=True,
            action_callback=open_automation_environment,
        )
    )
    layout.addSpacing(shell_spec.vertical_rhythm.section_spacing)

    layout.addWidget(
        _build_action_card(
            eyebrow=home_concept.signals[1].title,
            title=home_concept.signals[1].summary,
            summary="Check profile, readiness, warnings and commitment before proceeding.",
            button_text="Open Review",
            shell_spec=shell_spec,
            treatment="secondary action",
            primary=False,
            action_callback=open_automation_environment,
        )
    )
    layout.addSpacing(shell_spec.vertical_rhythm.section_spacing)

    layout.addLayout(
        _build_card_row(
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
    )


def _build_companion_mode_widget(
    shell_spec: PrototypeShellSpec,
    return_to_preparation,
    open_completion_state,
):
    from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(10)

    title_label = QLabel(shell_spec.companion_mode.title)
    subtitle_label = QLabel(shell_spec.companion_mode.primary_intention)
    _style_screen_title(title_label, shell_spec=shell_spec)
    _style_summary_label(subtitle_label, shell_spec=shell_spec)
    layout.addWidget(title_label)
    layout.addWidget(subtitle_label)
    layout.addSpacing(6)

    status_card = _build_preparation_text_card(
        eyebrow="AUTOMATION STATUS",
        shell_spec=shell_spec,
        treatment="commitment",
    )
    operation_card = _build_preparation_text_card(
        eyebrow="CURRENT OPERATION",
        shell_spec=shell_spec,
        treatment="primary orientation",
    )
    focus_card = _build_preparation_text_card(
        eyebrow="FH6 FOCUS",
        shell_spec=shell_spec,
        treatment="primary confidence check",
    )
    profile_card = _build_preparation_text_card(
        eyebrow="ACTIVE PROFILE",
        shell_spec=shell_spec,
        treatment="secondary contextual support",
    )
    reassurance_card = _build_preparation_text_card(
        eyebrow="OPERATIONAL REASSURANCE",
        shell_spec=shell_spec,
        treatment="tertiary",
    )
    stop_card = _build_preparation_text_card(
        eyebrow="STOP SAFELY",
        shell_spec=shell_spec,
        treatment="primary action",
    )

    layout.addWidget(status_card["card"])
    layout.addSpacing(6)
    layout.addWidget(operation_card["card"])
    layout.addSpacing(6)
    layout.addLayout(
        _build_card_row(
            cards=(focus_card["card"], profile_card["card"]),
            shell_spec=shell_spec,
        )
    )
    layout.addSpacing(6)
    layout.addWidget(reassurance_card["card"])
    layout.addSpacing(6)
    layout.addWidget(stop_card["card"])

    back_button = QPushButton("Return to Preparation")
    _style_secondary_button(back_button, shell_spec=shell_spec)
    back_button.clicked.connect(return_to_preparation)
    layout.addSpacing(6)

    prototype_outcome_row = QHBoxLayout()
    prototype_outcome_row.setContentsMargins(0, 0, 0, 0)
    prototype_outcome_row.setSpacing(shell_spec.vertical_rhythm.group_spacing)
    completed_button = QPushButton("Preview Completed")
    stopped_button = QPushButton("Preview Stopped")
    refused_button = QPushButton("Preview Paused")
    for button in (completed_button, stopped_button, refused_button):
        _style_secondary_button(button, shell_spec=shell_spec)
        prototype_outcome_row.addWidget(button)
    layout.addLayout(prototype_outcome_row)
    layout.addWidget(back_button)
    layout.addStretch()

    current_companion_state = {
        "value": {
            "automation_name": "No prepared run",
            "profile_name": "Prepare a run first",
            "status": "Not running",
            "progress": "No cycle active",
            "focus": "FH6 focus handoff not active",
            "stop": "F8 guidance appears after preparation",
            "summary": "Companion Mode is waiting for a prepared run preview.",
        }
    }

    def update_companion_mode(companion_state: dict[str, str]) -> None:
        current_companion_state["value"] = companion_state
        _set_preparation_card_text(
            status_card,
            title=companion_state["status"],
            summary=shell_spec.companion_mode.operation_label,
            details=(companion_state["summary"],),
        )
        _set_preparation_card_text(
            operation_card,
            title=companion_state["automation_name"],
            summary=companion_state["progress"],
            details=("Prepared state only. No automation is executing from this UI.",),
        )
        _set_preparation_card_text(
            focus_card,
            title=companion_state["focus"],
            summary="Focus handoff status placeholder",
            details=("Automatic focus handoff can be represented here later.",),
        )
        _set_preparation_card_text(
            profile_card,
            title=companion_state["profile_name"],
            summary="Safe default profile",
            details=("Profile assumptions remain active for this prepared run.",),
        )
        _set_preparation_card_text(
            reassurance_card,
            title="Supervise confidently",
            summary="Keep FH6 visible and the operation under observation.",
            details=("Completion and recovery states will follow in a later milestone.",),
        )
        _set_preparation_card_text(
            stop_card,
            title="Stop safely",
            summary=companion_state["stop"],
            details=("Calm stop guidance only. This prototype does not send input.",),
        )

    completed_button.clicked.connect(
        lambda: open_completion_state("completed", current_companion_state["value"])
    )
    stopped_button.clicked.connect(
        lambda: open_completion_state("stopped", current_companion_state["value"])
    )
    refused_button.clicked.connect(
        lambda: open_completion_state("refused", current_companion_state["value"])
    )
    update_companion_mode(current_companion_state["value"])

    return container, update_companion_mode


def _build_completion_state_widget(
    shell_spec: PrototypeShellSpec,
    return_to_preparation,
):
    from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(10)

    title_label = QLabel(shell_spec.completion_lifecycle.title)
    subtitle_label = QLabel(shell_spec.completion_lifecycle.primary_intention)
    _style_screen_title(title_label, shell_spec=shell_spec)
    _style_summary_label(subtitle_label, shell_spec=shell_spec)
    layout.addWidget(title_label)
    layout.addWidget(subtitle_label)
    layout.addSpacing(8)

    outcome_card = _build_preparation_text_card(
        eyebrow="OUTCOME",
        shell_spec=shell_spec,
        treatment="primary orientation",
    )
    summary_card = _build_preparation_text_card(
        eyebrow="WHAT HAPPENED",
        shell_spec=shell_spec,
        treatment="secondary contextual support",
    )
    next_step_card = _build_preparation_text_card(
        eyebrow="SUGGESTED NEXT STEP",
        shell_spec=shell_spec,
        treatment="primary action",
    )
    reassurance_card = _build_preparation_text_card(
        eyebrow="CONTROLLED RECOVERY",
        shell_spec=shell_spec,
        treatment="tertiary",
    )

    layout.addWidget(outcome_card["card"])
    layout.addSpacing(6)
    layout.addWidget(summary_card["card"])
    layout.addSpacing(6)
    layout.addWidget(next_step_card["card"])
    layout.addSpacing(6)
    layout.addWidget(reassurance_card["card"])
    layout.addSpacing(8)

    back_button = QPushButton("Return to Automation Environment")
    _style_primary_button(back_button, shell_spec=shell_spec)
    back_button.clicked.connect(return_to_preparation)
    layout.addWidget(back_button)
    layout.addStretch()

    states_by_id = {
        state.state_id: state for state in shell_spec.completion_lifecycle.states
    }

    def update_completion_state(state_id: str, companion_state: dict[str, str]) -> None:
        state = states_by_id.get(state_id, states_by_id["refused"])
        automation_name = companion_state.get("automation_name", "Prepared operation")
        profile_name = companion_state.get("profile_name", "Selected profile")

        _set_preparation_card_text(
            outcome_card,
            title=state.title,
            summary=state.emotional_treatment,
            details=(automation_name,),
        )
        _set_preparation_card_text(
            summary_card,
            title=state.summary,
            summary=profile_name,
            details=("Prototype-only lifecycle state. No automation result was produced.",),
        )
        _set_preparation_card_text(
            next_step_card,
            title=state.suggested_next_step,
            summary="Return to preparation when ready.",
            details=("No dead-end state. No execution is connected here.",),
        )
        _set_preparation_card_text(
            reassurance_card,
            title=state.reassurance,
            summary="The interface remains in a controlled manual flow.",
            details=("Review, prepare, or stop without mode shock.",),
        )

    update_completion_state(
        "completed",
        {
            "automation_name": "No completed run",
            "profile_name": "Prepare a run first",
        },
    )

    return container, update_completion_state


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


def _short_automation_label(automation_id: str) -> str:
    labels = {
        "auto1": "Auto1",
        "auto2": "Auto2",
        "auto3": "Auto3",
    }
    return labels.get(automation_id, automation_id)


def _automation_selector_label(automation_id: str) -> str:
    labels = {
        "auto1": "Auto1 Race",
        "auto2": "Auto2 Buy",
        "auto3": "Auto3 Skill",
    }
    return labels.get(automation_id, _short_automation_label(automation_id))


def _build_preparation_text_card(
    eyebrow: str,
    shell_spec: PrototypeShellSpec,
    treatment: str,
) -> dict[str, object]:
    from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout

    card = QFrame()
    card.setObjectName("PrototypeCard")
    card.setFrameShape(QFrame.Shape.NoFrame)
    card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    _style_visual_card(card, treatment=treatment)

    card_layout = QVBoxLayout(card)
    card_layout.setContentsMargins(14, 10, 14, 10)
    card_layout.setSpacing(4)

    eyebrow_label = QLabel(eyebrow)
    _style_eyebrow_label(eyebrow_label, primary="primary" in treatment)
    title_label = QLabel()
    _style_card_title(title_label, shell_spec=shell_spec, treatment=treatment)
    summary_label = QLabel()
    _style_summary_label(summary_label, shell_spec=shell_spec)
    detail_label = QLabel()
    _style_detail_label(detail_label, shell_spec=shell_spec)

    card_layout.addWidget(eyebrow_label)
    card_layout.addWidget(title_label)
    card_layout.addWidget(summary_label)
    card_layout.addWidget(detail_label)

    return {
        "card": card,
        "layout": card_layout,
        "title": title_label,
        "summary": summary_label,
        "detail": detail_label,
    }


def _set_preparation_card_text(
    card_parts: dict[str, object],
    title: str,
    summary: str,
    details: tuple[str, ...],
) -> None:
    card_parts["title"].setText(title)
    card_parts["summary"].setText(summary)
    card_parts["detail"].setText(" ".join(detail for detail in details if detail))


def _format_warning_summary(warnings: tuple[str, ...]) -> str:
    if not warnings:
        return "No contextual warnings for this selected automation."
    return warnings[0]


def _compact_text(text: str, max_length: int) -> str:
    if len(text) <= max_length:
        return text
    return f"{text[: max_length - 1].rstrip()}..."


def _build_action_card(
    eyebrow: str,
    title: str,
    summary: str,
    button_text: str,
    shell_spec: PrototypeShellSpec,
    treatment: str,
    primary: bool,
    action_callback,
):
    from PySide6.QtWidgets import (
        QFrame,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QSizePolicy,
        QVBoxLayout,
        QWidget,
    )

    card = QFrame()
    card.setObjectName("PrototypeCard")
    card.setFrameShape(QFrame.Shape.NoFrame)
    card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    _style_visual_card(card, treatment=treatment)

    card_layout = QHBoxLayout(card)
    card_layout.setContentsMargins(14, 12, 14, 12)
    card_layout.setSpacing(10)

    if _uses_accent_strip(treatment):
        card_layout.addWidget(_build_accent_strip(QFrame))

    content = QWidget()
    content.setStyleSheet("background: transparent; border: none;")
    content_layout = QVBoxLayout(content)
    content_layout.setContentsMargins(0, 0, 0, 0)
    content_layout.setSpacing(6)

    eyebrow_label = QLabel(eyebrow)
    _style_eyebrow_label(eyebrow_label, primary=primary)
    title_label = QLabel(title)
    _style_action_title(title_label, primary=primary)
    summary_label = QLabel(summary)
    _style_detail_label(summary_label, shell_spec=shell_spec)

    button = QPushButton(button_text)
    if primary:
        _style_primary_button(button, shell_spec=shell_spec)
    else:
        _style_secondary_button(button, shell_spec=shell_spec)

    if action_callback is not None:
        button.clicked.connect(action_callback)

    content_layout.addWidget(eyebrow_label)
    content_layout.addWidget(title_label)
    content_layout.addWidget(summary_label)
    content_layout.addWidget(button)
    card_layout.addWidget(content)

    return card


def _build_card_row(cards: tuple[object, object], shell_spec: PrototypeShellSpec):
    from PySide6.QtWidgets import QHBoxLayout

    row = QHBoxLayout()
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(shell_spec.vertical_rhythm.group_spacing)
    for card in cards:
        row.addWidget(card)

    return row


def _build_footer_metadata_label(text: str, shell_spec: PrototypeShellSpec):
    from PySide6.QtWidgets import QLabel

    label = QLabel(text)
    _style_footer_label(label, shell_spec=shell_spec)
    return label


def _build_visual_card(
    title: str,
    summary: str,
    details: tuple[str, ...],
    shell_spec: PrototypeShellSpec,
    treatment: str,
):
    from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget

    card = QFrame()
    card.setObjectName("PrototypeCard")
    card.setFrameShape(QFrame.Shape.NoFrame)
    card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    _style_visual_card(card, treatment=treatment)

    card_layout = QHBoxLayout(card)
    card_layout.setContentsMargins(
        shell_spec.vertical_rhythm.group_inner_margin + 2,
        shell_spec.vertical_rhythm.group_inner_margin,
        shell_spec.vertical_rhythm.group_inner_margin + 2,
        shell_spec.vertical_rhythm.group_inner_margin,
    )
    card_layout.setSpacing(10)

    if _uses_accent_strip(treatment):
        card_layout.addWidget(_build_accent_strip(QFrame))

    content = QWidget()
    content.setStyleSheet("background: transparent; border: none;")
    content_layout = QVBoxLayout(content)
    content_layout.setContentsMargins(0, 0, 0, 0)
    content_layout.setSpacing(6)

    title_label = QLabel(title)
    summary_label = QLabel(summary)
    _style_card_title(title_label, shell_spec=shell_spec, treatment=treatment)
    _style_summary_label(summary_label, shell_spec=shell_spec)
    content_layout.addWidget(title_label)
    content_layout.addWidget(summary_label)

    for detail in details:
        detail_label = QLabel(detail)
        _style_detail_label(detail_label, shell_spec=shell_spec)
        content_layout.addWidget(detail_label)

    card_layout.addWidget(content)

    return card


def _uses_accent_strip(treatment: str) -> bool:
    return (
        treatment == "hero"
        or "primary action" in treatment
        or "commitment" in treatment
    )


def _build_accent_strip(frame_type):
    strip = frame_type()
    strip.setFixedWidth(4)
    strip.setStyleSheet(
        f"""
        QFrame {{
            background-color: {COLOR_ACCENT_PRIMARY};
            border: none;
            border-radius: 2px;
        }}
        """
    )
    return strip


def _style_visual_card(card, treatment: str) -> None:
    if treatment == "hero":
        card.setStyleSheet(
            f"""
            QFrame#PrototypeCard {{
                background-color: {COLOR_SURFACE_CARD_RAISED};
                border: 1px solid {COLOR_BORDER_SUBTLE};
                border-radius: 18px;
            }}
            """
        )
        return

    if "primary action" in treatment:
        card.setStyleSheet(
            f"""
            QFrame#PrototypeCard {{
                background-color: {COLOR_SURFACE_CARD_RAISED};
                border: 1px solid {COLOR_ACCENT_PRIMARY};
                border-radius: 18px;
            }}
            """
        )
        return

    if "secondary action" in treatment:
        card.setStyleSheet(
            f"""
            QFrame#PrototypeCard {{
                background-color: {COLOR_SURFACE_CARD};
                border: 1px solid {COLOR_BORDER_SUBTLE};
                border-radius: 16px;
            }}
            """
        )
        return

    if "tertiary" in treatment:
        card.setStyleSheet(
            f"""
            QFrame#PrototypeCard {{
                background-color: {COLOR_SURFACE_RECESSED};
                border: 1px solid {COLOR_BORDER_SUBTLE};
                border-radius: 14px;
            }}
            """
        )
        return

    if "secondary" in treatment:
        card.setStyleSheet(
            f"""
            QFrame#PrototypeCard {{
                background-color: {COLOR_SURFACE_CARD_SOFT};
                border: 1px solid {COLOR_BORDER_SUBTLE};
                border-radius: 14px;
            }}
            """
        )
        return

    if "commitment" in treatment:
        card.setStyleSheet(
            f"""
            QFrame#PrototypeCard {{
                background-color: {COLOR_SURFACE_CARD_RAISED};
                border: 1px solid {COLOR_ACCENT_PRIMARY};
                border-radius: 18px;
            }}
            """
        )
        return

    card.setStyleSheet(
        f"""
        QFrame#PrototypeCard {{
            background-color: {COLOR_SURFACE_CARD};
            border: 1px solid {COLOR_BORDER_SUBTLE};
            border-radius: 16px;
        }}
        """
    )


def _style_card_title(label, shell_spec: PrototypeShellSpec, treatment: str) -> None:
    color = COLOR_TEXT_PRIMARY
    weight = 620
    size = shell_spec.typography.section_title_size
    if treatment == "hero":
        size = 18
        weight = 680
    if "secondary" in treatment or "tertiary" in treatment:
        color = COLOR_TEXT_SECONDARY
        weight = 560

    label.setStyleSheet(
        f"font-size: {size}px; "
        f"font-weight: {weight}; color: {color}; "
        "background: transparent; border: none;"
    )
    label.setWordWrap(True)


def _style_eyebrow_label(label, primary: bool) -> None:
    color = COLOR_ACCENT_PRIMARY if primary else COLOR_TEXT_MUTED
    label.setStyleSheet(
        f"font-size: 10px; font-weight: 700; color: {color}; "
        "letter-spacing: 1px; background: transparent; border: none;"
    )
    label.setWordWrap(True)


def _style_action_title(label, primary: bool) -> None:
    size = 18 if primary else 16
    weight = 680 if primary else 620
    label.setStyleSheet(
        f"font-size: {size}px; font-weight: {weight}; "
        f"color: {COLOR_TEXT_PRIMARY}; background: transparent; border: none;"
    )
    label.setWordWrap(True)


def _style_screen_title(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.screen_title_size}px; "
        f"font-weight: 650; color: {COLOR_TEXT_PRIMARY}; "
        "background: transparent; border: none;"
    )
    label.setWordWrap(True)


def _style_summary_label(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.summary_size}px; "
        f"font-weight: 500; color: {COLOR_TEXT_SECONDARY}; "
        "background: transparent; border: none;"
    )
    label.setWordWrap(True)


def _style_detail_label(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.detail_size}px; "
        f"font-weight: 400; color: {COLOR_TEXT_MUTED}; "
        "background: transparent; border: none;"
    )
    label.setWordWrap(True)


def _style_navigation_label(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.navigation_size}px; "
        f"font-weight: 600; color: {COLOR_TEXT_PRIMARY}; "
        "background: transparent; border: none;"
    )


def _style_footer_label(label, shell_spec: PrototypeShellSpec) -> None:
    label.setStyleSheet(
        f"font-size: {shell_spec.typography.footer_size}px; "
        f"font-weight: 400; color: {COLOR_TEXT_MUTED}; "
        "background: transparent; border: none;"
    )
    label.setWordWrap(True)


def _style_primary_button(button, shell_spec: PrototypeShellSpec) -> None:
    button.setStyleSheet(
        f"""
        QPushButton {{
            font-size: {shell_spec.typography.summary_size}px;
            font-weight: 620;
            color: #ffffff;
            background-color: {COLOR_ACCENT_PRIMARY};
            border: 1px solid {COLOR_ACCENT_PRIMARY};
            border-radius: 12px;
            padding: 8px 10px;
        }}
        QPushButton:hover {{
            background-color: {COLOR_ACCENT_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {COLOR_ACCENT_PRESSED};
        }}
        """
    )


def _style_secondary_button(button, shell_spec: PrototypeShellSpec) -> None:
    button.setStyleSheet(
        f"""
        QPushButton {{
            font-size: {shell_spec.typography.summary_size}px;
            font-weight: 600;
            color: {COLOR_TEXT_PRIMARY};
            background-color: transparent;
            border: 1px solid {COLOR_BORDER_STRONG};
            border-radius: 12px;
            padding: 8px 10px;
        }}
        QPushButton:hover {{
            background-color: {COLOR_SURFACE_CARD_SOFT};
            border: 1px solid {COLOR_TEXT_MUTED};
        }}
        QPushButton:pressed {{
            background-color: {COLOR_SURFACE_RECESSED};
        }}
        QPushButton:disabled {{
            color: {COLOR_TEXT_FAINT};
            background-color: transparent;
            border: 1px solid {COLOR_BORDER_SUBTLE};
        }}
        """
    )


def _style_automation_selector_button(
    button,
    shell_spec: PrototypeShellSpec,
    selected: bool,
) -> None:
    background = "rgba(242, 26, 135, 34)" if selected else COLOR_SURFACE_RECESSED
    border = (
        f"1px solid rgba(242, 26, 135, 82)"
        if selected
        else f"1px solid {COLOR_BORDER_SUBTLE}"
    )
    color = COLOR_ACCENT_PRIMARY if selected else COLOR_TEXT_SECONDARY
    button.setStyleSheet(
        f"""
        QPushButton {{
            font-size: {shell_spec.typography.summary_size}px;
            font-weight: 640;
            color: {color};
            background-color: {background};
            border: {border};
            border-radius: 12px;
            padding: 8px 10px;
        }}
        QPushButton:hover {{
            background-color: {COLOR_SURFACE_CARD_SOFT};
            color: {COLOR_TEXT_PRIMARY};
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
