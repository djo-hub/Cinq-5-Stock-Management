from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QVBoxLayout,
    QHBoxLayout, QPushButton, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt
from app.ui.base_table import BaseTableWidget
from app.services.client_service import get_all_clients, add_client, delete_client, update_client
from PyQt6.QtWidgets import QHeaderView
from app.i18n import t
from app.ui.icons import qicon

DIALOG_STYLE = """
    QDialog { background-color: #1e293b; color: #f1f5f9; }
    QLabel { color: #f1f5f9; font-size: 13px; font-weight: bold; min-width: 110px; }
    QLineEdit {
        background-color: #0f172a; color: #f1f5f9;
        border: 1px solid #334155; border-radius: 6px;
        padding: 7px 10px; font-size: 13px; min-width: 200px;
    }
    QLineEdit:focus { border: 1px solid #f59e0b; }
    QPushButton#ok_btn {
        background-color: #f59e0b; color: white; border: none;
        border-radius: 6px; padding: 9px 28px; font-size: 13px; font-weight: bold;
    }
    QPushButton#ok_btn:hover { background-color: #d97706; }
    QPushButton#cancel_btn {
        background-color: #1e293b; color: #94a3b8; border: 1px solid #334155;
        border-radius: 6px; padding: 9px 28px; font-size: 13px;
    }
    QPushButton#cancel_btn:hover { background-color: #334155; }
"""

ACTION_BTN = """
    QPushButton {{
        background: {bg}; color: white; border: none;
        padding: 9px 18px; border-radius: 8px; font-size: 13px; font-weight: bold;
    }}
    QPushButton:hover {{ background: {hover}; }}
"""


class ClientDialog(QDialog):
    def __init__(self, parent=None, client=None):
        super().__init__(parent)
        self.client = client
        is_edit = client is not None
        self.setWindowTitle(t("clients.edit_win") if is_edit else t("clients.add_win"))
        self.setMinimumWidth(420)
        self.setStyleSheet(DIALOG_STYLE)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 20)
        layout.setSpacing(10)

        title = QLabel(t("clients.edit_title") if is_edit else t("clients.add_title"))
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #f59e0b; margin-bottom: 10px;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.name_input = QLineEdit(); self.name_input.setPlaceholderText("Full name")
        self.phone_input = QLineEdit(); self.phone_input.setPlaceholderText("+213 XX XX XX XX")
        self.email_input = QLineEdit(); self.email_input.setPlaceholderText("email@example.com")
        self.address_input = QLineEdit(); self.address_input.setPlaceholderText("Address")

        # Pre-fill if editing
        if is_edit:
            self.name_input.setText(client.name)
            self.phone_input.setText(client.phone)
            self.email_input.setText(client.email)
            self.address_input.setText(client.address)

        form.addRow(t("clients.name"), self.name_input)
        form.addRow(t("clients.phone"), self.phone_input)
        form.addRow(t("clients.email"), self.email_input)
        form.addRow(t("clients.address"), self.address_input)
        layout.addLayout(form)
        layout.addSpacing(16)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton(t("clients.cancel")); cancel_btn.setObjectName("cancel_btn")
        cancel_btn.clicked.connect(self.reject)
        ok_btn = QPushButton(t("clients.update") if is_edit else t("clients.save"))
        ok_btn.setObjectName("ok_btn")
        ok_btn.clicked.connect(self.validate_and_accept)
        btn_row.addWidget(cancel_btn); btn_row.addWidget(ok_btn)
        layout.addLayout(btn_row)

    def validate_and_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, t("common.validation"), t("clients.name_req"))
            self.name_input.setFocus()
            return
        self.accept()

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "email": self.email_input.text().strip(),
            "address": self.address_input.text().strip(),
        }


class ClientsWidget(BaseTableWidget):
    def __init__(self):
        super().__init__(t("clients.title"),
                         [t("clients.col_id"), t("clients.col_name"), t("clients.col_phone"),
                          t("clients.col_email"), t("clients.col_address")])

        top_layout = self.layout().itemAt(0).layout()

        self.edit_btn = QPushButton(t("clients.edit"))
        self.edit_btn.setIcon(qicon("pencil", "white"))
        self.edit_btn.setStyleSheet(ACTION_BTN.format(bg="#3b82f6", hover="#2563eb"))
        self.edit_btn.clicked.connect(self.edit_selected)
        top_layout.insertWidget(top_layout.count() - 1, self.edit_btn)

        self.delete_btn = QPushButton(t("clients.delete"))
        self.delete_btn.setIcon(qicon("trash", "white"))
        self.delete_btn.setStyleSheet(ACTION_BTN.format(bg="#ef4444", hover="#dc2626"))
        self.delete_btn.clicked.connect(self.delete_selected)
        top_layout.insertWidget(top_layout.count() - 1, self.delete_btn)

        self.add_btn.clicked.connect(self.open_add_dialog)
        self.refresh()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(2, 120)
        self.table.cellDoubleClicked.connect(self.open_client_profile)


    def refresh(self):
        self.clients = get_all_clients()
        rows = [(c.id, c.name, c.phone, c.email, c.address) for c in self.clients]
        self.populate(rows)
    
    def open_client_profile(self, row, col):
        client_id = int(self.table.item(row, 0).text())
        client = next((c for c in self.clients if c.id == client_id), None)
        if client:
            from app.ui.client_profile import ClientProfileDialog
            dlg = ClientProfileDialog(client, parent=self)
            dlg.exec()

    def get_selected_client(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t("common.warning"), t("clients.select_first"))
            return None
        client_id = int(self.table.item(row, 0).text())
        return next((c for c in self.clients if c.id == client_id), None)

    def open_add_dialog(self):
        dlg = ClientDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            add_client(data["name"], data["phone"], data["email"], data["address"])
            self.refresh()

    def edit_selected(self):
        client = self.get_selected_client()
        if not client:
            return
        dlg = ClientDialog(self, client=client)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            update_client(client.id,
                          name=data["name"],
                          phone=data["phone"],
                          email=data["email"],
                          address=data["address"])
            self.refresh()

    def delete_selected(self):
        client = self.get_selected_client()
        if not client:
            return
        reply = QMessageBox.question(self, t("common.confirm_delete"),
                                     t("clients.del_confirm", name=client.name),
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            delete_client(client.id)
            self.refresh()
