"""Compatibility entrypoint for older PySide6 prototype commands.

Use `python -B -m desktop.app` for the production-facing desktop UI.
"""

from desktop.companion_shell import *  # noqa: F401,F403


if __name__ == "__main__":
    raise SystemExit(launch_desktop_app())
