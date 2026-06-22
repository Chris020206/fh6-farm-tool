"""Small desktop dialog for offline license status and import."""

from dataclasses import dataclass

from licensing.models import LicenseState
from licensing.service import LicenseService
from product.support import (
    community_feature_unavailable_message,
    license_activation_failure_message,
)


@dataclass(frozen=True)
class LicenseDialogStatus:
    edition: str
    status: str
    license_id: str
    enabled_features: tuple[str, ...]
    message: str


def license_dialog_status(state: LicenseState) -> LicenseDialogStatus:
    license_id = (
        state.license.payload.license_id
        if state.license is not None
        else "No local license"
    )
    return LicenseDialogStatus(
        edition=state.entitlements.edition.title(),
        status=state.status.replace("_", " ").title(),
        license_id=license_id,
        enabled_features=tuple(sorted(state.entitlements.features)),
        message=state.message,
    )


def select_and_import_license_file(
    parent,
    license_service: LicenseService,
    *,
    replacing: bool = False,
):
    """Select and validate a signed license through the existing service boundary."""
    from PySide6.QtWidgets import QFileDialog

    selected_path, _ = QFileDialog.getOpenFileName(
        parent,
        "Replace FAA license" if replacing else "Import FAA license",
        "",
        "FAA License (*.lic);;JSON Files (*.json);;All Files (*)",
    )
    if not selected_path:
        return None
    return license_service.import_file(selected_path)


def license_import_feedback(accepted: bool, success_message: str) -> str:
    return success_message if accepted else license_activation_failure_message()


def show_community_feature_dialog(parent) -> None:
    from PySide6.QtWidgets import QMessageBox

    from desktop.support_actions import open_official_discord

    dialog = QMessageBox(parent)
    dialog.setWindowTitle("Edition required - Forza Automation Assist")
    dialog.setIcon(QMessageBox.Icon.Information)
    dialog.setText(community_feature_unavailable_message())
    open_discord_button = dialog.addButton(
        "Open Discord",
        QMessageBox.ButtonRole.ActionRole,
    )
    dialog.addButton(QMessageBox.StandardButton.Close)
    dialog.exec()
    if dialog.clickedButton() is open_discord_button:
        open_official_discord()


def show_license_dialog(parent, license_service: LicenseService | None = None) -> None:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QDialog,
        QFileDialog,
        QHBoxLayout,
        QLabel,
        QPlainTextEdit,
        QPushButton,
        QVBoxLayout,
    )

    service = license_service or LicenseService()
    dialog = QDialog(parent)
    dialog.setWindowTitle("License - Forza Automation Assist")
    dialog.setModal(True)
    dialog.setMinimumWidth(480)

    layout = QVBoxLayout(dialog)
    layout.setContentsMargins(18, 16, 18, 16)
    layout.setSpacing(10)

    title = QLabel("Offline license")
    title.setStyleSheet("font-size: 18px; font-weight: 650;")
    layout.addWidget(title)

    status_label = QLabel()
    status_label.setWordWrap(True)
    status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    layout.addWidget(status_label)

    features_label = QLabel()
    features_label.setWordWrap(True)
    features_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    layout.addWidget(features_label)

    result_label = QLabel()
    result_label.setWordWrap(True)
    layout.addWidget(result_label)

    key_input = QPlainTextEdit()
    key_input.setPlaceholderText("Paste an FAA-LIC-v1 license key")
    key_input.setMaximumHeight(92)
    layout.addWidget(key_input)

    button_row = QHBoxLayout()
    import_file_button = QPushButton("Import license file")
    import_key_button = QPushButton("Import pasted key")
    close_button = QPushButton("Close")
    open_discord_button = QPushButton("Open Discord")
    button_row.addWidget(import_file_button)
    button_row.addWidget(import_key_button)
    button_row.addStretch(1)
    button_row.addWidget(open_discord_button)
    button_row.addWidget(close_button)
    layout.addLayout(button_row)

    def refresh_status() -> None:
        status = license_dialog_status(service.current_state())
        status_label.setText(
            f"Edition: {status.edition}\n"
            f"Status: {status.status}\n"
            f"License ID: {status.license_id}\n\n"
            f"{status.message}"
        )
        features_label.setText(
            "Enabled features:\n" + "\n".join(status.enabled_features)
        )

    def import_file() -> None:
        selected_path, _ = QFileDialog.getOpenFileName(
            dialog,
            "Import FAA license",
            "",
            "FAA License (*.lic);;JSON Files (*.json);;All Files (*)",
        )
        if not selected_path:
            return
        result = service.import_file(selected_path)
        result_label.setText(license_import_feedback(result.accepted, result.message))
        refresh_status()

    def import_key() -> None:
        result = service.import_key(key_input.toPlainText())
        result_label.setText(license_import_feedback(result.accepted, result.message))
        if result.accepted:
            key_input.clear()
        refresh_status()

    def open_discord() -> None:
        from desktop.support_actions import open_official_discord

        open_official_discord()

    import_file_button.clicked.connect(import_file)
    import_key_button.clicked.connect(import_key)
    open_discord_button.clicked.connect(open_discord)
    close_button.clicked.connect(dialog.accept)
    refresh_status()
    dialog.exec()
