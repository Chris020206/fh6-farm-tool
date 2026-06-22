from pathlib import Path
from tempfile import TemporaryDirectory
import inspect
import unittest

from settings.execution_preferences import (
    ExecutionPreferences,
    ExecutionPreferencesStore,
)
from desktop.companion_shell import (
    ResourceSpendingConfirmationResult,
    _handle_resource_spending_confirmation,
    _resource_spending_confirmation_for,
    _show_resource_spending_confirmation,
)


class ExecutionPreferencesTest(unittest.TestCase):
    def test_confirmation_settings_default_on(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            store = ExecutionPreferencesStore(
                Path(temporary_directory) / "settings.json"
            )

            preferences = store.load()

        self.assertTrue(preferences.show_auto2_purchase_confirmation)
        self.assertTrue(preferences.show_auto3_unlock_confirmation)

    def test_confirmation_settings_persist_after_reload(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "settings.json"
            store = ExecutionPreferencesStore(path)
            store.save(
                ExecutionPreferences(
                    show_auto2_purchase_confirmation=False,
                    show_auto3_unlock_confirmation=True,
                )
            )

            reloaded = ExecutionPreferencesStore(path).load()

        self.assertFalse(reloaded.show_auto2_purchase_confirmation)
        self.assertTrue(reloaded.show_auto3_unlock_confirmation)

    def test_invalid_stored_values_fail_safe_to_on(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "settings.json"
            path.write_text(
                '{"execution": {'
                '"show_auto2_purchase_confirmation": "no", '
                '"show_auto3_unlock_confirmation": null}}',
                encoding="utf-8",
            )

            preferences = ExecutionPreferencesStore(path).load()

        self.assertTrue(preferences.show_auto2_purchase_confirmation)
        self.assertTrue(preferences.show_auto3_unlock_confirmation)

    def test_auto2_warning_includes_dont_show_again_checkbox(self) -> None:
        confirmation = _resource_spending_confirmation_for(
            {"automation_id": "auto2", "auto2_mode": "purchase"}
        )

        self.assertEqual("Don't show this again", confirmation.checkbox_label)

    def test_auto3_warning_includes_dont_show_again_checkbox(self) -> None:
        confirmation = _resource_spending_confirmation_for(
            {"automation_id": "auto3", "auto3_mode": "unlock"}
        )

        self.assertEqual("Don't show this again", confirmation.checkbox_label)

    def test_warning_dialog_renders_confirmation_checkbox(self) -> None:
        source = inspect.getsource(_show_resource_spending_confirmation)

        self.assertIn("QCheckBox(confirmation.checkbox_label)", source)
        self.assertIn("dialog.setCheckBox", source)

    def test_auto2_checked_continue_disables_persisted_warning(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            store = ExecutionPreferencesStore(
                Path(temporary_directory) / "settings.json"
            )
            companion_state = {"automation_id": "auto2", "auto2_mode": "purchase"}
            confirmation = _resource_spending_confirmation_for(companion_state)

            accepted = _handle_resource_spending_confirmation(
                companion_state,
                confirmation,
                store,
                show_confirmation=lambda _item: ResourceSpendingConfirmationResult(
                    accepted=True,
                    dont_show_again=True,
                ),
            )
            reloaded = ExecutionPreferencesStore(store.path).load()

        self.assertTrue(accepted)
        self.assertFalse(reloaded.show_auto2_purchase_confirmation)
        self.assertTrue(reloaded.show_auto3_unlock_confirmation)

    def test_auto3_checked_continue_disables_persisted_warning(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            store = ExecutionPreferencesStore(
                Path(temporary_directory) / "settings.json"
            )
            companion_state = {"automation_id": "auto3", "auto3_mode": "unlock"}
            confirmation = _resource_spending_confirmation_for(companion_state)

            accepted = _handle_resource_spending_confirmation(
                companion_state,
                confirmation,
                store,
                show_confirmation=lambda _item: ResourceSpendingConfirmationResult(
                    accepted=True,
                    dont_show_again=True,
                ),
            )
            reloaded = ExecutionPreferencesStore(store.path).load()

        self.assertTrue(accepted)
        self.assertTrue(reloaded.show_auto2_purchase_confirmation)
        self.assertFalse(reloaded.show_auto3_unlock_confirmation)

    def test_checked_cancel_does_not_change_persisted_warning(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            store = ExecutionPreferencesStore(
                Path(temporary_directory) / "settings.json"
            )
            companion_state = {"automation_id": "auto2", "auto2_mode": "purchase"}
            confirmation = _resource_spending_confirmation_for(companion_state)

            accepted = _handle_resource_spending_confirmation(
                companion_state,
                confirmation,
                store,
                show_confirmation=lambda _item: ResourceSpendingConfirmationResult(
                    accepted=False,
                    dont_show_again=True,
                ),
            )
            reloaded = store.load()

        self.assertFalse(accepted)
        self.assertTrue(reloaded.show_auto2_purchase_confirmation)
        self.assertTrue(reloaded.show_auto3_unlock_confirmation)


if __name__ == "__main__":
    unittest.main()
