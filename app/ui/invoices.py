from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QDoubleSpinBox, QSpinBox, QMessageBox, QHeaderView, QWidget
)
from PyQt6.QtCore import Qt
from app.ui.base_table import BaseTableWidget, RowSelectFilter, NoFocusDelegate
from app.ui.product_picker import ProductPickerDialog
from app.services.invoice_service import get_all_invoices, create_invoice, mark_paid, InsufficientStockError
from app.services.client_service import get_all_clients
from app.services.product_service import get_all_products
from app.utils.pdf_generator import generate_invoice_pdf
from app.services.invoice_service import get_all_invoices, create_invoice, mark_paid, mark_unpaid, delete_invoice, InsufficientStockError
from app.i18n import t, translate_status
from app.ui.icons import qicon
import os, sys

DIALOG_STYLE = """
    QDialog { background-color: #1e293b; color: #f1f5f9; }
    QLabel { color: #f1f5f9; font-size: 13px; }
    QComboBox, QDoubleSpinBox, QSpinBox {
        background-color: #0f172a; color: #f1f5f9;
        border: 1px solid #334155; border-radius: 6px;
        padding: 6px 10px; font-size: 13px;
    }
    QComboBox::drop-down { border: none; background: #334155; width: 24px; }
    QComboBox QAbstractItemView { background: #1e293b; color: #f1f5f9; selection-background-color: #f59e0b; }
    QDoubleSpinBox::up-button, QDoubleSpinBox::down-button,
    QSpinBox::up-button, QSpinBox::down-button { background: #334155; border: none; width: 18px; }
    QTableWidget {
        background: #0f172a; color: #f1f5f9;
        border: 1px solid #334155; border-radius: 6px;
        gridline-color: #1e293b; font-size: 13px;
    }
    QHeaderView::section {
        background: #1e293b; color: #f59e0b;
        padding: 8px; border: none; font-weight: bold;
        border-bottom: 2px solid #f59e0b;
    }
    QPushButton#ok_btn {
        background: #f59e0b; color: white; border: none;
        border-radius: 6px; padding: 9px 28px; font-size: 13px; font-weight: bold;
    }
    QPushButton#ok_btn:hover { background: #d97706; }
    QPushButton#cancel_btn {
        background: #1e293b; color: #94a3b8; border: 1px solid #334155;
        border-radius: 6px; padding: 9px 28px; font-size: 13px;
    }
    QPushButton#add_item_btn {
        background: #3b82f6; color: white; border: none;
        border-radius: 6px; padding: 8px 16px; font-size: 13px;
    }
    QPushButton#add_item_btn:hover { background: #2563eb; }
"""

ACTION_BTN = """
    QPushButton {{
        background: {bg}; color: white; border: none;
        padding: 9px 18px; border-radius: 8px; font-size: 13px; font-weight: bold;
    }}
    QPushButton:hover {{ background: {hover}; }}
"""


class InvoicesWidget(BaseTableWidget):
    def __init__(self):
        super().__init__(t("invoices.title"),
                         [t("invoices.col_id"), t("invoices.col_client"), t("invoices.col_date"),
                          t("invoices.col_total"), t("invoices.col_status")])
        self.add_btn.setText(t("invoices.new"))
        self.add_btn.clicked.connect(self.open_add_dialog)

        top_layout = self.layout().itemAt(0).layout()

        self.pay_btn = QPushButton(t("invoices.mark_paid"))
        self.pay_btn.setIcon(qicon("mark_paid", "white"))
        self.pay_btn.setStyleSheet(ACTION_BTN.format(bg="#22c55e", hover="#16a34a"))
        self.pay_btn.clicked.connect(self.toggle_payment_status)
        top_layout.insertWidget(top_layout.count() - 1, self.pay_btn)


        self.pdf_btn = QPushButton(t("invoices.print_pdf"))
        self.pdf_btn.setIcon(qicon("pdf", "white"))
        self.pdf_btn.setStyleSheet(ACTION_BTN.format(bg="#3b82f6", hover="#2563eb"))
        self.pdf_btn.clicked.connect(self.print_pdf)
        top_layout.insertWidget(top_layout.count() - 1, self.pdf_btn)
        self.table.cellDoubleClicked.connect(self.open_invoice_detail)

        self.delete_btn = QPushButton(t("invoices.delete"))
        self.delete_btn.setIcon(qicon("trash", "white"))
        self.delete_btn.setStyleSheet(ACTION_BTN.format(bg="#ef4444", hover="#dc2626"))
        self.delete_btn.clicked.connect(self.delete_selected)
        top_layout.insertWidget(top_layout.count() - 1, self.delete_btn)

        self.set_sortable_columns([
            (t("invoices.col_total"), 3),
        ])

        self.refresh()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)    # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Client — stretches
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)    # Date
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)    # Total (DA)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)    # Status
        self.table.setColumnWidth(0, 50)    # ID
        self.table.setColumnWidth(2, 110)   # Date
        self.table.setColumnWidth(3, 120)   # Total (DA)
        self.table.setColumnWidth(4, 100)   # Status
        self.table.selectionModel().selectionChanged.connect(
            lambda: self._update_pay_btn()
        )

    def refresh(self):
        self.invoices = get_all_invoices()
        rows = [(inv.id, inv.client.name, inv.date.strftime("%Y-%m-%d"),
                 f"{inv.total:.2f}", translate_status(inv.status)) for inv in self.invoices]
        self.populate(rows)
        self._update_pay_btn()

    def open_invoice_detail(self, row, col):
        inv_id = int(self.table.item(row, 0).text())
        inv = next((i for i in self.invoices if i.id == inv_id), None)
        if inv:
            from app.ui.client_profile import InvoiceDetailDialog
            dlg = InvoiceDetailDialog(inv, parent=self)
            dlg.exec()

    def get_selected_invoice(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t("common.warning"), t("invoices.select_first"))
            return None
        inv_id = int(self.table.item(row, 0).text())
        return next((i for i in self.invoices if i.id == inv_id), None)

    def toggle_payment_status(self):
        inv = self.get_selected_invoice()
        if not inv:
            return
        if inv.status == "unpaid":
            mark_paid(inv.id)
        else:
            mark_unpaid(inv.id)
        self.refresh()

    def _update_pay_btn(self):
        row = self.table.currentRow()
        if row < 0:
            self.pay_btn.setIcon(qicon("mark_paid", "white"))
            self.pay_btn.setText(t("invoices.mark_paid"))
            self.pay_btn.setStyleSheet(
                ACTION_BTN.format(bg="#22c55e", hover="#16a34a")
            )
            return
        inv_id = int(self.table.item(row, 0).text())
        inv = next((i for i in self.invoices if i.id == inv_id), None)
        if inv and inv.status == "paid":
            self.pay_btn.setIcon(qicon("mark_unpaid", "white"))
            self.pay_btn.setText(t("invoices.mark_unpaid"))
            self.pay_btn.setStyleSheet(
                ACTION_BTN.format(bg="#e67e22", hover="#ca6f1e")
            )
        else:
            self.pay_btn.setIcon(qicon("mark_paid", "white"))
            self.pay_btn.setText(t("invoices.mark_paid"))
            self.pay_btn.setStyleSheet(
                ACTION_BTN.format(bg="#22c55e", hover="#16a34a")
            )

    def print_pdf(self):
        inv = self.get_selected_invoice()
        if inv:
            saves_dir = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "saves")
            os.makedirs(saves_dir, exist_ok=True)
            date_str = inv.date.strftime("%Y-%m-%d")
            filename = os.path.join(saves_dir, f"{date_str}_#{inv.id}.pdf")
            path = generate_invoice_pdf(inv, filename)
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                os.system(f"open {path}")
            else:
                os.system(f"xdg-open {path}")

    def open_add_dialog(self):
        dlg = NewInvoiceDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.refresh()

    def delete_selected(self):
        inv = self.get_selected_invoice()
        if not inv:
            return
        reply = QMessageBox.question(
            self, t("common.confirm_delete"),
            t("invoices.del_confirm", id=inv.id, client=inv.client.name, total=f"{inv.total:,.2f}"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            delete_invoice(inv.id)
            self.refresh()        

class NewInvoiceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("invoices.new_win"))
        self.setMinimumWidth(680)
        self.setMinimumHeight(520)
        self.setStyleSheet(DIALOG_STYLE)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        self.clients = get_all_clients()
        self.products = get_all_products()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(12)

        title = QLabel(t("invoices.new_title"))
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #f59e0b;")
        layout.addWidget(title)

        # Client selector
        client_row = QHBoxLayout()
        client_row.addWidget(QLabel(t("invoices.client")))
        self.client_combo = QComboBox()
        for c in self.clients:
            self.client_combo.addItem(c.name, c.id)
        client_row.addWidget(self.client_combo)
        client_row.addStretch()
        layout.addLayout(client_row)

        # Items table
        self.item_table = QTableWidget(0, 6)
        self.item_table.setHorizontalHeaderLabels(
            [t("invoices.col_product"), t("invoices.col_available"), t("invoices.col_qty"),
             t("invoices.col_unit_price"), t("invoices.col_subtotal"), ""]
        )
        header = self.item_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.item_table.setColumnWidth(1, 80)
        self.item_table.setColumnWidth(2, 70)
        self.item_table.setColumnWidth(3, 110)
        self.item_table.setColumnWidth(4, 100)
        self.item_table.setColumnWidth(5, 44)
        self.item_table.verticalHeader().setVisible(False)
        self.item_table.setShowGrid(False)
        self.item_table.setAlternatingRowColors(True)
        self.item_table.setItemDelegate(NoFocusDelegate(self.item_table))
        layout.addWidget(self.item_table)

        # ✅ Created ONCE here
        self._row_filter = RowSelectFilter(self.item_table)

        add_item_btn = QPushButton(t("invoices.add_item"))
        add_item_btn.setObjectName("add_item_btn")
        add_item_btn.clicked.connect(self.add_item_row)
        layout.addWidget(add_item_btn)

        self.total_label = QLabel(t("invoices.total", amount="0.00"))
        self.total_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #f59e0b;"
        )
        layout.addWidget(self.total_label)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton(t("invoices.cancel"))
        cancel_btn.setObjectName("cancel_btn")
        cancel_btn.clicked.connect(self.reject)
        ok_btn = QPushButton(t("invoices.save"))
        ok_btn.setObjectName("ok_btn")
        ok_btn.clicked.connect(self.save)
        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(ok_btn)
        layout.addLayout(btn_row)

    def add_item_row(self):
        row = self.item_table.rowCount()
        self.item_table.insertRow(row)

        name_lbl = QLabel(t("invoices.pick_product"))
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        name_lbl.setStyleSheet(
            "color: #64748b; font-size: 12px; border: none; padding-left: 8px;"
        )
        name_lbl.setCursor(Qt.CursorShape.PointingHandCursor)
        name_lbl.mousePressEvent = lambda e, r=row: self.open_product_picker(r)

        available_lbl = QLabel("—")
        available_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        available_lbl.setStyleSheet("color: #f59e0b; font-weight: bold; border: none;")

        qty = QSpinBox()
        qty.setMinimum(1)
        qty.setMaximum(9999)
        qty.setStyleSheet(
            "background:#0f172a;color:#f1f5f9;border:1px solid #334155;"
            "border-radius:6px;padding:6px 10px;font-size:13px;"
        )

        price = QDoubleSpinBox()
        price.setMinimum(0)
        price.setMaximum(999999)
        price.setDecimals(2)
        price.setStyleSheet(
            "background:#0f172a;color:#f1f5f9;border:1px solid #334155;"
            "border-radius:6px;padding:6px 10px;font-size:13px;"
        )

        qty.valueChanged.connect(lambda _: self._update_row_stock(row))
        qty.valueChanged.connect(lambda _: self.update_total())
        price.valueChanged.connect(lambda _: self.update_total())

        self.item_table.setItem(row, 4, QTableWidgetItem("0.00"))

        for col_idx, w in enumerate([name_lbl, available_lbl, qty, price]):
            w.installEventFilter(self._row_filter)
            for child in w.findChildren(QWidget):
                child.installEventFilter(self._row_filter)
            self.item_table.setCellWidget(row, col_idx, w)

        # Auto-open picker immediately
        self.open_product_picker(row)
                # Delete row button
        del_btn = QPushButton()
        del_btn.setIcon(qicon("delete_row", "white"))
        del_btn.setFixedSize(32, 32)
        del_btn.setStyleSheet("""
            QPushButton {
                background: #ef4444; color: white; border: none;
                border-radius: 6px; font-size: 14px;
            }
            QPushButton:hover { background: #dc2626; }
        """)
        del_btn.clicked.connect(lambda _, r=row: self.delete_row(r))
        del_btn.installEventFilter(self._row_filter)
        self.item_table.setCellWidget(row, 5, del_btn)


    def open_product_picker(self, row):
        dlg = ProductPickerDialog(self.products, parent=self)
        dlg.product_selected.connect(
            lambda product, r=row: self.set_row_product(r, product)
        )
        dlg.exec()

    def set_row_product(self, row, product):
        name_lbl = self.item_table.cellWidget(row, 0)
        available_lbl = self.item_table.cellWidget(row, 1)
        price_widget = self.item_table.cellWidget(row, 3)

        if name_lbl:
            name_lbl.setText(product.name)
            name_lbl.setToolTip(product.name)
            name_lbl.setStyleSheet(
                "color: #f1f5f9; font-size: 12px; font-weight: bold; "
                "border: none; padding-left: 8px;"
            )
            name_lbl.setProperty("product_id", product.id)

        if available_lbl:
            available_lbl.setText(f"{int(product.stock_qty)}")

        if price_widget:
            price_widget.setValue(product.price)

        self.update_total()

    def _update_row_stock(self, row):
        available_lbl = self.item_table.cellWidget(row, 1)
        qty_widget = self.item_table.cellWidget(row, 2)
        if not available_lbl or not qty_widget:
            return
        try:
            available = int(available_lbl.text())
            if qty_widget.value() > available:
                available_lbl.setStyleSheet(
                    "color: #e74c3c; font-weight: bold; border: none;"
                )
                qty_widget.setStyleSheet(
                    "border:1px solid #e74c3c;background:#0f172a;"
                    "color:#f1f5f9;border-radius:6px;padding:6px 10px;"
                )
            else:
                available_lbl.setStyleSheet(
                    "color: #f59e0b; font-weight: bold; border: none;"
                )
                qty_widget.setStyleSheet(
                    "background:#0f172a;color:#f1f5f9;border:1px solid #334155;"
                    "border-radius:6px;padding:6px 10px;font-size:13px;"
                )
        except ValueError:
            pass

    def update_total(self):
        total = 0
        for r in range(self.item_table.rowCount()):
            qty = self.item_table.cellWidget(r, 2)
            price = self.item_table.cellWidget(r, 3)
            if qty and price:
                sub = qty.value() * price.value()
                self.item_table.setItem(r, 4, QTableWidgetItem(f"{sub:.2f}"))
                total += sub
        self.total_label.setText(t("invoices.total", amount=f"{total:.2f}"))

    def save(self):
        client_id = self.client_combo.currentData()
        items = []
        for r in range(self.item_table.rowCount()):
            name_lbl = self.item_table.cellWidget(r, 0)
            qty = self.item_table.cellWidget(r, 2)
            price = self.item_table.cellWidget(r, 3)
            if name_lbl and qty and price:
                product_id = name_lbl.property("product_id")
                if not product_id:
                    QMessageBox.warning(
                        self, t("common.error"),
                        t("invoices.no_product", row=r+1)
                    )
                    return
                items.append({
                    "product_id": product_id,
                    "qty": qty.value(),
                    "unit_price": price.value()
                })

        if not items:
            QMessageBox.warning(self, t("common.error"), t("invoices.min_item"))
            return

        try:
            create_invoice(client_id, items)
            self.accept()
        except InsufficientStockError as e:
            QMessageBox.critical(
                self, t("invoices.insuff_title"),
                t("invoices.insuff_stock",
                  product=e.product_name,
                  available=e.available,
                  requested=e.requested)
            )
        except Exception as e:
            QMessageBox.critical(self, t("common.error"), str(e))

    def delete_row(self, row):
        # Find actual current row since indices shift after deletion
        for r in range(self.item_table.rowCount()):
            del_btn = self.item_table.cellWidget(r, 5)
            name_lbl = self.item_table.cellWidget(r, 0)
            # Match by button identity
            if del_btn and del_btn is self.item_table.cellWidget(r, 5):
                # Check if this is the row the button belongs to
                pass

        self.item_table.removeRow(row)
        self.update_total()

        # Re-wire delete buttons after row removal so indices stay correct
        for r in range(self.item_table.rowCount()):
            del_btn = self.item_table.cellWidget(r, 5)
            if del_btn:
                try:
                    del_btn.clicked.disconnect()
                except Exception:
                    pass
                del_btn.clicked.connect(lambda _, rr=r: self.delete_row(rr))
