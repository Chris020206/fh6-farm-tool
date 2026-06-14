"""Production-facing desktop shell facade."""

from desktop.companion_shell import (
    DesktopShellSpec,
    build_desktop_app_spec,
    launch_desktop_app,
)

__all__ = [
    "DesktopShellSpec",
    "build_desktop_app_spec",
    "launch_desktop_app",
]
