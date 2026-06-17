from __future__ import annotations

import shutil
from pathlib import Path


BETA_VERSION = "v0.2.0-beta"
APP_NAME = "FH6 Farm Tool"
PACKAGE_NAME = f"{APP_NAME} {BETA_VERSION}"

REQUIRED_PACKAGE_FILES = (
    "README_INSTALL.txt",
    "SAFETY_AND_TRANSPARENCY.txt",
    "VERSION.txt",
    "KNOWN_ISSUES.txt",
)


class PackageBuildError(RuntimeError):
    """Raised when the beta package cannot be assembled."""


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _require_path(path: Path, label: str) -> None:
    if not path.exists():
        raise PackageBuildError(f"Missing required {label}: {path}")


def _copy_directory(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def build_beta_package(root: Path | None = None) -> Path:
    root = root or project_root()

    dist_dir = root / "dist" / APP_NAME
    executable = dist_dir / f"{APP_NAME}.exe"
    internal_dir = dist_dir / "_internal"
    package_files_dir = root / "package_files"
    config_dir = root / "config"
    profiles_dir = root / "profiles"
    branding_dir = root / "assets" / "branding"
    output_dir = root / "output" / PACKAGE_NAME

    _require_path(dist_dir, "PyInstaller build folder")
    _require_path(executable, "packaged executable")
    _require_path(internal_dir, "PyInstaller _internal folder")
    _require_path(package_files_dir, "package_files folder")
    _require_path(config_dir, "config folder")
    _require_path(profiles_dir, "profiles folder")

    for file_name in REQUIRED_PACKAGE_FILES:
        _require_path(package_files_dir / file_name, f"package file {file_name}")

    print("-----------------------------------")
    print("Building Beta Package...")

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    print("Copying executable...")
    shutil.copy2(executable, output_dir / executable.name)

    print("Copying _internal...")
    _copy_directory(internal_dir, output_dir / "_internal")

    print("Copying config...")
    _copy_directory(config_dir, output_dir / "config")

    print("Copying profiles...")
    _copy_directory(profiles_dir, output_dir / "profiles")

    print("Copying package files...")
    for source_file in sorted(package_files_dir.iterdir()):
        if source_file.is_file():
            shutil.copy2(source_file, output_dir / source_file.name)

    if branding_dir.exists():
        print("Copying branding assets...")
        assets_dir = output_dir / "assets"
        assets_dir.mkdir()
        _copy_directory(branding_dir, assets_dir / "branding")

    print("Creating logs...")
    (output_dir / "logs").mkdir()

    print("Done.")
    print()
    print("Package created:")
    print(output_dir.relative_to(root))
    print("-----------------------------------")

    return output_dir


def main() -> int:
    try:
        build_beta_package()
    except PackageBuildError as exc:
        print("-----------------------------------")
        print("Beta package build failed.")
        print(str(exc))
        print("-----------------------------------")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
