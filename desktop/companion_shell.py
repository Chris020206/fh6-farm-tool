from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from frontend.automation_controller import (
    AutomationRunRequest,
    FrontendAutomationController,
)
from desktop.execution.auto1_desktop_execution import (
    AUTO1_LOOP_COUNT_MAX,
    AUTO1_LOOP_COUNT_MIN,
    AUTO1_RACE_DURATION_EXECUTION_BUFFER_SECONDS,
    AUTO1_RACE_DURATION_MAX_SECONDS,
    AUTO1_RACE_DURATION_MIN_SECONDS,
    auto1_execution_race_duration,
    build_auto1_ui_execution_profile,
    load_auto1_default_race_duration,
    parse_auto1_loop_count,
    parse_auto1_race_duration_override,
    start_auto1_ui_execution,
)
from desktop.execution.auto2_desktop_execution import (
    parse_auto2_purchase_count,
    start_auto2_ui_execution,
)
from desktop.execution.auto3_desktop_execution import (
    parse_auto3_car_count,
    start_auto3_ui_execution,
)
from desktop.execution.execution_boundary import (
    is_desktop_execution_supported,
    is_desktop_preparation_available,
)
from desktop.execution.execution_messages import (
    completion_state_id_for_status,
    completion_state_id_for_auto1_status,
    desktop_execution_confirmation_summary,
    desktop_execution_refusal_details,
    summarize_ui_execution_error,
    summarize_auto1_ui_execution_error,
)
from desktop.execution.focus_handoff import (
    DEFAULT_FH6_TARGET_TITLE,
    attempt_ui_focus_handoff,
    format_ui_focus_failure_message,
)
from product.automation_registry import get_automation_definition
from product.automation_registry import get_all_automation_definitions
from product.automation_registry import get_active_automation_definitions
from product.profile_metadata_registry import get_all_profile_metadata
from product.profile_metadata_registry import get_profile_metadata
from product.readiness_registry import get_all_readiness_models
from product.readiness_registry import get_readiness_model
from sessions.operational_history import OperationalHistoryEntry
from sessions.session_status import SessionStatus
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
from ui.help_screen import build_help_screen
from ui.history_screen import build_history_screen
from ui.profiles_screen import build_profiles_screen
from ui.settings_screen import build_settings_screen
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
DESKTOP_BRAND_LOGO_PATH = Path(__file__).with_name("assets") / "fh6_farm_tool_logo.png"
DESKTOP_BRAND_LOGO_MAX_WIDTH = 252
DESKTOP_BRAND_LOGO_MAX_HEIGHT = 46
DESKTOP_APP_ICON_PATH = Path(__file__).resolve().parents[1] / "assets" / "branding" / "app_icon.ico"
DESKTOP_APP_ICON_FALLBACK_PATH = (
    Path(__file__).resolve().parents[1] / "assets" / "branding" / "tray_icon.png"
)
DESKTOP_APP_USER_MODEL_ID = "FH6FarmTool.Desktop"
DESKTOP_APP_VERSION = "v0.2.0-beta"
DESKTOP_APP_BUILD_TYPE = "Founding Tester Beta"
DESKTOP_PRODUCT_NAME = "Forza Automation Assist"
DESKTOP_ABOUT_TITLE = f"About {DESKTOP_PRODUCT_NAME}"
DESKTOP_ABOUT_LINES = (
    DESKTOP_PRODUCT_NAME,
    f"Version: {DESKTOP_APP_VERSION}",
    f"Build type: {DESKTOP_APP_BUILD_TYPE}",
    "",
    "A supervised desktop automation utility for Forza Horizon 6.",
    "",
    "Controlled/manual beta. Not unattended automation.",
    "Keep F8 available during automation.",
    "",
    "Support: project Discord",
    f"© 2026 {DESKTOP_PRODUCT_NAME}",
)
DESKTOP_TRAY_TOOLTIP = DESKTOP_PRODUCT_NAME
DESKTOP_TRAY_ACTION_LABELS = (
    f"Show {DESKTOP_PRODUCT_NAME}",
    "Hide to Tray",
    DESKTOP_ABOUT_TITLE,
    "Exit",
)
NAVIGATION_ICON_SLOT_WIDTH = 42


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
class PrototypeCommitmentLayer:
    title: str
    primary_intention: str
    readiness_label: str
    focus_label: str
    profile_label: str
    stop_label: str
    focus_method_labels: tuple[str, str]
    countdown_values: tuple[int, ...]
    focus_methods_share_countdown: bool
    is_last_safe_exit: bool
    introduces_execution: bool


@dataclass(frozen=True)
class PrototypeExecutionWiring:
    enabled_automation_ids: tuple[str, ...]
    refused_automation_ids: tuple[str, ...]
    uses_existing_guarded_paths: bool
    preserves_f8_stop: bool
    fail_closed_for_unsupported_automations: bool


@dataclass(frozen=True)
class PrototypeWorkflowContract:
    transitions: tuple[tuple[str, str], ...]
    dead_button_policy: str
    unsupported_execution_policy: str
    state_reset_policy: str
    real_input_boundary: str
    stop_policy: str


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
    commitment_layer: PrototypeCommitmentLayer
    execution_wiring: PrototypeExecutionWiring
    workflow_contract: PrototypeWorkflowContract
    companion_mode: PrototypeCompanionMode
    completion_lifecycle: PrototypeCompletionLifecycle


def build_prototype_shell_spec() -> PrototypeShellSpec:
    sidebar_destinations = get_sidebar_destinations()

    return PrototypeShellSpec(
        window_title=DESKTOP_PRODUCT_NAME,
        window_width=640,
        window_height=960,
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
        commitment_layer=_build_prototype_commitment_layer(),
        execution_wiring=_build_prototype_execution_wiring(),
        workflow_contract=_build_prototype_workflow_contract(),
        companion_mode=_build_prototype_companion_mode(),
        completion_lifecycle=_build_prototype_completion_lifecycle(),
    )


def _desktop_app_icon_path() -> Path | None:
    if DESKTOP_APP_ICON_PATH.exists():
        return DESKTOP_APP_ICON_PATH
    if DESKTOP_APP_ICON_FALLBACK_PATH.exists():
        return DESKTOP_APP_ICON_FALLBACK_PATH
    return None


def _set_windows_app_user_model_id() -> None:
    import sys

    if sys.platform != "win32":
        return

    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            DESKTOP_APP_USER_MODEL_ID
        )
    except Exception:
        return


def _desktop_about_text() -> str:
    return "\n".join(DESKTOP_ABOUT_LINES)


def _desktop_visible_version_text() -> str:
    return DESKTOP_APP_VERSION


def _show_about_dialog(parent, icon) -> None:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QMessageBox

    dialog = QMessageBox(parent)
    dialog.setWindowTitle(DESKTOP_ABOUT_TITLE)
    dialog.setText(_desktop_about_text())
    dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
    if not icon.isNull():
        dialog.setWindowIcon(icon)
        dialog.setIconPixmap(
            icon.pixmap(64, 64).scaled(
                48,
                48,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
    dialog.exec()


def _install_system_tray(app, window, icon) -> object | None:
    from PySide6.QtGui import QAction
    from PySide6.QtWidgets import QMenu, QSystemTrayIcon

    if icon.isNull() or not QSystemTrayIcon.isSystemTrayAvailable():
        return None

    tray_icon = QSystemTrayIcon(icon, window)
    tray_icon.setToolTip(DESKTOP_TRAY_TOOLTIP)
    tray_menu = QMenu(window)

    show_action = QAction(DESKTOP_TRAY_ACTION_LABELS[0], tray_menu)
    hide_action = QAction(DESKTOP_TRAY_ACTION_LABELS[1], tray_menu)
    about_action = QAction(DESKTOP_TRAY_ACTION_LABELS[2], tray_menu)
    exit_action = QAction(DESKTOP_TRAY_ACTION_LABELS[3], tray_menu)

    def show_window() -> None:
        window.showNormal()
        window.raise_()
        window.activateWindow()

    show_action.triggered.connect(show_window)
    hide_action.triggered.connect(window.hide)
    about_action.triggered.connect(lambda: _show_about_dialog(window, icon))
    exit_action.triggered.connect(app.quit)

    tray_menu.addAction(show_action)
    tray_menu.addAction(hide_action)
    tray_menu.addAction(about_action)
    tray_menu.addSeparator()
    tray_menu.addAction(exit_action)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.activated.connect(
        lambda reason: show_window()
        if reason == QSystemTrayIcon.ActivationReason.Trigger
        else None
    )
    tray_icon.show()
    return tray_icon


def launch_pyside6_shell_prototype() -> int:
    try:
        from PySide6.QtCore import QPropertyAnimation, QRect, QTimer
        from PySide6.QtGui import QIcon
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
            QSystemTrayIcon,
            QVBoxLayout,
            QWidget,
        )
    except ImportError as error:
        raise SystemExit(
            "PySide6 is not installed. Install PySide6 before launching the desktop app."
        ) from error

    import sys

    shell_spec = build_prototype_shell_spec()
    _set_windows_app_user_model_id()
    app = QApplication(sys.argv)
    app.setStyleSheet(_global_stylesheet())
    app_icon_path = _desktop_app_icon_path()
    app_icon = QIcon(str(app_icon_path)) if app_icon_path is not None else QIcon()
    if not app_icon.isNull():
        app.setWindowIcon(app_icon)

    window = QMainWindow()
    window.setWindowTitle(shell_spec.window_title)
    if not app_icon.isNull():
        window.setWindowIcon(app_icon)
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
    commitment_layer_index = automation_environment_index + 1
    companion_mode_index = commitment_layer_index + 1
    completion_state_index = companion_mode_index + 1
    reset_preparation_state = {"callback": lambda: None}
    execution_control = {
        "stop_manager": None,
        "companion_state": None,
    }

    def return_home_cleanly() -> None:
        reset_preparation_state["callback"]()
        stacked_screens.setCurrentIndex(0)

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
                open_profiles=(
                    lambda: stacked_screens.setCurrentIndex(1)
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
        return_home=return_home_cleanly,
    )

    def open_completion_from_execution(
        state_id: str,
        companion_state: dict[str, str],
        execution_message: str,
    ) -> None:
        execution_control["stop_manager"] = None
        execution_control["companion_state"] = None
        completion_state = dict(companion_state)
        completion_state["execution_active"] = "false"
        completion_state["execution_message"] = execution_message
        update_completion_state(state_id, completion_state)
        stacked_screens.setCurrentIndex(completion_state_index)

    def begin_supervised_operation(companion_state: dict[str, str]) -> None:
        running_state = dict(companion_state)
        automation_id = companion_state.get("automation_id")
        real_execution_supported = _is_desktop_execution_supported(automation_id)
        running_state["status"] = "Running" if real_execution_supported else "Unavailable"
        running_state["execution_active"] = "true" if real_execution_supported else "false"
        running_state["progress"] = (
            _desktop_running_progress_label(running_state)
            if real_execution_supported
            else "Desktop execution is not available for this automation"
        )
        running_state["focus"] = (
            "FH6 focus confirmed"
            if real_execution_supported
            else "Focus handoff unavailable"
        )
        running_state["stop"] = (
            _desktop_stop_guidance(automation_id)
            if real_execution_supported
            else "No desktop real input is active."
        )
        running_state["summary"] = (
            f"{running_state.get('automation_name', 'Selected automation')} guarded operation is active. Keep FH6 supervised."
            if real_execution_supported
            else "No automation keys are being sent."
        )
        update_companion_mode(running_state)
        stacked_screens.setCurrentIndex(companion_mode_index)

        if not real_execution_supported:
            return

        from core.stop import StopManager

        stop_manager = StopManager()
        execution_control["companion_state"] = running_state
        if automation_id == "auto1":
            execution_control["stop_manager"] = stop_manager
            _start_auto1_ui_execution(
                companion_state=running_state,
                parent=body,
                timer_type=QTimer,
                on_result=open_completion_from_execution,
                stop_manager=stop_manager,
            )
        elif automation_id == "auto2":
            execution_control["stop_manager"] = None
            _start_auto2_ui_execution(
                companion_state=running_state,
                parent=body,
                timer_type=QTimer,
                on_result=open_completion_from_execution,
            )
        elif automation_id == "auto3":
            execution_control["stop_manager"] = None
            _start_auto3_ui_execution(
                companion_state=running_state,
                parent=body,
                timer_type=QTimer,
                on_result=open_completion_from_execution,
            )

    def request_stop_from_ui() -> str:
        stop_manager = execution_control["stop_manager"]
        companion_state = execution_control["companion_state"]
        if stop_manager is None or companion_state is None:
            return "Use F8 emergency stop for this guarded run. The desktop stop bridge is only available for Auto1."

        return _request_auto1_ui_stop(stop_manager, companion_state)

    companion_mode_widget, update_companion_mode = _build_companion_mode_widget(
        shell_spec=shell_spec,
        return_to_preparation=lambda: stacked_screens.setCurrentIndex(
            automation_environment_index
        ),
        request_stop=request_stop_from_ui,
    )
    commitment_layer_widget, update_commitment_layer = _build_commitment_layer_widget(
        shell_spec=shell_spec,
        timer_type=QTimer,
        return_to_preparation=lambda: stacked_screens.setCurrentIndex(
            automation_environment_index
        ),
        open_refusal_state=(
            lambda companion_state, message: open_completion_from_execution(
                "refused",
                companion_state,
                message,
            )
        ),
        open_companion_mode=begin_supervised_operation,
    )
    automation_environment_widget, reset_automation_environment = (
        _build_automation_environment_widget(
            shell_spec.automation_environment,
            shell_spec=shell_spec,
            open_commitment_layer=(
                lambda companion_state: (
                    update_commitment_layer(companion_state),
                    stacked_screens.setCurrentIndex(commitment_layer_index),
                )
            ),
        )
    )
    reset_preparation_state["callback"] = reset_automation_environment
    stacked_screens.addWidget(automation_environment_widget)
    stacked_screens.addWidget(commitment_layer_widget)
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

    body_layout.addWidget(collapsed_rail)
    body_layout.addWidget(main_area)
    root_layout.addWidget(body)

    body.resizeEvent = lambda _event: overlay_navigation.setGeometry(
        QRect(0, 0, overlay_navigation.width(), body.height())
    )

    window.setCentralWidget(root)
    window._fh6_tray_icon = _install_system_tray(app, window, app_icon)
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
        session_id_provider=lambda: "desktop-preview-session",
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
        primary_intention="",
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
            summary="Baseline requirements before operation.",
            details=(section.expected_baseline, section.manual_positioning_assumption),
            zone_role=ZoneRole.PRIMARY,
            readability_treatment="primary confidence check",
        )

    if isinstance(section, ContextualWarningsSection):
        return PrototypeAutomationEnvironmentSection(
            section_id=section.section_id,
            title="Contextual Warnings",
            summary="Warnings remain contextual and secondary.",
            details=section.warnings or ("No contextual warnings for this section.",),
            zone_role=ZoneRole.SECONDARY,
            readability_treatment="secondary contextual support",
        )

    if isinstance(section, AdvancedSection):
        return PrototypeAutomationEnvironmentSection(
            section_id=section.section_id,
            title="Advanced / Refinement",
            summary=section.purpose,
            details=section.available_refinements or ("Advanced refinements remain secondary.",),
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
                summary="Ready for supervised operation",
                zone_role=ZoneRole.TERTIARY,
            ),
        ),
    )


def _build_prototype_sidebar_composition() -> PrototypeSidebarComposition:
    return PrototypeSidebarComposition(
        navigation_block_label=DESKTOP_PRODUCT_NAME,
        footer_status="",
        footer_detail="",
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
        title=DESKTOP_PRODUCT_NAME,
        height=63,
        treatment="restrained product identity bar",
        reserves_identity_space=True,
    )


def _build_prototype_commitment_layer() -> PrototypeCommitmentLayer:
    return PrototypeCommitmentLayer(
        title="Commit to Supervision",
        primary_intention="Confirm readiness before supervised operation begins.",
        readiness_label="You are about to begin supervised operation.",
        focus_label="FH6 focus handoff ready",
        profile_label="Safe default profile loaded",
        stop_label="Emergency stop available (F8)",
        focus_method_labels=("Automatic Focus", "Manual Focus"),
        countdown_values=(3, 2, 1),
        focus_methods_share_countdown=True,
        is_last_safe_exit=True,
        introduces_execution=False,
    )


def _build_prototype_execution_wiring() -> PrototypeExecutionWiring:
    return PrototypeExecutionWiring(
        enabled_automation_ids=("auto1", "auto2", "auto3"),
        refused_automation_ids=("auto4",),
        uses_existing_guarded_paths=True,
        preserves_f8_stop=True,
        fail_closed_for_unsupported_automations=True,
    )


def _build_prototype_workflow_contract() -> PrototypeWorkflowContract:
    return PrototypeWorkflowContract(
        transitions=(
            ("home", "automation_environment"),
            ("automation_environment", "commitment"),
            ("commitment", "countdown"),
            ("countdown", "companion_mode"),
            ("companion_mode", "completion"),
            ("completion", "automation_environment"),
            ("completion", "home"),
        ),
        dead_button_policy="visible controls navigate, prepare, start guarded execution, or refuse with reason",
        unsupported_execution_policy="Auto4 is inactive; Auto1, Auto2, and Auto3 use bounded guarded desktop paths",
        state_reset_policy="returning home clears prepared desktop run state",
        real_input_boundary="Auto1, Auto2, and Auto3 start only after preparation, focus handoff, and commitment",
        stop_policy="F8 is available for guarded real-input runs; UI Request Stop is available where a shared StopManager exists",
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


def _start_auto1_ui_execution(
    companion_state: dict[str, str],
    parent,
    timer_type,
    on_result,
    stop_manager,
) -> None:
    start_auto1_ui_execution(
        companion_state=companion_state,
        parent=parent,
        timer_type=timer_type,
        on_result=on_result,
        stop_manager=stop_manager,
    )


def _start_auto2_ui_execution(
    companion_state: dict[str, str],
    parent,
    timer_type,
    on_result,
) -> None:
    start_auto2_ui_execution(
        companion_state=companion_state,
        parent=parent,
        timer_type=timer_type,
        on_result=on_result,
    )


def _start_auto3_ui_execution(
    companion_state: dict[str, str],
    parent,
    timer_type,
    on_result,
) -> None:
    start_auto3_ui_execution(
        companion_state=companion_state,
        parent=parent,
        timer_type=timer_type,
        on_result=on_result,
    )


def _attempt_ui_focus_handoff(companion_state: dict[str, str]):
    return attempt_ui_focus_handoff(companion_state)


def _format_ui_focus_failure_message(focus_result, automation_name: str = "operation") -> str:
    return format_ui_focus_failure_message(focus_result, automation_name)


def _build_auto1_ui_execution_profile(companion_state: dict[str, str]) -> dict:
    return build_auto1_ui_execution_profile(companion_state)


def _parse_auto1_race_duration_override(raw_value: str | None) -> float:
    return parse_auto1_race_duration_override(raw_value)


def _parse_auto1_loop_count(raw_value: str | None) -> int:
    return parse_auto1_loop_count(raw_value)


def _auto1_execution_race_duration(displayed_race_duration: float) -> float:
    return auto1_execution_race_duration(displayed_race_duration)


def _should_show_auto1_runtime_adjustment(automation_id: str) -> bool:
    return automation_id == "auto1"


def _is_desktop_execution_supported(automation_id: str) -> bool:
    return is_desktop_execution_supported(automation_id)


def _is_desktop_preparation_available(automation_id: str) -> bool:
    return is_desktop_preparation_available(automation_id)


def _desktop_execution_refusal_details(automation_id: str) -> tuple[str, ...]:
    return desktop_execution_refusal_details(automation_id)


def _desktop_execution_confirmation_summary(automation_id: str) -> str:
    return desktop_execution_confirmation_summary(automation_id)


def _format_auto1_race_duration_for_display(raw_value: str | None) -> str:
    return f"{_parse_auto1_race_duration_override(raw_value):.1f} seconds"


def _format_auto1_loop_count_for_display(raw_value: str | None) -> str:
    loop_count = _parse_auto1_loop_count(raw_value)
    return f"{loop_count} loop" if loop_count == 1 else f"{loop_count} loops"


def _build_commitment_readiness_details(companion_state: dict[str, str]) -> tuple[str, ...]:
    automation_id = companion_state.get("automation_id")
    if automation_id == "auto1":
        return (
            "Auto1 selected for supervised real-input operation.",
            f"Race drive duration: {_format_auto1_race_duration_for_display(companion_state.get('race_duration_seconds'))}.",
            f"Requested loops: {_format_auto1_loop_count_for_display(companion_state.get('requested_cycles'))}.",
            "Expected baseline: FH6 focused at the validated Auto1 race restart state.",
            "F8 emergency stop available.",
        )

    if automation_id == "auto2":
        purchase_count = _parse_auto2_purchase_count(
            companion_state.get("auto2_purchase_count")
        )
        return (
            "Auto2 selected for supervised real-input operation.",
            (
                f"Mode: {_auto2_mode_label(companion_state.get('auto2_mode', 'test'))}. "
                f"Purchases: {purchase_count}."
            ),
            "Expected baseline: FH6 focused at the validated Autoshow/buy-car menu state.",
            "F8 emergency stop available.",
        )

    if automation_id == "auto3":
        return (
            "Auto3 selected for supervised real-input operation.",
            f"Mode: {_auto3_mode_label(companion_state.get('auto3_mode', 'test'))}. Cars: {_parse_auto3_car_count(companion_state.get('auto3_cars'))}.",
            "Expected baseline: start row A with validated A1 -> B1 -> C1 -> A2 traversal.",
            "F8 emergency stop available.",
        )

    return (
        f"{companion_state.get('automation_name', 'Selected automation')} is not available for desktop execution.",
        "No automation keys will be sent.",
    )


def _load_auto1_default_race_duration() -> float:
    return load_auto1_default_race_duration()


def _completion_state_id_for_status(status: str) -> str:
    return completion_state_id_for_status(status)


def _completion_state_id_for_auto1_status(status: str) -> str:
    return completion_state_id_for_auto1_status(status)


def _summarize_auto1_ui_execution_error(error: Exception) -> str:
    return summarize_auto1_ui_execution_error(error)


def _summarize_ui_execution_error(automation_label: str, error: Exception) -> str:
    return summarize_ui_execution_error(automation_label, error)


def _is_real_auto1_execution_state(companion_state: dict[str, str]) -> bool:
    return (
        companion_state.get("automation_id") == "auto1"
        and companion_state.get("execution_active") == "true"
    )


def _request_auto1_ui_stop(stop_manager, companion_state: dict[str, str]) -> str:
    if not _is_real_auto1_execution_state(companion_state):
        return "No active Auto1 desktop run is available to stop."

    stop_manager.request_stop()
    return "Stop requested. Held keys will be released through the guarded Auto1 cleanup path."


def _build_top_bar_widget(shell_spec: PrototypeShellSpec, label_type):
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

    top_bar = QWidget()
    top_bar.setFixedHeight(shell_spec.top_bar.height)
    top_bar.setStyleSheet(
        f"background-color: {COLOR_SURFACE_TOPBAR}; "
        f"border-bottom: 1px solid {COLOR_BORDER_SUBTLE};"
    )
    layout = QHBoxLayout(top_bar)
    layout.setContentsMargins(14, 0, 18, 0)
    layout.setSpacing(6)

    layout.addWidget(_build_branding_logo_widget(label_type))
    layout.addStretch()
    version_label = QLabel(DESKTOP_APP_VERSION)
    version_label.setObjectName("DesktopVersionLabel")
    version_label.setToolTip(DESKTOP_APP_BUILD_TYPE)
    version_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    version_label.setStyleSheet(
        f"font-size: 11px; font-weight: 500; color: {COLOR_TEXT_MUTED}; "
        "background: transparent; border: none;"
    )
    layout.addWidget(version_label)

    return top_bar


def _build_branding_logo_widget(label_type):
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QImage, QPixmap
    from PySide6.QtWidgets import QLabel

    image = QImage(str(DESKTOP_BRAND_LOGO_PATH))
    if not image.isNull():
        bounds = _visible_image_bounds(image)
        if bounds is not None:
            image = image.copy(bounds)

        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(
            DESKTOP_BRAND_LOGO_MAX_WIDTH,
            DESKTOP_BRAND_LOGO_MAX_HEIGHT,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        logo_label = QLabel()
        logo_label.setObjectName("DesktopBrandLogo")
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setFixedSize(scaled_pixmap.size())
        logo_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        logo_label.setStyleSheet("background: transparent; border: none;")
        return logo_label

    fallback_label = label_type(DESKTOP_PRODUCT_NAME)
    fallback_label.setObjectName("DesktopBrandFallback")
    fallback_label.setStyleSheet(
        f"font-size: 14px; font-weight: 700; color: {COLOR_TEXT_PRIMARY}; "
        "background: transparent; border: none;"
    )
    return fallback_label


def _visible_image_bounds(image):
    from PySide6.QtCore import QRect

    width = image.width()
    height = image.height()
    left = width
    right = -1
    top = height
    bottom = -1

    for y in range(height):
        for x in range(width):
            if image.pixelColor(x, y).alpha() > 4:
                left = min(left, x)
                right = max(right, x)
                top = min(top, y)
                bottom = max(bottom, y)

    if right < left or bottom < top:
        return None

    return QRect(left, top, right - left + 1, bottom - top + 1)


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
    layout.setContentsMargins(0, 0, 0 if collapsed else 12, 0)
    layout.setSpacing(8)

    icon_label = QLabel(_navigation_icon_for_screen(screen.screen_id))
    icon_label.setFixedWidth(NAVIGATION_ICON_SLOT_WIDTH)
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
    open_profiles=None,
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
            open_profiles=open_profiles,
        )
        layout.addStretch()
        return container

    if screen.screen_id == ScreenId.PROFILES:
        _build_profiles_screen_content(layout, shell_spec=shell_spec)
        layout.addStretch()
        return container

    if screen.screen_id == ScreenId.HISTORY:
        _build_history_screen_content(layout, shell_spec=shell_spec)
        layout.addStretch()
        return container

    if screen.screen_id == ScreenId.HELP:
        _build_help_screen_content(layout, shell_spec=shell_spec)
        layout.addStretch()
        return container

    if screen.screen_id == ScreenId.SETTINGS:
        _build_settings_screen_content(layout, shell_spec=shell_spec)
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


def _has_specialized_desktop_screen_content(screen_id: ScreenId) -> bool:
    return screen_id in {
        ScreenId.HOME,
        ScreenId.PROFILES,
        ScreenId.HISTORY,
        ScreenId.HELP,
        ScreenId.SETTINGS,
    }


def _build_automation_environment_widget(
    automation_environment: PrototypeAutomationEnvironment,
    shell_spec: PrototypeShellSpec,
    open_commitment_layer,
):
    from PySide6.QtWidgets import (
        QComboBox,
        QDoubleSpinBox,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QSizePolicy,
        QSpinBox,
        QVBoxLayout,
        QWidget,
    )

    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(shell_spec.vertical_rhythm.header_spacing)
    title_label = QLabel(automation_environment.title)
    _style_screen_title(title_label, shell_spec=shell_spec)
    layout.addWidget(title_label)
    layout.addSpacing(2)

    controller = FrontendAutomationController(
        session_id_provider=lambda: "desktop-prepared-session",
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
    runtime = _build_preparation_text_card(
        eyebrow="QUICK SETTINGS",
        shell_spec=shell_spec,
        treatment="secondary contextual support",
    )
    runtime["layout"].setContentsMargins(12, 7, 12, 7)
    runtime["layout"].setSpacing(3)
    auto1_settings_widget = QWidget()
    auto1_settings_widget.setStyleSheet("background: transparent; border: none;")
    auto1_settings_row = QHBoxLayout(auto1_settings_widget)
    auto1_settings_row.setContentsMargins(0, 0, 0, 0)
    auto1_settings_row.setSpacing(8)
    auto2_settings_widget = QWidget()
    auto2_settings_widget.setStyleSheet("background: transparent; border: none;")
    auto2_settings_row = QHBoxLayout(auto2_settings_widget)
    auto2_settings_row.setContentsMargins(0, 0, 0, 0)
    auto2_settings_row.setSpacing(8)
    auto3_settings_widget = QWidget()
    auto3_settings_widget.setStyleSheet("background: transparent; border: none;")
    auto3_settings_row = QHBoxLayout(auto3_settings_widget)
    auto3_settings_row.setContentsMargins(0, 0, 0, 0)
    auto3_settings_row.setSpacing(8)
    race_duration_input = QDoubleSpinBox()
    race_duration_input.setRange(
        AUTO1_RACE_DURATION_MIN_SECONDS,
        AUTO1_RACE_DURATION_MAX_SECONDS,
    )
    race_duration_input.setDecimals(1)
    race_duration_input.setSingleStep(1.0)
    race_duration_input.setSuffix(" sec")
    race_duration_input.setMaximumWidth(16777215)
    race_duration_input.setFixedHeight(32)
    race_duration_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    _style_runtime_spinbox(race_duration_input, shell_spec=shell_spec)
    race_duration_input.setValue(_load_auto1_default_race_duration())
    race_duration_column = QWidget()
    race_duration_column.setStyleSheet("background: transparent; border: none;")
    race_duration_column_layout = QVBoxLayout(race_duration_column)
    race_duration_column_layout.setContentsMargins(0, 0, 0, 0)
    race_duration_column_layout.setSpacing(4)
    race_duration_hint = QLabel(
        "Use the race completion time shown on the Auto1 Restart screen."
    )
    _style_detail_label(race_duration_hint, shell_spec=shell_spec)
    race_duration_hint.setWordWrap(False)
    race_duration_column_layout.addWidget(race_duration_input)
    race_duration_column_layout.addWidget(race_duration_hint)
    auto1_settings_row.addWidget(race_duration_column, 1)
    auto1_loop_count_input = QSpinBox()
    auto1_loop_count_input.setRange(AUTO1_LOOP_COUNT_MIN, AUTO1_LOOP_COUNT_MAX)
    auto1_loop_count_input.setSingleStep(1)
    auto1_loop_count_input.setSuffix(" loops")
    auto1_loop_count_input.setMaximumWidth(16777215)
    auto1_loop_count_input.setFixedHeight(32)
    auto1_loop_count_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    _style_runtime_spinbox(auto1_loop_count_input, shell_spec=shell_spec)
    loop_count_column = QWidget()
    loop_count_column.setStyleSheet("background: transparent; border: none;")
    loop_count_column_layout = QVBoxLayout(loop_count_column)
    loop_count_column_layout.setContentsMargins(0, 0, 0, 0)
    loop_count_column_layout.setSpacing(4)
    loop_count_column_layout.addWidget(auto1_loop_count_input)
    loop_count_column_layout.addSpacing(race_duration_hint.sizeHint().height())
    auto1_settings_row.addWidget(loop_count_column, 1)
    auto2_mode_input = QComboBox()
    auto2_mode_input.addItem("Test navigation", "test")
    auto2_mode_input.addItem("Purchase cars", "purchase")
    auto2_mode_input.setMaximumWidth(16777215)
    auto2_mode_input.setFixedHeight(32)
    auto2_mode_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    _style_runtime_combobox(auto2_mode_input, shell_spec=shell_spec)
    auto2_settings_row.addWidget(auto2_mode_input, 1)
    auto2_purchase_count_input = QSpinBox()
    auto2_purchase_count_input.setRange(1, 25)
    auto2_purchase_count_input.setSingleStep(1)
    auto2_purchase_count_input.setSuffix(" cars")
    auto2_purchase_count_input.setMaximumWidth(16777215)
    auto2_purchase_count_input.setFixedHeight(32)
    auto2_purchase_count_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    _style_runtime_spinbox(auto2_purchase_count_input, shell_spec=shell_spec)
    auto2_settings_row.addWidget(auto2_purchase_count_input, 1)
    auto3_mode_input = QComboBox()
    auto3_mode_input.addItem("Test traversal", "test")
    auto3_mode_input.addItem("Unlock skill trees", "unlock")
    auto3_mode_input.setMaximumWidth(16777215)
    auto3_mode_input.setFixedHeight(32)
    auto3_mode_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    _style_runtime_combobox(auto3_mode_input, shell_spec=shell_spec)
    auto3_settings_row.addWidget(auto3_mode_input, 1)
    auto3_cars_input = QSpinBox()
    auto3_cars_input.setRange(1, 4)
    auto3_cars_input.setSingleStep(1)
    auto3_cars_input.setSuffix(" cars")
    auto3_cars_input.setMaximumWidth(16777215)
    auto3_cars_input.setFixedHeight(32)
    auto3_cars_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    _style_runtime_spinbox(auto3_cars_input, shell_spec=shell_spec)
    auto3_settings_row.addWidget(auto3_cars_input, 1)
    runtime["layout"].addWidget(auto1_settings_widget)
    runtime["layout"].addWidget(auto2_settings_widget)
    runtime["layout"].addWidget(auto3_settings_widget)
    run = _build_preparation_text_card(
        eyebrow="RUN PREPARATION",
        shell_spec=shell_spec,
        treatment="primary action",
    )

    layout.addWidget(overview["card"])
    layout.addSpacing(3)
    layout.addLayout(
        _build_card_row(
            cards=(profile["card"], warnings["card"]),
            shell_spec=shell_spec,
        )
    )
    layout.addSpacing(3)
    layout.addWidget(readiness["card"])
    layout.addSpacing(3)
    layout.addWidget(runtime["card"])
    layout.addSpacing(3)

    prepare_button = QPushButton("Prepare Run")
    _style_primary_button(prepare_button, shell_spec=shell_spec)
    run["layout"].addWidget(prepare_button)
    companion_button = QPushButton("Move to Supervision")
    companion_button.setEnabled(False)
    _style_secondary_button(companion_button, shell_spec=shell_spec)
    run["layout"].addWidget(companion_button)
    layout.addWidget(run["card"])

    preparation_cards = {
        "overview": overview,
        "profile": profile,
        "readiness": readiness,
        "warnings": warnings,
        "runtime": runtime,
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
        requested_count = _desktop_requested_count(
            automation_id,
            auto1_loop_count_input.value(),
            auto2_purchase_count_input.value(),
            auto3_cars_input.value(),
        )
        plan = controller.prepare_run_plan(
            AutomationRunRequest(
                automation_id=automation_id,
                profile_id=profile_id,
                requested_count=requested_count,
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
        desktop_execution_supported = _is_desktop_execution_supported(automation_id)
        desktop_preparation_available = _is_desktop_preparation_available(automation_id)
        runtime["card"].setVisible(automation_id in {"auto1", "auto2", "auto3"})
        auto1_settings_widget.setVisible(automation_id == "auto1")
        auto2_settings_widget.setVisible(automation_id == "auto2")
        auto3_settings_widget.setVisible(automation_id == "auto3")
        race_duration_input.setEnabled(automation_id == "auto1")
        auto1_loop_count_input.setEnabled(automation_id == "auto1")
        auto2_mode_input.setEnabled(automation_id == "auto2")
        auto2_purchase_count_input.setEnabled(
            automation_id == "auto2"
            and auto2_mode_input.currentData() == "purchase"
        )
        auto3_mode_input.setEnabled(automation_id == "auto3")
        auto3_cars_input.setEnabled(automation_id == "auto3")
        companion_button.setText(
            "Move to Supervision"
            if desktop_preparation_available
            else "Desktop Unavailable"
        )
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
            title="Required Starting Position",
            summary=_desktop_baseline_summary(automation_id),
            details=_desktop_baseline_details(automation_id, readiness_model),
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
        if automation_id == "auto1":
            _set_preparation_card_text(
                preparation_cards["runtime"],
                title="Auto1 runtime",
                summary=(
                    f"{race_duration_input.value():.1f}s drive duration. "
                    f"{auto1_loop_count_input.value()} loop(s)."
                ),
                details=(
                    "Race drive duration range: "
                    f"{AUTO1_RACE_DURATION_MIN_SECONDS:.0f}-"
                    f"{AUTO1_RACE_DURATION_MAX_SECONDS:.0f} seconds. "
                    f"Loop range: {AUTO1_LOOP_COUNT_MIN}-{AUTO1_LOOP_COUNT_MAX}.",
                ),
            )
        elif automation_id == "auto2":
            _set_preparation_card_text(
                preparation_cards["runtime"],
                title="Auto2 mode",
                summary=_auto2_mode_label(auto2_mode_input.currentData()),
                details=(
                    (
                        f"Purchases requested: {auto2_purchase_count_input.value()}."
                        if auto2_mode_input.currentData() == "purchase"
                        else "Test navigation does not purchase."
                    ),
                ),
            )
        elif automation_id == "auto3":
            _set_preparation_card_text(
                preparation_cards["runtime"],
                title="Auto3 mode and cars",
                summary=(
                    f"{_auto3_mode_label(auto3_mode_input.currentData())}. "
                    f"Cars: {auto3_cars_input.value()}."
                ),
                details=(
                    "Validated A-start boundary. Current hard max: 4 cars.",
                ),
            )
        _set_preparation_card_text(
            preparation_cards["run"],
            title=(
                (
                    "Prepared for supervised operation"
                    if desktop_preparation_available
                    else "Desktop preparation unavailable"
                )
                if prepared
                else (
                    "Prepare the run plan"
                    if desktop_preparation_available
                    else "Review guarded manual boundary"
                )
            ),
            summary=(
                (
                    (
                        "Ready for focus handoff. No execution has started."
                        if desktop_execution_supported
                        else "Ready for preparation review. No execution has started."
                    )
                    if desktop_execution_supported
                    else "Ready for preparation review. No execution has started."
                )
                if prepared
                else _desktop_execution_confirmation_summary(automation_id)
            ),
            details=(
                (
                    f"Selected: {definition.display_name}. "
                    f"Requested cycles: {_desktop_requested_count(automation_id, auto1_loop_count_input.value(), auto2_purchase_count_input.value(), auto3_cars_input.value())}."
                ),
                (
                    (
                        "Prepared state only. Supervision is available after commitment."
                        if desktop_preparation_available
                        else " ".join(_desktop_execution_refusal_details(automation_id))
                    )
                    if prepared
                    else (
                        "No operation begins until focus handoff and commitment."
                        if desktop_preparation_available
                        else " ".join(_desktop_execution_refusal_details(automation_id))
                    )
                ),
            ),
        )
        if prepared and desktop_preparation_available:
            selected_companion_state["value"] = {
                "automation_id": definition.automation_id,
                "automation_name": definition.display_name,
                "profile_id": profile_metadata.profile_id,
                "profile_name": profile_metadata.profile_name,
                "requested_cycles": str(auto1_loop_count_input.value()),
                "race_duration_seconds": f"{race_duration_input.value():.1f}",
                "auto2_mode": str(auto2_mode_input.currentData()),
                "auto2_purchase_count": str(auto2_purchase_count_input.value()),
                "auto3_mode": str(auto3_mode_input.currentData()),
                "auto3_cars": str(auto3_cars_input.value()),
                "status": "Prepared",
                "progress": (
                    "Waiting for focus handoff and commitment"
                    if desktop_execution_supported
                    else "Waiting for preparation review"
                ),
                "focus": (
                    "FH6 focus handoff ready"
                    if desktop_execution_supported
                    else "Focus handoff unavailable"
                ),
                "stop": "F8 emergency stop available",
                "summary": (
                    "Prepared state. No automation is executing."
                    if desktop_execution_supported
                    else "Prepared state. Desktop execution is unavailable for this automation."
                ),
                "execution_active": "false",
            }
            companion_button.setEnabled(True)
        elif prepared:
            selected_companion_state["value"] = None
            companion_button.setEnabled(False)

    def select_automation(automation_id: str) -> None:
        render_preparation_state(automation_id, prepared=False)

    def reset_preparation_state() -> None:
        render_preparation_state(active_automations[0].automation_id, prepared=False)

    for automation_id, button in selector_buttons.items():
        button.clicked.connect(
            lambda _checked=False, selected_id=automation_id: select_automation(selected_id)
        )

    def rerender_if_selected(automation_id: str) -> None:
        if selected_automation_id["value"] == automation_id:
            render_preparation_state(automation_id, prepared=False)

    race_duration_input.valueChanged.connect(
        lambda _value: rerender_if_selected("auto1")
    )
    auto1_loop_count_input.valueChanged.connect(
        lambda _value: rerender_if_selected("auto1")
    )
    auto2_mode_input.currentIndexChanged.connect(
        lambda _index: rerender_if_selected("auto2")
    )
    auto2_purchase_count_input.valueChanged.connect(
        lambda _value: rerender_if_selected("auto2")
    )
    auto3_mode_input.currentIndexChanged.connect(
        lambda _index: rerender_if_selected("auto3")
    )
    auto3_cars_input.valueChanged.connect(
        lambda _value: rerender_if_selected("auto3")
    )
    prepare_button.clicked.connect(
        lambda: render_preparation_state(selected_automation_id["value"], prepared=True)
    )
    companion_button.clicked.connect(
        lambda: open_commitment_layer(selected_companion_state["value"])
        if selected_companion_state["value"] is not None
        else None
    )
    render_preparation_state(selected_automation_id["value"], prepared=False)

    layout.addStretch()
    return container, reset_preparation_state


def _build_commitment_layer_widget(
    shell_spec: PrototypeShellSpec,
    timer_type,
    return_to_preparation,
    open_refusal_state,
    open_companion_mode,
):
    from PySide6.QtWidgets import (
        QHBoxLayout,
        QLabel,
        QPushButton,
        QVBoxLayout,
        QWidget,
    )

    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(10)

    title_label = QLabel(shell_spec.commitment_layer.title)
    subtitle_label = QLabel(shell_spec.commitment_layer.primary_intention)
    _style_screen_title(title_label, shell_spec=shell_spec)
    _style_summary_label(subtitle_label, shell_spec=shell_spec)
    layout.addWidget(title_label)
    layout.addWidget(subtitle_label)
    layout.addSpacing(8)

    readiness_card = _build_preparation_text_card(
        eyebrow="LAST SAFE CHECKPOINT",
        shell_spec=shell_spec,
        treatment="primary action",
    )
    focus_card = _build_preparation_text_card(
        eyebrow="FOCUS HANDOFF",
        shell_spec=shell_spec,
        treatment="primary confidence check",
    )
    profile_card = _build_preparation_text_card(
        eyebrow="PROFILE",
        shell_spec=shell_spec,
        treatment="secondary contextual support",
    )
    countdown_card = _build_preparation_text_card(
        eyebrow="COMMITMENT COUNTDOWN",
        shell_spec=shell_spec,
        treatment="commitment",
    )

    layout.addWidget(readiness_card["card"])
    layout.addSpacing(6)
    layout.addLayout(
        _build_card_row(
            cards=(focus_card["card"], profile_card["card"]),
            shell_spec=shell_spec,
        )
    )
    layout.addSpacing(6)
    layout.addWidget(countdown_card["card"])
    layout.addSpacing(8)

    action_row = QHBoxLayout()
    action_row.setContentsMargins(0, 0, 0, 0)
    action_row.setSpacing(shell_spec.vertical_rhythm.group_spacing)
    automatic_focus_button = QPushButton("Automatic Focus")
    manual_focus_button = QPushButton("Manual Focus")
    return_button = QPushButton("Return to Preparation")
    _style_primary_button(automatic_focus_button, shell_spec=shell_spec)
    _style_secondary_button(manual_focus_button, shell_spec=shell_spec)
    _style_secondary_button(return_button, shell_spec=shell_spec)
    action_row.addWidget(automatic_focus_button)
    action_row.addWidget(manual_focus_button)
    action_row.addWidget(return_button)
    layout.addLayout(action_row)
    layout.addStretch()

    countdown_timer = timer_type(container)
    countdown_timer.setInterval(900)
    current_companion_state = {"value": None}
    countdown_position = {"value": 0}

    def set_waiting_state(companion_state: dict[str, str]) -> None:
        current_companion_state["value"] = companion_state
        real_execution_supported = _is_desktop_execution_supported(
            companion_state.get("automation_id", "")
        )
        countdown_timer.stop()
        countdown_position["value"] = 0
        automatic_focus_button.setEnabled(True)
        manual_focus_button.setEnabled(True)
        _set_preparation_card_text(
            readiness_card,
            title=shell_spec.commitment_layer.readiness_label,
            summary=companion_state.get("automation_name", "Prepared operation"),
            details=_build_commitment_readiness_details(companion_state),
        )
        _set_preparation_card_text(
            focus_card,
            title=(
                shell_spec.commitment_layer.focus_label
                if real_execution_supported
                else "No desktop real-input handoff"
            ),
            summary=(
                f"Target window: {DEFAULT_FH6_TARGET_TITLE}"
                if real_execution_supported
                else "This prepared supervision state will not send automation keys."
            ),
            details=(
                (
                    "Automatic Focus asks the app to bring FH6 forward before countdown."
                    if real_execution_supported
                    else "Desktop execution is unavailable for this automation."
                ),
                (
                    "Manual Focus starts the same countdown so you can switch to FH6 before zero."
                    if real_execution_supported
                    else "Return to preparation and choose Auto1, Auto2, or Auto3."
                ),
            ),
        )
        _set_preparation_card_text(
            profile_card,
            title=companion_state.get("profile_name", "Selected profile"),
            summary=shell_spec.commitment_layer.profile_label,
            details=(
                shell_spec.commitment_layer.stop_label,
                (
                    "Keep the validated FH6 baseline visible before continuing."
                    if real_execution_supported
                    else "This desktop path is unavailable for the selected automation."
                ),
            ),
        )
        _set_preparation_card_text(
            countdown_card,
            title="Choose a focus method",
            summary="Supervised operation begins after the shared countdown.",
            details=("Choose Automatic Focus, Manual Focus, or return to preparation.",),
        )

    def start_countdown(focus_method: str) -> None:
        automatic_focus_button.setEnabled(False)
        manual_focus_button.setEnabled(False)
        countdown_position["value"] = 0
        if focus_method == "manual":
            _set_preparation_card_text(
                focus_card,
                title="Manual Focus selected",
                summary="Switch to the FH6 game window during the countdown.",
                details=(
                    "Automation will begin automatically when the timer reaches zero.",
                    "Keep F8 available.",
                ),
            )
            _set_preparation_card_text(
                countdown_card,
                title="Manual Focus",
                summary="Countdown begins now.",
                details=("Switch to FH6 before the timer reaches zero.",),
            )
        else:
            _set_preparation_card_text(
                focus_card,
                title="Automatic Focus selected",
                summary="FH6 focus handoff was confirmed.",
                details=(
                    "Automation will begin automatically when the timer reaches zero.",
                    "Keep F8 available.",
                ),
            )
            _set_preparation_card_text(
                countdown_card,
                title="Automatic Focus",
                summary="Countdown begins now.",
                details=("FH6 focus is confirmed before the timer reaches zero.",),
            )
        advance_countdown()
        countdown_timer.start()

    def advance_countdown() -> None:
        values = shell_spec.commitment_layer.countdown_values
        index = countdown_position["value"]
        if index >= len(values):
            countdown_timer.stop()
            if current_companion_state["value"] is not None:
                open_companion_mode(current_companion_state["value"])
            return

        value = values[index]
        countdown_position["value"] = index + 1
        _set_preparation_card_text(
            countdown_card,
            title=str(value),
            summary="Supervised operation begins in",
            details=(
                (
                    "The selected operation begins after this commitment countdown."
                    if current_companion_state["value"] is not None
                    else "Supervision opens after this countdown."
                ),
            ),
        )

    def begin_automatic_focus_countdown() -> None:
        if current_companion_state["value"] is None:
            return

        if not _is_desktop_execution_supported(
            current_companion_state["value"].get("automation_id", "")
        ):
            open_refusal_state(
                current_companion_state["value"],
                "Desktop execution is unavailable for the selected automation.",
            )
            return

        automatic_focus_button.setEnabled(False)
        manual_focus_button.setEnabled(False)
        _set_preparation_card_text(
            focus_card,
            title="Automatic Focus selected",
            summary="Attempting to focus FH6.",
            details=("Automation will begin automatically when the timer reaches zero.",),
        )
        focus_result = _attempt_ui_focus_handoff(current_companion_state["value"])
        if not focus_result.succeeded:
            failure_message = _format_ui_focus_failure_message(
                focus_result,
                current_companion_state["value"].get("automation_name", "operation"),
            )
            _set_preparation_card_text(
                focus_card,
                title="Focus handoff needs attention",
                summary="The selected operation has not started.",
                details=(failure_message,),
            )
            _set_preparation_card_text(
                countdown_card,
                title="Choose a focus method",
                summary="Automatic Focus did not confirm FH6.",
                details=(
                    "Retry Automatic Focus, choose Manual Focus and switch during countdown, or return to preparation.",
                ),
            )
            automatic_focus_button.setEnabled(True)
            manual_focus_button.setEnabled(True)
            return

        start_countdown("automatic")

    def begin_manual_focus_countdown() -> None:
        if current_companion_state["value"] is None:
            return

        if not _is_desktop_execution_supported(
            current_companion_state["value"].get("automation_id", "")
        ):
            open_refusal_state(
                current_companion_state["value"],
                "Desktop execution is unavailable for the selected automation.",
            )
            return

        start_countdown("manual")

    def return_to_preparation_from_commitment() -> None:
        countdown_timer.stop()
        countdown_position["value"] = 0
        automatic_focus_button.setEnabled(True)
        manual_focus_button.setEnabled(True)
        return_to_preparation()

    countdown_timer.timeout.connect(advance_countdown)
    automatic_focus_button.clicked.connect(begin_automatic_focus_countdown)
    manual_focus_button.clicked.connect(begin_manual_focus_countdown)
    return_button.clicked.connect(return_to_preparation_from_commitment)
    set_waiting_state(
        {
            "automation_name": "Prepared operation",
            "profile_name": "Selected profile",
        }
    )

    return container, set_waiting_state


def _build_home_screen_content(
    layout,
    home_concept: PrototypeHomeConcept,
    shell_spec: PrototypeShellSpec,
    open_automation_environment,
    open_profiles,
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
            button_text="Review Profiles",
            shell_spec=shell_spec,
            treatment="secondary action",
            primary=False,
            action_callback=open_profiles,
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


def _is_real_desktop_execution_state(companion_state: dict[str, str]) -> bool:
    return (
        _is_desktop_execution_supported(companion_state.get("automation_id", ""))
        and companion_state.get("execution_active") == "true"
    )


def _auto2_mode_label(mode: str) -> str:
    return "Purchase cars" if mode == "purchase" else "Test navigation"


def _auto3_mode_label(mode: str) -> str:
    return "Multi-car unlock" if mode == "unlock" else "Multi-car test traversal"


def _parse_auto3_car_count(raw_value: str | None) -> int:
    return parse_auto3_car_count(raw_value)


def _parse_auto2_purchase_count(raw_value: str | None) -> int:
    return parse_auto2_purchase_count(raw_value)


def _desktop_running_progress_label(companion_state: dict[str, str]) -> str:
    automation_id = companion_state.get("automation_id")
    if automation_id == "auto1":
        return (
            f"Requested loops: {_parse_auto1_loop_count(companion_state.get('requested_cycles'))} "
            "- guarded race run active"
        )

    if automation_id == "auto2":
        if companion_state.get("auto2_mode") == "purchase":
            return (
                "Purchase cars - "
                f"{_parse_auto2_purchase_count(companion_state.get('auto2_purchase_count'))} purchase(s) active"
            )
        return "Test navigation - guarded one-cycle run active"

    if automation_id == "auto3":
        return (
            f"{_auto3_mode_label(companion_state.get('auto3_mode', 'test'))} - "
            f"{_parse_auto3_car_count(companion_state.get('auto3_cars'))} car(s) active"
        )

    return "Guarded operation active"


def _desktop_stop_guidance(automation_id: str | None) -> str:
    if automation_id == "auto1":
        return "F8 emergency stop available. UI stop request available."

    if automation_id in {"auto2", "auto3"}:
        return "F8 emergency stop available."

    return "No desktop real input is active."


def _desktop_requested_count(
    automation_id: str,
    auto1_loops: int,
    auto2_purchases: int,
    auto3_cars: int,
) -> int:
    if automation_id == "auto1":
        return auto1_loops

    if automation_id == "auto2":
        return auto2_purchases

    if automation_id == "auto3":
        return auto3_cars

    return 1


def _build_profiles_screen_content(layout, shell_spec: PrototypeShellSpec) -> None:
    from PySide6.QtWidgets import (
        QFrame,
        QGridLayout,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QDoubleSpinBox,
        QSizePolicy,
        QVBoxLayout,
        QWidget,
    )

    profiles = _load_desktop_profile_settings()
    first_profile = profiles[0] if profiles else None
    selected_profile_id = {"value": first_profile["profile_id"] if first_profile else ""}
    selector_buttons: dict[str, QPushButton] = {}
    timing_editor_layout = QGridLayout()
    status_label = QLabel()
    selected_summary_label = QLabel()

    layout.addWidget(
        _build_visual_card(
            title="Profile settings",
            summary="Adjust profile timing behavior without touching automation logic.",
            details=(
                "Official profiles are locked reference defaults.",
                "Custom profiles can be tuned for slower or faster FH6 menu behavior.",
            ),
            shell_spec=shell_spec,
            treatment="hero",
        )
    )

    layout.addSpacing(6)

    profile_stage = QFrame()
    profile_stage.setObjectName("DesktopCard")
    profile_stage.setFrameShape(QFrame.Shape.NoFrame)
    profile_stage.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    _style_visual_card(profile_stage, treatment="primary")

    profile_stage_layout = QHBoxLayout(profile_stage)
    profile_stage_layout.setContentsMargins(12, 10, 12, 10)
    profile_stage_layout.setSpacing(10)

    selector_column = QWidget()
    selector_column.setStyleSheet("background: transparent; border: none;")
    selector_column.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Preferred,
    )
    selector_layout = QVBoxLayout(selector_column)
    selector_layout.setContentsMargins(0, 0, 0, 0)
    selector_layout.setSpacing(6)

    selector_title = QLabel("Available profiles")
    _style_eyebrow_label(selector_title, primary=True)
    selector_layout.addWidget(selector_title)

    detail_panel = QFrame()
    detail_panel.setObjectName("DesktopCard")
    detail_panel.setFrameShape(QFrame.Shape.NoFrame)
    detail_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    _style_visual_card(detail_panel, treatment="primary")

    detail_layout = QVBoxLayout(detail_panel)
    detail_layout.setContentsMargins(12, 10, 12, 10)
    detail_layout.setSpacing(7)

    selected_eyebrow = QLabel("Timing controls")
    _style_eyebrow_label(selected_eyebrow, primary=True)
    selected_title_label = QLabel()
    _style_card_title(selected_title_label, shell_spec=shell_spec, treatment="primary")
    _style_detail_label(selected_summary_label, shell_spec=shell_spec)
    _style_detail_label(status_label, shell_spec=shell_spec)

    detail_layout.addWidget(selected_eyebrow)
    detail_layout.addWidget(selected_title_label)
    detail_layout.addWidget(selected_summary_label)
    detail_layout.addLayout(timing_editor_layout)
    detail_layout.addWidget(status_label)

    def render_selected_profile(profile: dict[str, Any]) -> None:
        profile_id = str(profile["profile_id"])
        selected_profile_id["value"] = profile_id
        for profile_id, button in selector_buttons.items():
            _style_profile_selector_button(
                button,
                shell_spec=shell_spec,
                selected=profile_id == selected_profile_id["value"],
            )

        _clear_layout(timing_editor_layout)
        profile_data = profile["data"]
        selected_title_label.setText(profile_data["profile_name"])
        selected_summary_label.setText(_profile_settings_summary(profile_data))
        status_label.setText(_profile_settings_status(profile_data))

        timings = profile_data.get("timings", {})
        for index, timing_key in enumerate(timings):
            label = QLabel(_timing_display_label(timing_key))
            _style_detail_label(label, shell_spec=shell_spec)
            spinbox = QDoubleSpinBox()
            spinbox.setRange(0.0, 240.0)
            spinbox.setDecimals(1)
            spinbox.setSingleStep(0.5)
            spinbox.setValue(float(timings[timing_key]))
            spinbox.setFixedHeight(30)
            spinbox.setEnabled(not profile_data.get("is_official", False))
            spinbox.setSuffix(" sec")
            _style_runtime_spinbox(spinbox, shell_spec=shell_spec)

            row = index // 2
            column = (index % 2) * 2
            timing_editor_layout.addWidget(label, row, column)
            timing_editor_layout.addWidget(spinbox, row, column + 1)

        if not timings:
            empty_label = QLabel("No editable timing fields found for this profile.")
            _style_detail_label(empty_label, shell_spec=shell_spec)
            timing_editor_layout.addWidget(empty_label, 0, 0, 1, 4)

    for profile in profiles:
        profile_data = profile["data"]
        button = QPushButton(_profile_settings_selector_text(profile_data))
        button.setObjectName(f"ProfileSelector_{profile['profile_id']}")
        button.setMinimumHeight(58)
        button.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        button.clicked.connect(lambda _checked=False, item=profile: render_selected_profile(item))
        selector_buttons[str(profile["profile_id"])] = button
        selector_layout.addWidget(button)

    selector_layout.addStretch(1)

    profile_stage_layout.addWidget(selector_column, 9)
    profile_stage_layout.addWidget(detail_panel, 11)

    layout.addWidget(profile_stage)
    layout.addSpacing(6)
    layout.addLayout(
        _build_card_row(
            cards=(
                _build_visual_card(
                    title="What belongs here",
                    summary="Menu delay, wait timing, race duration, and recovery pacing.",
                    details=(
                        "Timing controls affect how patiently the macro waits between steps.",
                    ),
                    shell_spec=shell_spec,
                    treatment="secondary",
                ),
                _build_visual_card(
                    title="What does not belong here",
                    summary="Keys, routes, navigation counts, deletion behavior, or automation logic.",
                    details=(
                        "Those remain locked unless a future milestone explicitly opens them.",
                    ),
                    shell_spec=shell_spec,
                    treatment="tertiary",
                ),
            ),
            shell_spec=shell_spec,
        )
    )

    if first_profile is not None:
        render_selected_profile(first_profile)


def _build_history_screen_content(layout, shell_spec: PrototypeShellSpec) -> None:
    screen = build_history_screen(
        (
            OperationalHistoryEntry(
                session_id="current-desktop-session",
                automation_id="desktop",
                automation_name="Desktop UI",
                profile_id="none",
                profile_name="No persisted run profile",
                outcome=SessionStatus.PREPARED,
                summary="Desktop UI session is active. Run persistence is not connected yet.",
                timestamp=datetime.now(timezone.utc),
                requested_count=0,
                completed_count=0,
                confidence_note="History is session-oriented and will show completed supervised runs once persistence is added.",
                warnings=(),
                recovery_note=None,
                suggested_next_step="Prepare a supervised operation from Automation Environment.",
                expandable_details=(),
            ),
        )
    )
    recent = screen.recent_sessions.sessions[0]

    layout.addWidget(
        _build_visual_card(
            title="Operational memory",
            summary=screen.primary_intention,
            details=(
                "History summarizes sessions, not raw logs.",
                "Persistence is intentionally not connected in this pass.",
            ),
            shell_spec=shell_spec,
            treatment="hero",
        )
    )
    layout.addSpacing(shell_spec.vertical_rhythm.section_spacing)
    layout.addWidget(
        _build_visual_card(
            title=recent.outcome_message,
            summary=recent.summary,
            details=(
                recent.confidence_note,
                recent.suggested_next_step or "Review the current preparation state.",
            ),
            shell_spec=shell_spec,
            treatment="primary action",
        )
    )
    layout.addSpacing(shell_spec.vertical_rhythm.section_spacing)
    layout.addWidget(
        _build_visual_card(
            title="Older sessions",
            summary="No stored older sessions yet",
            details=("When persistence is added, this remains recency-first and session-oriented.",),
            shell_spec=shell_spec,
            treatment="tertiary",
        )
    )


def _build_help_screen_content(layout, shell_spec: PrototypeShellSpec) -> None:
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QPixmap
    from PySide6.QtWidgets import (
        QFrame,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QScrollArea,
        QSizePolicy,
        QVBoxLayout,
        QWidget,
    )

    screen = build_help_screen(
        automation_definitions=tuple(get_all_automation_definitions()),
        readiness_models=tuple(get_all_readiness_models()),
        profile_metadata=tuple(get_all_profile_metadata()),
    )
    guides_by_automation_id = {
        guide.automation_id: guide
        for guide in screen.contextual_guidance.guides
    }
    auto1_guide = guides_by_automation_id["auto1"]
    auto2_guide = guides_by_automation_id["auto2"]
    auto3_guide = guides_by_automation_id["auto3"]
    guide_asset_directories = (
        Path(__file__).resolve().parents[1] / "assets" / "guides",
        Path(__file__).resolve().parents[1] / "assets" / "Guides",
    )

    def build_text_label(text: str, *, role: str = "detail") -> QLabel:
        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        if role == "heading":
            label.setStyleSheet(
                f"font-size: {shell_spec.typography.summary_size}px; "
                f"font-weight: 650; color: {COLOR_TEXT_PRIMARY}; "
                "background: transparent; border: none;"
            )
        elif role == "summary":
            _style_summary_label(label, shell_spec=shell_spec)
        else:
            _style_detail_label(label, shell_spec=shell_spec)
        return label

    def build_bullet_list(items: tuple[str, ...]) -> QWidget:
        bullet_widget = QWidget()
        bullet_widget.setStyleSheet("background: transparent; border: none;")
        bullet_layout = QVBoxLayout(bullet_widget)
        bullet_layout.setContentsMargins(0, 0, 0, 0)
        bullet_layout.setSpacing(3)
        for item in items:
            bullet_layout.addWidget(build_text_label(f"- {item}"))
        return bullet_widget

    def build_numbered_list(items: tuple[str, ...]) -> QWidget:
        numbered_widget = QWidget()
        numbered_widget.setStyleSheet("background: transparent; border: none;")
        numbered_layout = QVBoxLayout(numbered_widget)
        numbered_layout.setContentsMargins(0, 0, 0, 0)
        numbered_layout.setSpacing(3)
        for index, item in enumerate(items, start=1):
            numbered_layout.addWidget(build_text_label(f"{index}. {item}"))
        return numbered_widget

    def add_section_heading(target_layout: QVBoxLayout, title: str) -> None:
        target_layout.addSpacing(4)
        target_layout.addWidget(build_text_label(title, role="heading"))

    def build_screenshot_placeholder(text: str) -> QFrame:
        placeholder = QFrame()
        placeholder.setObjectName("HelpScreenshotPlaceholder")
        placeholder.setFrameShape(QFrame.Shape.NoFrame)
        placeholder.setMinimumHeight(58)
        placeholder.setStyleSheet(
            f"""
            QFrame#HelpScreenshotPlaceholder {{
                background-color: {COLOR_SURFACE_RECESSED};
                border: 1px dashed {COLOR_BORDER_STRONG};
                border-radius: 14px;
            }}
            """
        )
        placeholder_layout = QVBoxLayout(placeholder)
        placeholder_layout.setContentsMargins(12, 10, 12, 10)
        placeholder_layout.addWidget(build_text_label(text))
        return placeholder

    def resolve_guide_image_path(filename: str) -> Path | None:
        for guide_asset_directory in guide_asset_directories:
            candidate = guide_asset_directory / filename
            if candidate.exists():
                return candidate
        return None

    def build_guide_image(
        filename: str,
        fallback_text: str,
        caption: str,
    ) -> QFrame:
        image_card = QFrame()
        image_card.setObjectName("HelpGuideImage")
        image_card.setFrameShape(QFrame.Shape.NoFrame)
        image_card.setStyleSheet(
            f"""
            QFrame#HelpGuideImage {{
                background-color: {COLOR_SURFACE_RECESSED};
                border: 1px solid {COLOR_BORDER_SUBTLE};
                border-radius: 14px;
            }}
            """
        )
        image_layout = QVBoxLayout(image_card)
        image_layout.setContentsMargins(10, 10, 10, 10)
        image_layout.setSpacing(7)

        image_path = resolve_guide_image_path(filename)
        pixmap = QPixmap(str(image_path)) if image_path is not None else QPixmap()
        if not pixmap.isNull():
            image_label = QLabel()
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setStyleSheet("background: transparent; border: none;")
            image_label.setPixmap(
                pixmap.scaled(
                    456,
                    214,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            image_layout.addWidget(image_label)
        else:
            image_layout.addWidget(build_screenshot_placeholder(fallback_text))

        caption_label = build_text_label(caption)
        caption_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_layout.addWidget(caption_label)
        return image_card

    def build_section_content(content_widgets: tuple[QWidget, ...]) -> QWidget:
        content = QWidget()
        content.setStyleSheet("background: transparent; border: none;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 10, 0, 0)
        content_layout.setSpacing(7)
        for widget in content_widgets:
            content_layout.addWidget(widget)
        return content

    def build_getting_started_content() -> QWidget:
        content = QWidget()
        content.setStyleSheet("background: transparent; border: none;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(7)
        content_layout.addWidget(build_text_label(f"{DESKTOP_PRODUCT_NAME} uses supervised automation."))
        content_layout.addWidget(
            build_bullet_list(
                (
                    "Choose Auto1, Auto2, or Auto3.",
                    "Read the readiness card before running.",
                    "Open the matching guide if the required starting position is unclear.",
                    "Verify the required starting position in FH6.",
                    "Use test mode first when available.",
                    "Keep F8 ready.",
                    "Do not run unattended.",
                )
            )
        )
        return content

    def build_auto1_content() -> QWidget:
        content = QWidget()
        content.setStyleSheet("background: transparent; border: none;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(7)
        content_layout.addWidget(build_text_label(f"Purpose: {auto1_guide.purpose}"))
        content_layout.addWidget(
            build_text_label(
                f"Required starting position: {auto1_guide.required_starting_position}"
            )
        )
        add_section_heading(content_layout, "Step-by-step")
        content_layout.addWidget(
            build_numbered_list(
                (
                    "Complete one race manually.",
                    "Stay on the Restart screen.",
                    "Confirm pressing X would restart the event.",
                    f"Return to {DESKTOP_PRODUCT_NAME} and prepare Auto1.",
                    "Choose focus method and keep F8 ready.",
                )
            )
        )
        content_layout.addWidget(
            build_guide_image(
                "auto1_starting_position.png",
                "Auto1 screenshot placeholder: post-race Restart screen.",
                (
                    "Correct Auto1 starting position. The Restart screen should already "
                    "be visible and pressing X should restart the event."
                ),
            )
        )
        add_section_heading(content_layout, "Race Drive Duration")
        content_layout.addWidget(
            build_text_label(
                "Auto1 uses this value to determine how long it should drive before preparing for the next restart."
            )
        )
        content_layout.addWidget(
            build_text_label(
                "At the required starting position, the Restart screen shows your previous race completion time. Set Race Drive Duration to match that value."
            )
        )
        content_layout.addWidget(
            build_text_label(
                "Example: previous race time 20.1 seconds -> Race Drive Duration 20 seconds."
            )
        )
        add_section_heading(content_layout, "Before pressing Run")
        content_layout.addWidget(
            build_bullet_list(
                (
                    "Restart screen visible",
                    "X restarts the event",
                    "FH6 can receive focus",
                    "F8 ready",
                )
            )
        )
        add_section_heading(content_layout, "Common mistakes")
        content_layout.addWidget(
            build_bullet_list(
                (
                    "Starting from freeroam",
                    "Starting from pause/map/garage",
                    "Starting before completing one race",
                )
            )
        )
        add_section_heading(content_layout, "Recovery")
        content_layout.addWidget(
            build_text_label(
                "Stop with F8 if needed, return to the Restart screen, then try again."
            )
        )
        return content

    def build_auto2_content() -> QWidget:
        content = QWidget()
        content.setStyleSheet("background: transparent; border: none;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(7)
        content_layout.addWidget(build_text_label(f"Purpose: {auto2_guide.purpose}"))
        content_layout.addWidget(
            build_text_label(
                f"Target vehicle: {auto2_guide.target_or_vehicle_requirement}"
            )
        )
        content_layout.addWidget(
            build_text_label(
                "Why this vehicle: It is the current validated/optimal wheelspin workflow target."
            )
        )
        content_layout.addWidget(
            build_text_label(
                f"Required starting position: {auto2_guide.required_starting_position}"
            )
        )
        add_section_heading(content_layout, "Step-by-step")
        content_layout.addWidget(
            build_numbered_list(
                (
                    "Open Autoshow.",
                    f"Prepare Auto2 in {DESKTOP_PRODUCT_NAME}.",
                    "Use test mode first if unsure.",
                    "Use purchase mode only when alignment is trusted.",
                    "Keep F8 ready.",
                )
            )
        )
        content_layout.addWidget(
            build_guide_image(
                "auto2_starting_position.png",
                "Auto2 screenshot placeholder: Autoshow validated starting position.",
                "Correct Auto2 starting position. Simply enter Autoshow, then proceed to automation start.",
            )
        )
        add_section_heading(content_layout, "Before pressing Run")
        content_layout.addWidget(
            build_bullet_list(
                (
                    "Autoshow open",
                    "Credits available if using purchase mode",
                    "Test mode used if uncertain",
                    "F8 ready",
                )
            )
        )
        add_section_heading(content_layout, "Common mistakes")
        content_layout.addWidget(
            build_bullet_list(
                (
                    "Purchase mode before test mode",
                    "Wrong manufacturer/car visible",
                    "Unexpected confirmation screen",
                )
            )
        )
        add_section_heading(content_layout, "Recovery")
        content_layout.addWidget(
            build_text_label(
                "Stop with F8 if alignment is wrong, return to Autoshow, and use test mode first."
            )
        )
        return content

    def build_auto3_content() -> QWidget:
        content = QWidget()
        content.setStyleSheet("background: transparent; border: none;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(7)
        content_layout.addWidget(build_text_label(f"Purpose: {auto3_guide.purpose}"))
        add_section_heading(content_layout, "Important vehicle rule")
        content_layout.addWidget(
            build_text_label(
                "Auto3 operates on the currently selected vehicle. It does not verify the car model."
            )
        )
        content_layout.addWidget(
            build_text_label(
                "Target vehicle: the selected vehicle should be the first newly purchased Subaru Impreza 22B-STi Version (1998)."
            )
        )
        content_layout.addWidget(
            build_text_label(
                f"Required starting position: {auto3_guide.required_starting_position}"
            )
        )
        add_section_heading(content_layout, "Step-by-step")
        content_layout.addWidget(
            build_numbered_list(
                (
                    "Open Garage.",
                    "Go to Cars -> My Cars.",
                    "Sort by Recently Added.",
                    "Make sure the correct newly purchased Subaru is selected.",
                    "Confirm start row A.",
                    f"Prepare Auto3 in {DESKTOP_PRODUCT_NAME}.",
                    "Keep F8 ready.",
                )
            )
        )
        content_layout.addWidget(
            build_guide_image(
                "auto3_starting_position.png",
                "Auto3 screenshot placeholder: My Cars sorted by Recently Added.",
                (
                    "Correct Auto3 starting position. From Garage -> Cars -> My Cars, "
                    "(not Freeroam -> Change car!). The seated car should be the most "
                    "recent Subaru Impreza 22B-STI (1998)."
                ),
            )
        )
        add_section_heading(content_layout, "Before pressing Run")
        content_layout.addWidget(
            build_bullet_list(
                (
                    "My Cars open",
                    "Recently Added sorting active",
                    "Correct Subaru selected",
                    "Start row A",
                    "Verify that the desired cars to be unlocked are placed in a continuous string.",
                    "Skill points available",
                    "F8 ready",
                )
            )
        )
        add_section_heading(content_layout, "Common mistakes")
        content_layout.addWidget(
            build_bullet_list(
                (
                    "Wrong car selected",
                    "Entering My Cars directly from freeroam and not a garage",
                    "Wrong start row",
                    "Assuming Auto3 verifies the car model",
                    "Running unlock mode while unsure",
                    (
                        "The number of cars wished to be unlocked are misaligned, "
                        "either with other cars in between or otherwise not in a continuous "
                        "string (see screenshot Auto3 Guide)."
                    ),
                )
            )
        )
        add_section_heading(content_layout, "Recovery")
        content_layout.addWidget(
            build_text_label(
                "If unsure which car is selected, do not run unlock mode. Re-sort Recently Added and verify the selected Subaru first."
            )
        )
        add_section_heading(content_layout, "Safety")
        content_layout.addWidget(
            build_bullet_list(
                (
                    "Unlock mode can spend skill points.",
                    "Current validated max: 4 cars.",
                    "Validated traversal: A1 -> B1 -> C1 -> A2.",
                )
            )
        )
        return content

    def build_faq_content() -> QWidget:
        return build_section_content(
            tuple(
                build_text_label(
                    f"{question.question} {question.answer}"
                )
                for question in screen.common_questions.questions
            )
        )

    def build_troubleshooting_content() -> QWidget:
        return build_section_content(
            tuple(
                build_text_label(
                    f"{question.question} {question.answer}"
                )
                for question in screen.troubleshooting.questions
            )
            + (
                build_text_label("Known issue: Auto3 is validated for max 4 cars and start row A."),
                build_text_label("Safety note: stop with F8 whenever the visible FH6 state looks wrong."),
            )
        )

    sections = (
        (
            "Operator Knowledge / Getting Started",
            "Pick an automation, read the readiness card, and use the matching guide if the starting position is unclear.",
            build_getting_started_content,
        ),
        (
            "Auto1 Guide",
            "Start from the post-race Restart screen where X restarts the event.",
            build_auto1_content,
        ),
        (
            "Auto2 Guide",
            "Auto2 purchases the Subaru Impreza 22B-STi Version (1998) from Autoshow.",
            build_auto2_content,
        ),
        (
            "Auto3 Guide",
            "Auto3 unlocks the validated wheelspin perk path on the currently selected Subaru.",
            build_auto3_content,
        ),
        (
            "FAQ",
            "Short answers for common operator questions.",
            build_faq_content,
        ),
        (
            "Troubleshooting",
            "Calm recovery guidance when FH6 state or automation alignment is unclear.",
            build_troubleshooting_content,
        ),
    )

    layout.addWidget(build_text_label("Operator Knowledge", role="heading"))
    layout.addWidget(
        build_text_label(
            "Use Help for starting positions, operator checks, and recovery guidance.",
            role="summary",
        )
    )
    layout.addSpacing(8)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setFrameShape(QFrame.Shape.NoFrame)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll_area.setStyleSheet(
        f"""
        QScrollArea {{
            background: transparent;
            border: none;
        }}
        QScrollBar:vertical {{
            background: {COLOR_SURFACE_RECESSED};
            width: 8px;
            margin: 2px 0 2px 0;
            border-radius: 4px;
        }}
        QScrollBar::handle:vertical {{
            background: {COLOR_BORDER_STRONG};
            border-radius: 4px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        """
    )

    scroll_content = QWidget()
    scroll_content.setStyleSheet("background: transparent; border: none;")
    scroll_outer_layout = QHBoxLayout(scroll_content)
    scroll_outer_layout.setContentsMargins(10, 0, 10, 0)
    scroll_outer_layout.setSpacing(0)

    scroll_column = QWidget()
    scroll_column.setStyleSheet("background: transparent; border: none;")
    scroll_column.setMaximumWidth(500)
    scroll_column.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Preferred,
    )
    scroll_layout = QVBoxLayout(scroll_column)
    scroll_layout.setContentsMargins(0, 0, 0, 0)
    scroll_layout.setSpacing(7)
    scroll_outer_layout.addStretch(1)
    scroll_outer_layout.addWidget(scroll_column)
    scroll_outer_layout.addStretch(1)

    section_buttons: list[QPushButton] = []
    section_content_widgets: list[QWidget] = []

    def update_section_styles(expanded_index: int) -> None:
        for index, button in enumerate(section_buttons):
            expanded = index == expanded_index
            button.setText(
                f"{'v' if expanded else '>'}  {sections[index][0]}\n{sections[index][1]}"
            )
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {COLOR_SURFACE_CARD_RAISED if expanded else COLOR_SURFACE_CARD};
                    border: 1px solid {COLOR_ACCENT_PRIMARY if expanded else COLOR_BORDER_SUBTLE};
                    border-radius: 16px;
                    color: {COLOR_TEXT_PRIMARY};
                    font-size: {shell_spec.typography.detail_size}px;
                    font-weight: 600;
                    padding: 10px 12px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    border-color: {COLOR_ACCENT_HOVER};
                    background-color: {COLOR_SURFACE_CARD_RAISED};
                }}
                """
            )
            section_content_widgets[index].setVisible(expanded)

    def expand_section(section_index: int) -> None:
        currently_open = section_content_widgets[section_index].isVisible()
        if currently_open:
            section_content_widgets[section_index].setVisible(False)
            update_section_styles(-1)
            return
        update_section_styles(section_index)

    for index, (_, _, content_builder) in enumerate(sections):
        section_frame = QFrame()
        section_frame.setObjectName("HelpAccordionSection")
        section_frame.setFrameShape(QFrame.Shape.NoFrame)
        section_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Maximum,
        )
        section_frame.setStyleSheet(
            f"""
            QFrame#HelpAccordionSection {{
                background-color: {COLOR_SURFACE_CARD_SOFT};
                border: 1px solid {COLOR_BORDER_SUBTLE};
                border-radius: 18px;
            }}
            """
        )
        section_layout = QVBoxLayout(section_frame)
        section_layout.setContentsMargins(8, 8, 8, 8)
        section_layout.setSpacing(0)

        section_button = QPushButton()
        section_button.setObjectName("HelpAccordionHeader")
        section_button.setMinimumHeight(66)
        section_button.setCursor(Qt.CursorShape.PointingHandCursor)
        section_button.clicked.connect(
            lambda _checked=False, section_index=index: expand_section(section_index)
        )
        section_content = build_section_content((content_builder(),))
        section_content.setVisible(False)

        section_buttons.append(section_button)
        section_content_widgets.append(section_content)
        section_layout.addWidget(section_button)
        section_layout.addWidget(section_content)
        scroll_layout.addWidget(section_frame)

    scroll_layout.addStretch(1)
    scroll_area.setWidget(scroll_content)
    layout.addWidget(scroll_area, 1)
    update_section_styles(0)


def _build_settings_screen_content(layout, shell_spec: PrototypeShellSpec) -> None:
    from PySide6.QtWidgets import (
        QFrame,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QSizePolicy,
        QVBoxLayout,
        QWidget,
    )

    screen = build_settings_screen()

    expected = screen.expected_application_behavior.settings
    safety = screen.safety_and_operational_preferences.settings
    advanced = screen.advanced_system_preferences.settings

    layout.addWidget(
        _build_visual_card(
            title="Quiet system control",
            summary=screen.primary_intention,
            details=(
                "Settings control the app shell, not automation timing or profile behavior.",
            ),
            shell_spec=shell_spec,
            treatment="hero",
        )
    )
    layout.addSpacing(6)

    settings_stage = QFrame()
    settings_stage.setObjectName("DesktopCard")
    settings_stage.setFrameShape(QFrame.Shape.NoFrame)
    settings_stage.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    _style_visual_card(settings_stage, treatment="primary")

    settings_stage_layout = QVBoxLayout(settings_stage)
    settings_stage_layout.setContentsMargins(12, 10, 12, 10)
    settings_stage_layout.setSpacing(7)

    expected_label = QLabel("Expected application behavior")
    _style_eyebrow_label(expected_label, primary=True)
    settings_stage_layout.addWidget(expected_label)

    expected_grid = QHBoxLayout()
    expected_grid.setContentsMargins(0, 0, 0, 0)
    expected_grid.setSpacing(7)
    for setting in expected:
        expected_grid.addWidget(
            _build_setting_item_card(
                setting,
                shell_spec=shell_spec,
                status_text=_setting_status_label(setting),
                treatment="primary",
            )
        )
    settings_stage_layout.addLayout(expected_grid)

    boundary_note = QLabel(
        "Execution behavior stays in Profiles. Settings only controls the app shell."
    )
    _style_detail_label(boundary_note, shell_spec=shell_spec)
    settings_stage_layout.addWidget(boundary_note)

    license_button = QPushButton("Manage offline license")
    license_button.setToolTip(
        "View Community or licensed entitlements and import a signed FAA license."
    )
    license_button.clicked.connect(
        lambda: _show_license_management_dialog(settings_stage)
    )
    settings_stage_layout.addWidget(license_button)

    layout.addWidget(settings_stage)
    layout.addSpacing(6)
    layout.addLayout(
        _build_card_row(
            cards=(
                _build_settings_section_card(
                    title="Safety preferences",
                    settings=safety,
                    shell_spec=shell_spec,
                    treatment="secondary",
                ),
                _build_settings_section_card(
                    title="Advanced system",
                    settings=advanced,
                    shell_spec=shell_spec,
                    treatment="tertiary",
                ),
            ),
            shell_spec=shell_spec,
        )
    )


def _show_license_management_dialog(parent) -> None:
    from desktop.license_dialog import show_license_dialog

    show_license_dialog(parent)


def _build_companion_mode_widget(
    shell_spec: PrototypeShellSpec,
    return_to_preparation,
    request_stop,
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
    stop_request_button = QPushButton("Request Stop")
    _style_secondary_button(stop_request_button, shell_spec=shell_spec)
    stop_card["layout"].addWidget(stop_request_button)

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
            "summary": "Companion Mode is waiting for a prepared run.",
            "execution_active": "false",
        }
    }

    def update_companion_mode(companion_state: dict[str, str]) -> None:
        current_companion_state["value"] = companion_state
        is_real_auto1_running = _is_real_auto1_execution_state(companion_state)
        is_real_desktop_running = _is_real_desktop_execution_state(companion_state)
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
            details=("Guarded desktop execution is active for the selected automation.",),
        )
        _set_preparation_card_text(
            focus_card,
            title=companion_state["focus"],
            summary="Focus handoff status",
            details=("Focus state follows the selected automation boundary.",),
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
            details=("The completion state opens automatically when the guarded run returns.",),
        )
        _set_preparation_card_text(
            stop_card,
            title="Stop safely",
            summary=companion_state["stop"],
            details=(
                (
                    "Use F8 or Request Stop. Cleanup is handled by the guarded Auto1 runner."
                    if is_real_auto1_running
                    else "Use F8 emergency stop for this guarded runner."
                    if is_real_desktop_running
                    else "Stop controls become available during an active guarded run."
                ),
            ),
        )
        stop_request_button.setEnabled(is_real_auto1_running)
        back_button.setEnabled(not is_real_desktop_running)

    def request_stop_from_ui() -> None:
        message = request_stop()
        current_state = dict(current_companion_state["value"])
        current_state["stop"] = message
        current_state["summary"] = "Stop requested. Waiting for guarded cleanup and completion."
        update_companion_mode(current_state)

    stop_request_button.clicked.connect(request_stop_from_ui)
    update_companion_mode(current_companion_state["value"])

    return container, update_companion_mode


def _build_completion_state_widget(
    shell_spec: PrototypeShellSpec,
    return_to_preparation,
    return_home,
):
    from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

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

    action_row = QHBoxLayout()
    action_row.setContentsMargins(0, 0, 0, 0)
    action_row.setSpacing(shell_spec.vertical_rhythm.group_spacing)
    prepare_again_button = QPushButton("Prepare Again")
    return_preparation_button = QPushButton("Automation Environment")
    return_home_button = QPushButton("Return Home")
    _style_primary_button(prepare_again_button, shell_spec=shell_spec)
    _style_secondary_button(return_preparation_button, shell_spec=shell_spec)
    _style_secondary_button(return_home_button, shell_spec=shell_spec)
    prepare_again_button.clicked.connect(return_to_preparation)
    return_preparation_button.clicked.connect(return_to_preparation)
    return_home_button.clicked.connect(return_home)
    action_row.addWidget(prepare_again_button)
    action_row.addWidget(return_preparation_button)
    action_row.addWidget(return_home_button)
    layout.addLayout(action_row)
    layout.addStretch()

    states_by_id = {
        state.state_id: state for state in shell_spec.completion_lifecycle.states
    }

    def update_completion_state(state_id: str, companion_state: dict[str, str]) -> None:
        state = states_by_id.get(state_id, states_by_id["refused"])
        automation_name = companion_state.get("automation_name", "Prepared operation")
        profile_name = companion_state.get("profile_name", "Selected profile")
        execution_message = companion_state.get(
            "execution_message",
            "No automation result has been produced for this state.",
        )
        outcome_details = (
            (automation_name, execution_message)
            if state_id == "refused"
            else (automation_name,)
        )

        _set_preparation_card_text(
            outcome_card,
            title=state.title,
            summary=(
                "Paused before or during Auto1 execution."
                if state_id == "refused"
                else state.emotional_treatment
            ),
            details=outcome_details,
        )
        _set_preparation_card_text(
            summary_card,
            title=("Reason" if state_id == "refused" else state.summary),
            summary=profile_name,
            details=(execution_message,),
        )
        _set_preparation_card_text(
            next_step_card,
            title=state.suggested_next_step,
            summary="Choose the next safe step when ready.",
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
                _build_section_card(profile, shell_spec=shell_spec),
                _build_section_card(warnings, shell_spec=shell_spec),
            ),
            shell_spec=shell_spec,
        )
    )
    layout.addSpacing(shell_spec.vertical_rhythm.section_spacing)
    layout.addWidget(_build_section_card(overview, shell_spec=shell_spec))
    layout.addSpacing(shell_spec.vertical_rhythm.section_spacing)
    layout.addWidget(_build_section_card(readiness, shell_spec=shell_spec))
    layout.addSpacing(shell_spec.vertical_rhythm.section_spacing)
    layout.addLayout(
        _build_card_row(
            cards=(
                _build_section_card(advanced, shell_spec=shell_spec),
                _build_section_card(run, shell_spec=shell_spec),
            ),
            shell_spec=shell_spec,
        )
    )


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
    card.setObjectName("DesktopCard")
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


def _desktop_baseline_summary(automation_id: str) -> str:
    summaries = {
        "auto1": "Post-race Restart screen.",
        "auto2": "Autoshow at the validated buy-car menu.",
        "auto3": "Garage -> Cars -> My Cars -> Recently Added.",
    }
    return summaries.get(automation_id, "Use the documented starting position for this automation.")


def _desktop_baseline_details(automation_id: str, readiness_model) -> tuple[str, ...]:
    if automation_id == "auto1":
        return (
            "Purpose: repeated race automation.",
            "Complete one race first; pressing X should restart the event.",
            "Expected Result: repeated race restart and completion.",
            "Safety: supervised automation. Keep F8 available. Need help? See Help -> Auto1 Guide.",
        )

    if automation_id == "auto2":
        return (
            "Purpose: purchase the validated wheelspin vehicle.",
            "Target: Subaru Impreza 22B-STi Version (1998).",
            "Expected Result: purchases the selected validated Subaru.",
            "Safety: uses credits. Use test mode first if alignment is uncertain. Need help? See Help -> Auto2 Guide.",
        )

    if automation_id == "auto3":
        return (
            "Purpose: unlock the validated wheelspin perk path.",
            "Target assumption: operates on the currently selected vehicle and does not verify the car model.",
            "Selected vehicle should be the first newly purchased Subaru Impreza 22B-STi Version (1998).",
            "Safety: uses skill points. Max 4 cars. Traversal: A1 -> B1 -> C1 -> A2. Need help? See Help -> Auto3 Guide.",
        )

    return (
        readiness_model.expected_baseline,
        readiness_model.manual_positioning_assumption,
    )


def _format_profile_list(profiles: tuple[object, ...]) -> str:
    if not profiles:
        return "No profiles available."

    return " / ".join(profile.profile_name for profile in profiles[:3])


def _load_desktop_profile_settings() -> list[dict[str, Any]]:
    from profiles import ProfileManager

    profile_manager = ProfileManager()
    loaded_profiles: list[dict[str, Any]] = []

    for profile_path in sorted(profile_manager.official_profiles_path.glob("*.json")):
        profile_data = profile_manager.load_profile(profile_path)
        if profile_data.get("profile_type") in {
            "auto1_race",
            "auto2_buy_car",
            "auto3_skill_tree",
        }:
            loaded_profiles.append(
                {
                    "profile_id": profile_data["profile_id"],
                    "data": profile_data,
                    "source": "official",
                }
            )

    for profile_path in sorted(profile_manager.custom_profiles_path.glob("*.json")):
        profile_data = profile_manager.load_profile(profile_path)
        loaded_profiles.append(
            {
                "profile_id": profile_data["profile_id"],
                "data": profile_data,
                "source": "custom",
            }
        )

    return loaded_profiles


def _profile_settings_selector_text(profile_data: dict[str, Any]) -> str:
    lock_state = "Locked default" if profile_data.get("is_official") else "Custom editable"
    return (
        f"{profile_data['profile_name']}\n"
        f"{_profile_type_label(profile_data.get('profile_type'))} - {lock_state}"
    )


def _profile_settings_summary(profile_data: dict[str, Any]) -> str:
    timing_count = len(profile_data.get("timings", {}))
    profile_state = "Official locked profile" if profile_data.get("is_official") else "Custom editable profile"
    return f"{profile_state}. {timing_count} timing value(s) shown."


def _profile_settings_status(profile_data: dict[str, Any]) -> str:
    if profile_data.get("is_official"):
        return "Official defaults are protected. Duplicate to custom before saving timing changes."

    return "Custom profile timing controls are editable here. Save wiring is the next step."


def _profile_type_label(profile_type: str | None) -> str:
    labels = {
        "auto1_race": "Auto1 Race",
        "auto2_buy_car": "Auto2 Buy Car",
        "auto3_skill_tree": "Auto3 Skill Tree",
    }
    return labels.get(profile_type or "", "Profile")


def _timing_display_label(timing_key: str) -> str:
    labels = {
        "startup_delay": "Startup delay",
        "wait_after_restart": "After restart",
        "wait_after_first_confirm": "After first confirm",
        "race_duration": "Race drive duration",
        "post_cycle_delay": "After cycle",
        "menu_key_delay": "Menu keypress delay",
        "wait_after_menu_confirm": "After menu confirm",
        "wait_after_car_selection": "After car selection",
        "wait_after_purchase_confirm": "After purchase confirm",
        "skill_tree_key_delay": "Skill tree keypress delay",
        "wait_after_get_in": "After get in",
        "wait_after_get_in_next_car": "Later-car recovery wait",
        "wait_after_menu_open": "After menu open",
        "wait_after_unlock": "After unlock",
    }
    return labels.get(timing_key, timing_key.replace("_", " ").title())


def _profile_selector_text(profile) -> str:
    automation_name = profile.automation_name or _profile_automation_type_label(
        profile.automation_id
    )
    tier = profile.package_tier.value.title()
    confidence = profile.validation_confidence.value.title()
    return f"{profile.profile_name}\n{automation_name} - {tier} - {confidence}"


def _profile_detail_lines(profile) -> tuple[str, ...]:
    automation_name = profile.automation_name or _profile_automation_type_label(
        profile.automation_id
    )
    return (
        f"{automation_name}. {profile.reliability_posture}",
        f"{profile.package_tier.value.title()} / {profile.recommendation_status.value.title()} / {profile.availability.value.title()}",
        profile.customization_status,
    )


def _profile_automation_type_label(automation_id: str | None) -> str:
    labels = {
        "auto1": "Auto1 Race",
        "auto2": "Auto2 Buy Car",
        "auto3": "Auto3 Skill Tree",
    }
    return labels.get(automation_id or "", "Automation profile")


def _format_setting_list(settings: tuple[object, ...]) -> str:
    if not settings:
        return "No settings available."

    return " / ".join(setting.label for setting in settings[:3])


def _setting_status_label(setting) -> str:
    return "Available" if setting.is_editable_now else "Planned"


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
    card.setObjectName("DesktopCard")
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


def _clear_layout(layout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        child_layout = item.layout()
        child_widget = item.widget()

        if child_layout is not None:
            _clear_layout(child_layout)

        if child_widget is not None:
            child_widget.deleteLater()


def _build_setting_item_card(
    setting,
    shell_spec: PrototypeShellSpec,
    status_text: str,
    treatment: str,
):
    from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout

    card = QFrame()
    card.setObjectName("DesktopCard")
    card.setFrameShape(QFrame.Shape.NoFrame)
    card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    _style_visual_card(card, treatment=treatment)

    card_layout = QVBoxLayout(card)
    card_layout.setContentsMargins(9, 8, 9, 8)
    card_layout.setSpacing(4)

    status_label = QLabel(status_text.upper())
    _style_eyebrow_label(status_label, primary=status_text == "Available")
    title_label = QLabel(setting.label)
    _style_card_title(title_label, shell_spec=shell_spec, treatment=treatment)
    detail_label = QLabel(_compact_text(setting.description, 64))
    _style_detail_label(detail_label, shell_spec=shell_spec)

    card_layout.addWidget(status_label)
    card_layout.addWidget(title_label)
    card_layout.addWidget(detail_label)

    return card


def _build_settings_section_card(
    title: str,
    settings: tuple[object, ...],
    shell_spec: PrototypeShellSpec,
    treatment: str,
):
    from PySide6.QtWidgets import QFrame, QVBoxLayout

    card = QFrame()
    card.setObjectName("DesktopCard")
    card.setFrameShape(QFrame.Shape.NoFrame)
    _style_visual_card(card, treatment=treatment)

    card_layout = QVBoxLayout(card)
    card_layout.setContentsMargins(10, 9, 10, 9)
    card_layout.setSpacing(6)

    section_title = _build_footer_metadata_label(title.upper(), shell_spec=shell_spec)
    card_layout.addWidget(section_title)

    for setting in settings:
        card_layout.addWidget(
            _build_setting_item_card(
                setting,
                shell_spec=shell_spec,
                status_text=_setting_status_label(setting),
                treatment=treatment,
            )
        )

    return card


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
    card.setObjectName("DesktopCard")
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
            QFrame#DesktopCard {{
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
            QFrame#DesktopCard {{
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
            QFrame#DesktopCard {{
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
            QFrame#DesktopCard {{
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
            QFrame#DesktopCard {{
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
            QFrame#DesktopCard {{
                background-color: {COLOR_SURFACE_CARD_RAISED};
                border: 1px solid {COLOR_ACCENT_PRIMARY};
                border-radius: 18px;
            }}
            """
        )
        return

    card.setStyleSheet(
        f"""
        QFrame#DesktopCard {{
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


def _style_runtime_spinbox(spinbox, shell_spec: PrototypeShellSpec) -> None:
    spinbox.setStyleSheet(
        f"""
        QDoubleSpinBox, QSpinBox {{
            font-size: {shell_spec.typography.summary_size}px;
            font-weight: 600;
            color: {COLOR_TEXT_PRIMARY};
            background-color: {COLOR_SURFACE_CARD_SOFT};
            border: 1px solid {COLOR_BORDER_SUBTLE};
            border-radius: 10px;
            padding: 5px 8px;
        }}
        QDoubleSpinBox:focus, QSpinBox:focus {{
            border: 1px solid {COLOR_ACCENT_PRIMARY};
        }}
        QDoubleSpinBox:disabled, QSpinBox:disabled {{
            color: {COLOR_TEXT_FAINT};
            border: 1px solid {COLOR_BORDER_SUBTLE};
        }}
        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button,
        QSpinBox::up-button, QSpinBox::down-button {{
            width: 14px;
            background-color: transparent;
            border: none;
            border-radius: 9px;
        }}
        QDoubleSpinBox::up-arrow, QDoubleSpinBox::down-arrow,
        QSpinBox::up-arrow, QSpinBox::down-arrow {{
            width: 7px;
            height: 7px;
        }}
        """
    )


def _style_runtime_combobox(combobox, shell_spec: PrototypeShellSpec) -> None:
    arrow_path = (Path(__file__).with_name("assets") / "chevron_down.svg").as_posix()
    combobox.setStyleSheet(
        f"""
        QComboBox {{
            font-size: {shell_spec.typography.summary_size}px;
            font-weight: 520;
            color: {COLOR_TEXT_PRIMARY};
            background-color: {COLOR_SURFACE_CARD_SOFT};
            border: 1px solid {COLOR_BORDER_SUBTLE};
            border-radius: 10px;
            padding: 5px 8px;
        }}
        QComboBox:focus {{
            border: 1px solid {COLOR_ACCENT_PRIMARY};
        }}
        QComboBox:disabled {{
            color: {COLOR_TEXT_FAINT};
            border: 1px solid {COLOR_BORDER_SUBTLE};
        }}
        QComboBox::drop-down {{
            width: 26px;
            background-color: transparent;
            border: none;
            border-radius: 9px;
        }}
        QComboBox::down-arrow {{
            image: url("{arrow_path}");
            width: 10px;
            height: 10px;
        }}
        QComboBox QAbstractItemView {{
            color: {COLOR_TEXT_PRIMARY};
            background-color: {COLOR_SURFACE_CARD_SOFT};
            selection-background-color: {COLOR_SURFACE_CARD_RAISED};
        }}
        """
    )


def _style_profile_selector_button(
    button,
    shell_spec: PrototypeShellSpec,
    selected: bool,
) -> None:
    background = COLOR_SURFACE_CARD_RAISED if selected else COLOR_SURFACE_CARD_SOFT
    border = COLOR_ACCENT_PRIMARY if selected else COLOR_BORDER_SUBTLE
    text_color = COLOR_TEXT_PRIMARY if selected else COLOR_TEXT_SECONDARY
    button.setStyleSheet(
        f"""
        QPushButton {{
            font-size: {shell_spec.typography.detail_size}px;
            font-weight: 580;
            color: {text_color};
            background-color: {background};
            border: 1px solid {border};
            border-radius: 10px;
            padding: 7px 10px;
            text-align: left;
        }}
        QPushButton:hover {{
            color: {COLOR_TEXT_PRIMARY};
            background-color: {COLOR_SURFACE_CARD_RAISED};
            border: 1px solid {COLOR_BORDER_STRONG};
        }}
        QPushButton:pressed {{
            background-color: {COLOR_SURFACE_RECESSED};
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


DesktopShellSpec = PrototypeShellSpec


def build_companion_shell_spec() -> DesktopShellSpec:
    return build_prototype_shell_spec()


def build_desktop_app_spec() -> DesktopShellSpec:
    return build_companion_shell_spec()


def launch_companion_shell() -> int:
    return launch_pyside6_shell_prototype()


def launch_desktop_app() -> int:
    return launch_companion_shell()


def main() -> int:
    return launch_desktop_app()


if __name__ == "__main__":
    raise SystemExit(main())
