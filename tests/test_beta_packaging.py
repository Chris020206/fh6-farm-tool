import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import zipfile

_SCRIPT_PATH = Path(__file__).resolve().parents[1] / "packaging" / "build_beta_package.py"
_SPEC = importlib.util.spec_from_file_location("faa_beta_packaging", _SCRIPT_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Packaging script could not be loaded for testing.")
_PACKAGING = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_PACKAGING)

APP_NAME = _PACKAGING.APP_NAME
PACKAGE_NAME = _PACKAGING.PACKAGE_NAME
REQUIRED_PACKAGE_FILES = _PACKAGING.REQUIRED_PACKAGE_FILES
ZIP_NAME = _PACKAGING.ZIP_NAME
PackageBuildError = _PACKAGING.PackageBuildError
build_beta_package = _PACKAGING.build_beta_package
build_beta_zip = _PACKAGING.build_beta_zip


class BetaPackagingTest(unittest.TestCase):
    def test_assembly_and_zip_use_current_product_name_and_clean_tree(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self._create_valid_sources(root)

            package_dir = build_beta_package(root)
            zip_path = build_beta_zip(package_dir, root)

            self.assertEqual(root / "output" / PACKAGE_NAME, package_dir)
            self.assertEqual(root / "output" / ZIP_NAME, zip_path)
            self.assertTrue((package_dir / f"{APP_NAME}.exe").is_file())
            self.assertTrue((package_dir / "_internal" / "runtime.dll").is_file())
            self.assertTrue((package_dir / "config" / "default_settings.json").is_file())
            self.assertTrue((package_dir / "profiles" / "official" / "auto1.json").is_file())
            self.assertTrue((package_dir / "profiles" / "custom" / "custom.json").is_file())
            self.assertFalse((package_dir / "profiles" / "profile_manager.py").exists())
            self.assertFalse((package_dir / "profiles" / "__pycache__").exists())
            self.assertTrue((package_dir / "assets" / "branding" / "app_icon.ico").is_file())
            self.assertTrue((package_dir / "assets" / "Guides" / "auto1.png").is_file())
            self.assertTrue((package_dir / "logs").is_dir())
            self.assertEqual([], list((package_dir / "logs").iterdir()))
            for file_name in REQUIRED_PACKAGE_FILES:
                self.assertTrue((package_dir / file_name).is_file())
            self.assertFalse((package_dir / "unapproved-extra.txt").exists())

            with zipfile.ZipFile(zip_path) as archive:
                names = set(archive.namelist())
            archive_root = f"{PACKAGE_NAME}/"
            self.assertIn(archive_root + f"{APP_NAME}.exe", names)
            self.assertIn(archive_root + "README_INSTALL.txt", names)
            self.assertFalse(any("FH6 Farm Tool" in name for name in names))

    def test_missing_dist_build_fails_with_clear_message(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package_files").mkdir()
            (root / "config").mkdir()
            (root / "profiles").mkdir()
            (root / "assets" / "branding").mkdir(parents=True)

            with self.assertRaisesRegex(
                PackageBuildError,
                "Missing required PyInstaller build folder",
            ):
                build_beta_package(root)

    def test_missing_required_package_file_fails_before_output_cleanup(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self._create_valid_sources(root)
            (root / "package_files" / "VERSION.txt").unlink()
            existing_output = root / "output" / PACKAGE_NAME
            existing_output.mkdir(parents=True)
            marker = existing_output / "keep.txt"
            marker.write_text("existing", encoding="utf-8")

            with self.assertRaisesRegex(PackageBuildError, "VERSION.txt"):
                build_beta_package(root)

            self.assertTrue(marker.exists())

    @staticmethod
    def _create_valid_sources(root: Path) -> None:
        dist = root / "dist" / APP_NAME
        (dist / "_internal").mkdir(parents=True)
        (dist / f"{APP_NAME}.exe").write_bytes(b"exe")
        (dist / "_internal" / "runtime.dll").write_bytes(b"runtime")

        config = root / "config"
        config.mkdir()
        (config / "default_settings.json").write_text("{}", encoding="utf-8")

        profiles = root / "profiles"
        (profiles / "official").mkdir(parents=True)
        (profiles / "custom").mkdir()
        (profiles / "__pycache__").mkdir()
        (profiles / "official" / "auto1.json").write_text("{}", encoding="utf-8")
        (profiles / "custom" / "custom.json").write_text("{}", encoding="utf-8")
        (profiles / "profile_manager.py").write_text("source", encoding="utf-8")
        (profiles / "__pycache__" / "profile.pyc").write_bytes(b"cache")

        assets = root / "assets"
        (assets / "branding").mkdir(parents=True)
        (assets / "Guides").mkdir()
        (assets / "branding" / "app_icon.ico").write_bytes(b"icon")
        (assets / "Guides" / "auto1.png").write_bytes(b"image")

        package_files = root / "package_files"
        package_files.mkdir()
        for file_name in REQUIRED_PACKAGE_FILES:
            (package_files / file_name).write_text(
                f"Forza Automation Assist {file_name}",
                encoding="utf-8",
            )
        (package_files / "unapproved-extra.txt").write_text("extra", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
