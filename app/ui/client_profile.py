from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QFrame, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
from app.database import get_session
from app.models.invoice import Invoice, InvoiceItem
from app.models.debt import Debt
from sqlalchemy.orm import joinedload
from app.services.invoice_service import mark_paid, mark_unpaid
from app.i18n import t, translate_status
from app.ui.base_table import NoFocusDelegate

PROFILE_STYLE = """
    QDialog { background-color: #0f172a; color: #f1f5f9; }
    QLabel { color: #f1f5f9; border: none; }
    QTableWidget {
        background: #1e293b; color: #f1f5f9;
        border: 1px solid #334155; border-radius: 8px;
        gridline-color: #334155; font-size: 13px;
    }
    QTableWidget::item { padding: 6px; border: none; }
    QTableWidget::item:selected { background: #f59e0b; color: #1c1917; }
    QTableWidget::item:alternate { background: #1a2535; }
    QHeaderView::section {
        background: #1e293b; color: #f59e0b;
        padding: 8px; border: none; font-weight: bold;
        border-bottom: 2px solid #f59e0b;
    }
    QFrame#stat_card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
    }
    QPushButton#close_btn {
        background: #1e293b; color: #94a3b8;
        border: 1px solid #334155; border-radius: 6px;
        padding: 8px 24px; font-size: 13px;
    }
    QPushButton#close_btn:hover { background: #334155; }
    QPushButton#view_btn {
        background: #3b82f6; color: white; border: none;
        border-radius: 5px; padding: 5px 12px; font-size: 12px;
    }
    QPushButton#view_btn:hover { background: #2563eb; }
"""


class StatCard(QFrame):
    def __init__(self, label, value, color="#1abc9c"):
        super().__init__(objectName="stat_card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)
        lbl = QLabel(label)
        lbl.setStyleSheet("color: #94a3b8; font-size: 12px;")
        val = QLabel(value)
        val.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: bold;")
        layout.addWidget(lbl)
        layout.addWidget(val)
        self.val_label = val

    def update_value(self, value):
        self.val_label.setText(value)


class ClientProfileDialog(QDialog):
    def __init__(self, client, parent=None):
        super().__init__(parent)
        self.client = client
        self.setWindowTitle(f"Client — {client.name}")
        self.setMinimumSize(750, 560)
        self.setStyleSheet(PROFILE_STYLE)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(16)

        # --- Header ---
        header = QHBoxLayout()
        icon = QLabel("👤")
        icon.setStyleSheet("font-size: 32px;")
        info = QVBoxLayout()
        name_lbl = QLabel(client.name)
        name_lbl.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: #f59e0b;"
        )
        details = QLabel(
            f"📞 {client.phone or '—'}    "
            f"✉️ {client.email or '—'}    "
            f"📍 {client.address or '—'}"
        )
        details.setStyleSheet("color: #94a3b8; font-size: 12px;")
        info.addWidget(name_lbl)
        info.addWidget(details)
        header.addWidget(icon)
        header.addLayout(info)
        header.addStretch()
        layout.addLayout(header)

        # --- Stat cards ---
        self.invoices = self._load_invoices()
        self.debts = self._load_debts()

        total_spent = sum(inv.total for inv in self.invoices)
        total_debt = sum(
            max(0, d.amount_due - d.amount_paid) for d in self.debts
        )
        paid_count = sum(1 for inv in self.invoices if inv.status == "paid")
        unpaid_count = sum(
            1 for inv in self.invoices if inv.status == "unpaid"
        )

        cards_row = QHBoxLayout()
        cards_row.setSpacing(12)
        cards_row.addWidget(
            StatCard(t("profile.total_invoices"), str(len(self.invoices)))
        )
        cards_row.addWidget(
            StatCard(t("profile.total_spent"), f"{total_spent:,.0f} DA")
        )
        cards_row.addWidget(
            StatCard(t("profile.outstanding_debt"), f"{total_debt:,.0f} DA",
                     "#e74c3c" if total_debt > 0 else "#2ecc71")
        )
        cards_row.addWidget(
            StatCard(t("profile.paid_unpaid"), f"{paid_count} / {unpaid_count}",
                     "#2ecc71")
        )
        layout.addLayout(cards_row)

        # --- Invoices table ---
        section_lbl = QLabel(t("profile.invoice_history"))
        section_lbl.setStyleSheet(
            "font-size: 15px; font-weight: bold; color: #f1f5f9;"
        )
        layout.addWidget(section_lbl)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            [t("profile.col_id"), t("profile.col_date"), t("profile.col_total"),
             t("profile.col_status"), ""]
        )
        header_h = self.table.horizontalHeader()
        header_h.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header_h.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header_h.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header_h.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header_h.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(3, 90)
        self.table.setColumnWidth(4, 90)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.setItemDelegate(NoFocusDelegate(self.table))
        layout.addWidget(self.table)

        self._populate_table()

        # --- Bottom ---
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        close_btn = QPushButton(t("profile.close"))
        close_btn.setObjectName("close_btn")
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)

    def _load_invoices(self):
        session = get_session()
        return (
            session.query(Invoice)
            .options(
                joinedload(Invoice.items).joinedload(InvoiceItem.product)
            )
            .filter_by(client_id=self.client.id)
            .order_by(Invoice.date.desc())
            .all()
        )

    def _load_debts(self):
        session = get_session()
        return (
            session.query(Debt)
            .filter_by(client_id=self.client.id)
            .all()
        )

    def _populate_table(self):
        self.table.setRowCount(len(self.invoices))
        for r, inv in enumerate(self.invoices):
            status_color = "#2ecc71" if inv.status == "paid" else "#e74c3c"

            id_item = QTableWidgetItem(str(inv.id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            date_item = QTableWidgetItem(inv.date.strftime("%Y-%m-%d"))
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            total_item = QTableWidgetItem(f"{inv.total:,.2f}")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            status_item = QTableWidgetItem(translate_status(inv.status))
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setForeground(
                __import__('PyQt6.QtGui', fromlist=['QColor']).QColor(status_color)
            )

            self.table.setItem(r, 0, id_item)
            self.table.setItem(r, 1, date_item)
            self.table.setItem(r, 2, total_item)
            self.table.setItem(r, 3, status_item)

            view_btn = QPushButton(t("profile.view"))
            view_btn.setObjectName("view_btn")
            view_btn.clicked.connect(
                lambda _, i=inv: self.open_invoice_detail(i)
            )
            self.table.setCellWidget(r, 4, view_btn)

    def open_invoice_detail(self, invoice):
        dlg = InvoiceDetailDialog(invoice, parent=self)
        dlg.exec()


class InvoiceDetailDialog(QDialog):
    def __init__(self, invoice, parent=None):
        super().__init__(parent)
        self.invoice = invoice
        self.setWindowTitle(f"Invoice #{invoice.id}")
        self.setMinimumSize(580, 460)
        self.setStyleSheet(PROFILE_STYLE)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(14)

        # Header
        title = QLabel(f"🧾  Invoice #{invoice.id}")
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #f59e0b;"
        )
        layout.addWidget(title)

        meta_row = QHBoxLayout()
        meta_row.addWidget(
            self._meta_label(f"📅 {invoice.date.strftime('%Y-%m-%d')}")
        )
        meta_row.addWidget(
            self._meta_label(f"👤 {invoice.client.name}")
        )
        status_color = "#2ecc71" if invoice.status == "paid" else "#e74c3c"
        meta_row.addWidget(
            self._meta_label(
                f"● {translate_status(invoice.status)}", status_color
            )
        )
        meta_row.addStretch()
        layout.addLayout(meta_row)

        # Items table
        items_table = QTableWidget(0, 4)
        items_table.setHorizontalHeaderLabels(
            [t("inv_detail.col_product"), t("inv_detail.col_qty"),
             t("inv_detail.col_unit_price"), t("inv_detail.col_subtotal")]
        )
        h = items_table.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        h.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        h.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        h.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        items_table.setColumnWidth(1, 70)
        items_table.setColumnWidth(2, 120)
        items_table.setColumnWidth(3, 120)
        items_table.verticalHeader().setVisible(False)
        items_table.setAlternatingRowColors(True)
        items_table.setShowGrid(False)
        items_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        items_table.verticalHeader().setDefaultSectionSize(38)
        items_table.setItemDelegate(NoFocusDelegate(items_table))
        items_table.setRowCount(len(invoice.items))

        for r, item in enumerate(invoice.items):
            subtotal = item.qty * item.unit_price
            name = QTableWidgetItem(item.product.name)
            name.setToolTip(item.product.name)
            qty = QTableWidgetItem(str(int(item.qty)))
            qty.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            price = QTableWidgetItem(f"{item.unit_price:,.2f} DA")
            price.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            sub = QTableWidgetItem(f"{subtotal:,.2f} DA")
            sub.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            items_table.setItem(r, 0, name)
            items_table.setItem(r, 1, qty)
            items_table.setItem(r, 2, price)
            items_table.setItem(r, 3, sub)

        layout.addWidget(items_table)

        # Total
        total_lbl = QLabel(t("inv_detail.total", amount=f"{invoice.total:,.2f}"))
        total_lbl.setStyleSheet(
            "font-size: 17px; font-weight: bold; color: #f59e0b; "
            "padding: 6px 0;"
        )
        total_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(total_lbl)

        if invoice.notes:
            notes_lbl = QLabel(f"📝 Notes: {invoice.notes}")
            notes_lbl.setStyleSheet("color: #94a3b8; font-size: 12px;")
            layout.addWidget(notes_lbl)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.status_btn = QPushButton()
        self._refresh_status_btn()
        self.status_btn.clicked.connect(self.toggle_status)

        pdf_btn = QPushButton(t("inv_detail.print_pdf"))
        pdf_btn.setStyleSheet(
            "background:#3b82f6;color:white;border:none;border-radius:6px;"
            "padding:8px 20px;font-size:13px;font-weight:bold;"
        )
        pdf_btn.clicked.connect(self.print_pdf)

        close_btn = QPushButton(t("inv_detail.close"))
        close_btn.setObjectName("close_btn")
        close_btn.clicked.connect(self.accept)

        btn_row.addWidget(pdf_btn)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)

    def _meta_label(self, text, color="#7f8c8d"):
        lbl = QLabel(text)
        lbl.setStyleSheet(f"color: {color}; font-size: 13px; padding-right: 16px; background: transparent;")
        return lbl
    
    def _refresh_status_btn(self):
        if self.invoice.status == "unpaid":
            self.status_btn.setText(t("inv_detail.mark_paid"))
            self.status_btn.setStyleSheet(
                "background:#22c55e;color:white;border:none;"
                "border-radius:6px;padding:8px 20px;"
                "font-size:13px;font-weight:bold;"
            )
        else:
            self.status_btn.setText(t("inv_detail.mark_unpaid"))
            self.status_btn.setStyleSheet(
                "background:#e67e22;color:white;border:none;"
                "border-radius:6px;padding:8px 20px;"
                "font-size:13px;font-weight:bold;"
            )

    def toggle_status(self):
        if self.invoice.status == "unpaid":
            mark_paid(self.invoice.id)
            self.invoice.status = "paid"
        else:
            mark_unpaid(self.invoice.id)
            self.invoice.status = "unpaid"

        # Update status label color in header
        self._refresh_status_btn()

        # Refresh the status label in the dialog header
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if item and item.layout():
                inner = item.layout()
                for j in range(inner.count()):
                    w = inner.itemAt(j)
                    if w and w.widget() and isinstance(w.widget(), QLabel):
                        lbl = w.widget()
                        if any(kw in lbl.text() for kw in ["PAID", "UNPAID", "PAYÉE", "IMPAYÉE"]):
                            status_color = (
                                "#2ecc71" if self.invoice.status == "paid"
                                else "#e74c3c"
                            )
                            lbl.setText(f"● {translate_status(self.invoice.status)}")
                            lbl.setStyleSheet(
                                f"color: {status_color}; font-size: 13px; "
                                f"padding-right: 16px;"
                            )


    def print_pdf(self):
        from app.utils.pdf_generator import generate_invoice_pdf
        import os, sys
        saves_dir = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "saves")
        os.makedirs(saves_dir, exist_ok=True)
        date_str = self.invoice.date.strftime("%Y-%m-%d")
        filename = os.path.join(saves_dir, f"{date_str}_#{self.invoice.id}.pdf")
        path = generate_invoice_pdf(self.invoice, filename)
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            os.system(f"open {path}")
        else:
            os.system(f"xdg-open {path}")
