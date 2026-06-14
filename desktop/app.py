"""Desktop UI application entrypoint."""

from desktop.shell import (
    DesktopShellSpec,
    build_desktop_app_spec,
    launch_desktop_app,
)


def main() -> int:
    return launch_desktop_app()


if __name__ == "__main__":
    raise SystemExit(main())
