from PyQt6.QtWidgets import QDialog, QFormLayout, QDoubleSpinBox, QDialogButtonBox, QPushButton, QMessageBox
from app.ui.base_table import BaseTableWidget
from app.services.debt_service import get_all_debts, record_payment
from PyQt6.QtWidgets import QHeaderView
from app.i18n import t, translate_status
from app.ui.icons import qicon

class DebtsWidget(BaseTableWidget):
    def __init__(self):
        super().__init__(t("debts.title"),
                         [t("debts.col_id"), t("debts.col_client"), t("debts.col_due"),
                          t("debts.col_paid"), t("debts.col_remaining"), t("debts.col_status")])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)      # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)    # Client — stretches
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)      # Due
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)      # Paid
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)      # Remaining
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)      # Status
        self.table.setColumnWidth(0, 50)    # ID
        self.table.setColumnWidth(2, 110)   # Due
        self.table.setColumnWidth(3, 110)   # Paid
        self.table.setColumnWidth(4, 110)   # Remaining
        self.table.setColumnWidth(5, 100)   # Status

        self.set_sortable_columns([
            (t("debts.col_due"), 2),
            (t("debts.col_paid"), 3),
            (t("debts.col_remaining"), 4),
        ])

        self.add_btn.setText(t("debts.record_payment"))
        self.add_btn.setIcon(qicon("cash_plus", "white"))
        self.add_btn.clicked.connect(self.open_payment_dialog)
        self.refresh()

    def refresh(self):
        self.debts = get_all_debts()
        rows = [(d.id, d.client.name, f"{d.amount_due:.2f}",
                 f"{d.amount_paid:.2f}", f"{d.amount_due - d.amount_paid:.2f}", translate_status(d.status))
                for d in self.debts]
        self.populate(rows)

    def open_payment_dialog(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t("common.warning"), t("debts.select_first"))
            return
        debt_id = int(self.table.item(row, 0).text())
        dlg = QDialog(self)
        dlg.setWindowTitle(t("debts.pay_title"))
        form = QFormLayout(dlg)
        amount = QDoubleSpinBox(); amount.setMaximum(999999); amount.setDecimals(2)
        form.addRow(t("debts.pay_amount"), amount)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dlg.accept); buttons.rejected.connect(dlg.reject)
        form.addRow(buttons)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            record_payment(debt_id, amount.value())
            self.refresh()
