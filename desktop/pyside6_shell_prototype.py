from dataclasses import dataclass

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
class PrototypeShellSpec:
    window_title: str
    sidebar_destinations: tuple[SidebarDestination, ...]
    screens: tuple[PrototypeScreen, ...]


def build_prototype_shell_spec() -> PrototypeShellSpec:
    sidebar_destinations = get_sidebar_destinations()

    return PrototypeShellSpec(
        window_title="FH6 Farm Tool - PySide6 Shell Prototype",
        sidebar_destinations=sidebar_destinations,
        screens=tuple(
            _build_prototype_screen(get_screen_descriptor(destination.screen_id))
            for destination in sidebar_destinations
        ),
    )


def launch_pyside6_shell_prototype() -> int:
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
    window.resize(1100, 720)

    root = QWidget()
    root_layout = QHBoxLayout(root)

    sidebar = QListWidget()
    sidebar.setFixedWidth(220)
    sidebar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

    stacked_screens = QStackedWidget()

    for screen in shell_spec.screens:
        item = QListWidgetItem(screen.title)
        item.setData(256, screen.screen_id.value)
        sidebar.addItem(item)
        stacked_screens.addWidget(_build_screen_widget(screen))

    sidebar.currentRowChanged.connect(stacked_screens.setCurrentIndex)
    sidebar.setCurrentRow(0)

    root_layout.addWidget(sidebar)
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


def _build_screen_widget(screen: PrototypeScreen):
    from PySide6.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QWidget

    container = QWidget()
    layout = QVBoxLayout(container)
    layout.addWidget(QLabel(screen.title))
    layout.addWidget(QLabel(screen.primary_intention))

    for zone in screen.zones:
        group_box = QGroupBox(zone.role.value.title())
        zone_layout = QVBoxLayout(group_box)
        zone_layout.addWidget(QLabel(zone.purpose))
        layout.addWidget(group_box)

    return container


def _vertical_separator(frame_type):
    separator = frame_type()
    separator.setFrameShape(frame_type.Shape.VLine)
    separator.setFrameShadow(frame_type.Shadow.Sunken)
    return separator


def main() -> int:
    return launch_pyside6_shell_prototype()


if __name__ == "__main__":
    raise SystemExit(main())
