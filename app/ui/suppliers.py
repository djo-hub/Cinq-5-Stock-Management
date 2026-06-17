from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QLabel, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView
from app.ui.base_table import BaseTableWidget
from app.services.supplier_service import (
    get_all_suppliers, add_supplier, update_supplier, delete_supplier
)
from app.i18n import t
from app.ui.icons import qicon

DIALOG_STYLE = """
    QDialog { background-color: #1e293b; color: #f1f5f9; }
    QLabel  { color: #f1f5f9; font-size: 13px; font-weight: bold; min-width: 130px; }
    QLineEdit, QTextEdit {
        background-color: #0f172a; color: #f1f5f9;
        border: 1px solid #334155; border-radius: 6px;
        padding: 7px 10px; font-size: 13px; min-width: 220px;
    }
    QLineEdit:focus, QTextEdit:focus { border: 1px solid #f59e0b; }
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


class SupplierDialog(QDialog):
    def __init__(self, parent=None, supplier=None):
        super().__init__(parent)
        self.supplier = supplier
        is_edit = supplier is not None
        self.setWindowTitle(t("suppliers.edit_win") if is_edit else t("suppliers.add_win"))
        self.setMinimumWidth(460)
        self.setStyleSheet(DIALOG_STYLE)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 20)
        layout.setSpacing(10)

        title = QLabel(t("suppliers.edit_title") if is_edit else t("suppliers.add_title"))
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #f59e0b; margin-bottom: 10px;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.name_input    = QLineEdit(); self.name_input.setPlaceholderText("Company name")
        self.contact_input = QLineEdit(); self.contact_input.setPlaceholderText("Contact person name")
        self.phone_input   = QLineEdit(); self.phone_input.setPlaceholderText("+213 XX XX XX XX")
        self.email_input   = QLineEdit(); self.email_input.setPlaceholderText("supplier@example.com")
        self.address_input = QLineEdit(); self.address_input.setPlaceholderText("City, Country")
        self.notes_input   = QTextEdit(); self.notes_input.setPlaceholderText("Optional notes...")
        self.notes_input.setFixedHeight(70)

        if is_edit:
            self.name_input.setText(supplier.name)
            self.contact_input.setText(supplier.contact_person)
            self.phone_input.setText(supplier.phone)
            self.email_input.setText(supplier.email)
            self.address_input.setText(supplier.address)
            self.notes_input.setPlainText(supplier.notes)

        form.addRow(t("suppliers.company"),    self.name_input)
        form.addRow(t("suppliers.contact"),  self.contact_input)
        form.addRow(t("suppliers.phone"),           self.phone_input)
        form.addRow(t("suppliers.email"),           self.email_input)
        form.addRow(t("suppliers.address"),         self.address_input)
        form.addRow(t("suppliers.notes"),           self.notes_input)
        layout.addLayout(form)
        layout.addSpacing(16)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton(t("suppliers.cancel")); cancel_btn.setObjectName("cancel_btn")
        cancel_btn.clicked.connect(self.reject)
        ok_btn = QPushButton(t("suppliers.update") if is_edit else t("suppliers.save"))
        ok_btn.setObjectName("ok_btn")
        ok_btn.clicked.connect(self._validate_and_accept)
        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(ok_btn)
        layout.addLayout(btn_row)

    def _validate_and_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, t("common.validation"), t("suppliers.name_req"))
            self.name_input.setFocus()
            return
        self.accept()

    def get_data(self):
        return {
            "name":           self.name_input.text().strip(),
            "contact_person": self.contact_input.text().strip(),
            "phone":          self.phone_input.text().strip(),
            "email":          self.email_input.text().strip(),
            "address":        self.address_input.text().strip(),
            "notes":          self.notes_input.toPlainText().strip(),
        }


class SuppliersWidget(BaseTableWidget):
    def __init__(self):
        super().__init__(t("suppliers.title"),
                         [t("suppliers.col_id"), t("suppliers.col_company"), t("suppliers.col_contact"),
                          t("suppliers.col_phone"), t("suppliers.col_email"), t("suppliers.col_products")])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(2, 140)
        self.table.setColumnWidth(3, 130)
        self.table.setColumnWidth(5, 80)

        top_layout = self.layout().itemAt(0).layout()

        self.edit_btn = QPushButton(t("suppliers.edit"))
        self.edit_btn.setIcon(qicon("pencil", "white"))
        self.edit_btn.setStyleSheet(ACTION_BTN.format(bg="#3b82f6", hover="#2563eb"))
        self.edit_btn.clicked.connect(self.edit_selected)
        top_layout.insertWidget(top_layout.count() - 1, self.edit_btn)

        self.delete_btn = QPushButton(t("suppliers.delete"))
        self.delete_btn.setIcon(qicon("trash", "white"))
        self.delete_btn.setStyleSheet(ACTION_BTN.format(bg="#ef4444", hover="#dc2626"))
        self.delete_btn.clicked.connect(self.delete_selected)
        top_layout.insertWidget(top_layout.count() - 1, self.delete_btn)

        self.set_sortable_columns([
            (t("suppliers.col_products"), 5),
        ])

        self.add_btn.clicked.connect(self.open_add_dialog)
        self.table.cellDoubleClicked.connect(self._open_profile)
        self.refresh()

    def refresh(self):
        self.suppliers = get_all_suppliers()
        rows = [(s.id, s.name, s.contact_person, s.phone,
                 s.email, len(s.products)) for s in self.suppliers]
        self.populate(rows)

    def _get_selected(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t("common.warning"), t("suppliers.select_first"))
            return None
        sid = int(self.table.item(row, 0).text())
        return next((s for s in self.suppliers if s.id == sid), None)

    def _open_profile(self, row, col):
        sid = int(self.table.item(row, 0).text())
        supplier = next((s for s in self.suppliers if s.id == sid), None)
        if supplier:
            from app.ui.supplier_profile import SupplierProfileDialog
            dlg = SupplierProfileDialog(supplier, parent=self)
            dlg.exec()

    def open_add_dialog(self):
        dlg = SupplierDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            d = dlg.get_data()
            add_supplier(**d)
            self.refresh()

    def edit_selected(self):
        supplier = self._get_selected()
        if not supplier:
            return
        dlg = SupplierDialog(self, supplier=supplier)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            update_supplier(supplier.id, **dlg.get_data())
            self.refresh()

    def delete_selected(self):
        supplier = self._get_selected()
        if not supplier:
            return
        product_count = len(supplier.products)
        msg = t("suppliers.del_confirm", name=supplier.name)
        if product_count:
            msg += t("suppliers.del_unlink", count=product_count)
        reply = QMessageBox.question(self, t("common.confirm_delete"), msg,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            delete_supplier(supplier.id)
            self.refresh()
