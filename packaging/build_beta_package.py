from __future__ import annotations

import shutil
from pathlib import Path


BETA_VERSION = "v0.2.0-beta"
APP_NAME = "Forza Automation Assist"
EDITION_NAME = "Community Edition"
PACKAGE_NAME = f"{APP_NAME} {EDITION_NAME} {BETA_VERSION}"
ZIP_NAME = "Forza_Automation_Assist_Community_Edition_v0.2.0-beta.zip"

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


def _require_directory(path: Path, label: str) -> None:
    if not path.is_dir():
        raise PackageBuildError(f"Missing required {label}: {path}")


def _require_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise PackageBuildError(f"Missing required {label}: {path}")


def _copy_directory(
    source: Path,
    destination: Path,
    *,
    ignore=None,
) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination, ignore=ignore)


def _locked_output_message(output_dir: Path) -> str:
    return "\n".join(
        (
            f"Output package folder appears locked: {output_dir}",
            "",
            "Windows could not remove the previous beta package output.",
            "Likely causes:",
            "- File Explorer is open inside output/",
            "- an image/logo file from the package is open",
            "- OneDrive is syncing the output folder",
            "- the packaged app is still running",
            "",
            "Close anything using the output folder, then delete output/ manually",
            "or rerun this script after the folder is unlocked.",
        )
    )


def _clean_previous_output(output_dir: Path) -> None:
    if not output_dir.exists():
        return

    print("Cleaning previous output package...")
    try:
        shutil.rmtree(output_dir)
    except PermissionError as exc:
        raise PackageBuildError(_locked_output_message(output_dir)) from None


def _clean_previous_zip(zip_path: Path) -> None:
    if not zip_path.exists():
        return
    print("Cleaning previous beta ZIP...")
    try:
        zip_path.unlink()
    except PermissionError:
        raise PackageBuildError(
            f"Output ZIP appears locked: {zip_path}\n\n"
            "Close File Explorer, archive tools, OneDrive sync activity, or any "
            "process using the ZIP, then rerun the packaging script."
        ) from None


def build_beta_package(root: Path | None = None) -> Path:
    root = root or project_root()

    dist_dir = root / "dist" / APP_NAME
    executable = dist_dir / f"{APP_NAME}.exe"
    internal_dir = dist_dir / "_internal"
    package_files_dir = root / "package_files"
    config_dir = root / "config"
    profiles_dir = root / "profiles"
    assets_dir = root / "assets"
    output_dir = root / "output" / PACKAGE_NAME

    _require_directory(dist_dir, "PyInstaller build folder")
    _require_file(executable, "packaged executable")
    _require_directory(internal_dir, "PyInstaller _internal folder")
    _require_directory(package_files_dir, "package_files folder")
    _require_directory(config_dir, "config folder")
    _require_directory(profiles_dir, "profiles folder")
    _require_directory(assets_dir, "assets folder")
    _require_directory(assets_dir / "branding", "branding assets folder")

    for file_name in REQUIRED_PACKAGE_FILES:
        _require_file(package_files_dir / file_name, f"package file {file_name}")

    print("-----------------------------------")
    print("Building Community Edition Package...")

    _clean_previous_output(output_dir)
    output_dir.mkdir(parents=True)

    print("Copying executable...")
    shutil.copy2(executable, output_dir / executable.name)

    print("Copying _internal...")
    _copy_directory(internal_dir, output_dir / "_internal")

    print("Copying config...")
    _copy_directory(
        config_dir,
        output_dir / "config",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )

    print("Copying profiles...")
    _copy_directory(
        profiles_dir,
        output_dir / "profiles",
        ignore=shutil.ignore_patterns("__pycache__", "*.py", "*.pyc"),
    )

    print("Copying assets...")
    _copy_directory(
        assets_dir,
        output_dir / "assets",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )

    print("Copying package files...")
    for file_name in REQUIRED_PACKAGE_FILES:
        source_file = package_files_dir / file_name
        shutil.copy2(source_file, output_dir / source_file.name)

    print("Creating logs...")
    (output_dir / "logs").mkdir()

    print("Done.")
    print()
    print("Package created:")
    print(output_dir.relative_to(root))
    print("-----------------------------------")

    return output_dir


def build_beta_zip(package_dir: Path, root: Path | None = None) -> Path:
    root = root or project_root()
    package_dir = Path(package_dir)
    expected_package_dir = root / "output" / PACKAGE_NAME
    if package_dir.resolve() != expected_package_dir.resolve():
        raise PackageBuildError(
            f"Unexpected beta package folder: {package_dir}. "
            f"Expected: {expected_package_dir}"
        )
    _require_directory(package_dir, "assembled beta package folder")

    zip_path = root / "output" / ZIP_NAME
    _clean_previous_zip(zip_path)
    print("Creating Community Edition ZIP...")
    try:
        created_archive = Path(
            shutil.make_archive(
                str(zip_path.with_suffix("")),
                "zip",
                root_dir=package_dir.parent,
                base_dir=package_dir.name,
            )
        )
    except (OSError, shutil.Error) as exc:
        raise PackageBuildError(f"Beta ZIP could not be created: {exc}") from exc

    print("ZIP created:")
    print(created_archive.relative_to(root))
    print(f"ZIP size: {created_archive.stat().st_size / (1024 * 1024):.1f} MB")
    print("-----------------------------------")
    return created_archive


def main() -> int:
    try:
        package_dir = build_beta_package()
        build_beta_zip(package_dir)
    except PackageBuildError as exc:
        print("-----------------------------------")
        print("Community Edition package build failed.")
        print(str(exc))
        print("-----------------------------------")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
