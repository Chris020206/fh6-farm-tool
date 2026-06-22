import inspect
import unittest

from desktop import app
from desktop import shell


class DesktopShellTest(unittest.TestCase):
    def test_production_shell_facade_imports_safely(self) -> None:
        spec = shell.build_desktop_app_spec()

        self.assertEqual("Forza Automation Assist", spec.window_title)
        self.assertEqual(640, spec.window_width)
        self.assertEqual(860, spec.window_height)
        self.assertTrue(spec.is_fixed_size)

    def test_desktop_app_uses_production_shell_facade(self) -> None:
        source = inspect.getsource(app)

        self.assertIn("desktop.shell", source)
        self.assertNotIn("pyside6_shell_prototype", source)

    def test_public_shell_facade_avoids_prototype_language(self) -> None:
        self.assertNotIn("prototype", shell.__doc__.lower())
        self.assertEqual("Forza Automation Assist", shell.build_desktop_app_spec().window_title)


if __name__ == "__main__":
    unittest.main()
