from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QSpinBox, QLabel, QComboBox,
    QListWidget, QListWidgetItem, QDoubleSpinBox
)
from PyQt6.QtCore import Qt
from app.ui.base_table import BaseTableWidget
from app.services.product_service import get_all_products, add_product, delete_product, update_product
from app.services.category_service import get_category_names, add_category, delete_category
from app.i18n import t
from app.ui.icons import qicon

DIALOG_STYLE = """
    QDialog { background-color: #1e293b; color: #f1f5f9; }
    QLabel { color: #f1f5f9; font-size: 13px; font-weight: bold; min-width: 110px; }
    QLineEdit, QSpinBox, QComboBox {
        background-color: #0f172a; color: #f1f5f9;
        border: 1px solid #334155; border-radius: 6px;
        padding: 7px 10px; font-size: 13px; min-width: 200px;
    }
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus { border: 1px solid #f59e0b; }
    QComboBox::drop-down { border: none; background: #334155; width: 24px; border-radius: 0 6px 6px 0; }
    QComboBox QAbstractItemView { background: #1e293b; color: #f1f5f9; selection-background-color: #f59e0b; }
    QSpinBox::up-button, QSpinBox::down-button { background-color: #334155; border: none; width: 18px; }
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
    QPushButton#add_cat_btn {
        background-color: #3b82f6; color: white; border: none;
        border-radius: 6px; padding: 6px 14px; font-size: 12px;
    }
    QPushButton#add_cat_btn:hover { background-color: #2563eb; }
    QPushButton#del_cat_btn {
        background-color: #ef4444; color: white; border: none;
        border-radius: 6px; padding: 6px 14px; font-size: 12px;
    }
    QPushButton#del_cat_btn:hover { background-color: #dc2626; }
    QListWidget {
        background: #0f172a; color: #f1f5f9; border: 1px solid #334155;
        border-radius: 6px; font-size: 13px;
    }
    QListWidget::item:selected { background: #f59e0b; color: white; }
"""

ACTION_BTN = """
    QPushButton {{
        background: {bg}; color: white; border: none;
        padding: 9px 18px; border-radius: 8px; font-size: 13px; font-weight: bold;
    }}
    QPushButton:hover {{ background: {hover}; }}
"""


class ManageCategoriesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("cat.win_title"))
        self.setMinimumWidth(360)
        self.setMinimumHeight(400)
        self.setStyleSheet(DIALOG_STYLE)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(12)

        title = QLabel(t("cat.title"))
        title.setStyleSheet("font-size: 17px; font-weight: bold; color: #f59e0b; margin-bottom: 6px;")
        layout.addWidget(title)

        row = QHBoxLayout()
        self.cat_input = QLineEdit()
        self.cat_input.setPlaceholderText(t("cat.placeholder"))
        self.cat_input.returnPressed.connect(self.add_cat)
        row.addWidget(self.cat_input)
        add_btn = QPushButton(t("cat.add"))
        add_btn.setObjectName("add_cat_btn")
        add_btn.clicked.connect(self.add_cat)
        row.addWidget(add_btn)
        layout.addLayout(row)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        del_btn = QPushButton(t("cat.delete"))
        del_btn.setObjectName("del_cat_btn")
        del_btn.clicked.connect(self.delete_cat)
        layout.addWidget(del_btn)

        close_btn = QPushButton(t("cat.close"))
        close_btn.setObjectName("cancel_btn")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.load_categories()

    def load_categories(self):
        self.list_widget.clear()
        for name in get_category_names():
            self.list_widget.addItem(QListWidgetItem(name))

    def add_cat(self):
        name = self.cat_input.text().strip()
        if not name:
            return
        add_category(name)
        self.cat_input.clear()
        self.load_categories()

    def delete_cat(self):
        item = self.list_widget.currentItem()
        if not item:
            QMessageBox.warning(self, t("common.warning"), t("cat.select_warn"))
            return
        reply = QMessageBox.question(self, t("common.confirm"), t("cat.del_confirm", name=item.text()),
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            delete_category(item.text())
            self.load_categories()


class ProductDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.product = product
        is_edit = product is not None
        self.setWindowTitle(t("products.edit_win") if is_edit else t("products.add_win"))
        self.setMinimumWidth(440)
        self.setStyleSheet(DIALOG_STYLE)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 20)
        layout.setSpacing(10)

        title = QLabel(t("products.edit_title") if is_edit else t("products.add_title"))
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #f59e0b; margin-bottom: 10px;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Laptop")

        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("e.g. 6191234567890")

        cat_row = QHBoxLayout()
        self.category_combo = QComboBox()
        self.reload_categories()
        cat_row.addWidget(self.category_combo)
        manage_btn = QPushButton()
        manage_btn.setIcon(qicon("gear", "#f1f5f9"))
        manage_btn.setObjectName("add_cat_btn")
        manage_btn.setFixedWidth(36)
        manage_btn.setToolTip(t("cat.win_title"))
        manage_btn.clicked.connect(self.open_manage_categories)
        cat_row.addWidget(manage_btn)

        # ✅ QSpinBox for integer price — use QLineEdit with validator for decimals
        self.price_input = QDoubleSpinBox()
        self.price_input.setMaximum(9999999)
        self.price_input.setDecimals(2)
        self.price_input.setSuffix("  DA")
        self.price_input.setStyleSheet(
            "background:#0f172a;color:#f1f5f9;border:1px solid #334155;"
            "border-radius:6px;padding:7px 10px;font-size:13px;min-width:200px;"
        )

        # Cost price (supplier purchase price)
        self.cost_price_input = QDoubleSpinBox()
        self.cost_price_input.setMaximum(9999999)
        self.cost_price_input.setDecimals(2)
        self.cost_price_input.setSuffix("  DA")
        self.cost_price_input.setStyleSheet(
            "background:#0f172a;color:#f1f5f9;border:1px solid #334155;"
            "border-radius:6px;padding:7px 10px;font-size:13px;min-width:200px;"
        )

        # ✅ QSpinBox (integer) for stock
        self.qty_input = QSpinBox()
        self.qty_input.setMaximum(9999999)
        self.qty_input.setMinimum(0)

        self.unit_input = QLineEdit()
        self.unit_input.setText("pcs")

        # Supplier combo
        from app.services.supplier_service import get_all_suppliers
        self.supplier_combo = QComboBox()
        self.supplier_combo.addItem(t("products.none_supplier"), None)
        self._suppliers = get_all_suppliers()
        for s in self._suppliers:
            self.supplier_combo.addItem(s.name, s.id)

        if is_edit:
            self.name_input.setText(product.name)
            self.barcode_input.setText(product.barcode or "")
            if product.category in get_category_names():
                self.category_combo.setCurrentText(product.category)
            self.price_input.setValue(product.price)
            self.cost_price_input.setValue(product.cost_price or 0.0)
            self.qty_input.setValue(int(product.stock_qty))
            self.unit_input.setText(product.unit)
            # Pre-select supplier
            if product.supplier_id:
                idx = self.supplier_combo.findData(product.supplier_id)
                if idx >= 0:
                    self.supplier_combo.setCurrentIndex(idx)

        form.addRow(t("products.name"), self.name_input)
        form.addRow(t("products.barcode"), self.barcode_input)
        form.addRow(t("products.category"), cat_row)
        form.addRow(t("products.supplier"), self.supplier_combo)
        form.addRow(t("products.price"), self.price_input)
        form.addRow(t("products.cost_price"), self.cost_price_input)
        form.addRow(t("products.stock_qty"), self.qty_input)
        form.addRow(t("products.unit"), self.unit_input)
        layout.addLayout(form)
        layout.addSpacing(16)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton(t("products.cancel"))
        cancel_btn.setObjectName("cancel_btn")
        cancel_btn.clicked.connect(self.reject)
        ok_btn = QPushButton(t("products.update") if is_edit else t("products.save"))
        ok_btn.setObjectName("ok_btn")
        ok_btn.clicked.connect(self.validate_and_accept)
        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(ok_btn)
        layout.addLayout(btn_row)

    def reload_categories(self):
        current = self.category_combo.currentText() if self.category_combo.count() > 0 else ""
        self.category_combo.clear()
        cats = get_category_names()
        if not cats:
            add_category("General")
            cats = get_category_names()
        self.category_combo.addItems(cats)
        if current in cats:
            self.category_combo.setCurrentText(current)

    def open_manage_categories(self):
        dlg = ManageCategoriesDialog(self)
        dlg.exec()
        self.reload_categories()

    def validate_and_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, t("common.validation"), t("products.name_req"))
            self.name_input.setFocus()
            return
        self.accept()

    def get_data(self):
        return {
            "name":        self.name_input.text().strip(),
            "barcode":     self.barcode_input.text().strip(),
            "category":    self.category_combo.currentText(),
            "supplier_id": self.supplier_combo.currentData(),
            "price":       self.price_input.value(),
            "cost_price":  self.cost_price_input.value(),
            "stock_qty":   self.qty_input.value(),
            "unit":        self.unit_input.text().strip() or "pcs",
        }


class ProductsWidget(BaseTableWidget):
    def __init__(self):
        super().__init__(t("products.title"),
                         [t("products.col_id"), t("products.col_barcode"), t("products.col_name"),
                          t("products.col_category"), t("products.col_price"), t("products.col_stock"),
                          t("products.col_unit")])
        header = self.table.horizontalHeader()
        from PyQt6.QtWidgets import QHeaderView
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)       # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)       # Barcode
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)     # Name — takes all extra space
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)       # Category
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)       # Price
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)       # Stock
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)       # Unit
        self.table.setColumnWidth(0, 50)   # ID
        self.table.setColumnWidth(1, 120)  # Barcode
        self.table.setColumnWidth(3, 110)  # Category
        self.table.setColumnWidth(4, 110)  # Price
        self.table.setColumnWidth(5, 70)   # Stock
        self.table.setColumnWidth(6, 70)   # Unit
        
        top_layout = self.layout().itemAt(0).layout()

        self.edit_btn = QPushButton(t("products.edit"))
        self.edit_btn.setIcon(qicon("pencil", "white"))
        self.edit_btn.setStyleSheet(ACTION_BTN.format(bg="#3b82f6", hover="#2563eb"))
        self.edit_btn.clicked.connect(self.edit_selected)
        top_layout.insertWidget(top_layout.count() - 1, self.edit_btn)

        self.delete_btn = QPushButton(t("products.delete"))
        self.delete_btn.setIcon(qicon("trash", "white"))
        self.delete_btn.setStyleSheet(ACTION_BTN.format(bg="#ef4444", hover="#dc2626"))
        self.delete_btn.clicked.connect(self.delete_selected)
        top_layout.insertWidget(top_layout.count() - 1, self.delete_btn)

        
        self.set_sortable_columns([
            (t("products.col_price"), 4),
            (t("products.col_stock"), 5),
        ])

        self.add_btn.clicked.connect(self.open_add_dialog)
        self.table.cellDoubleClicked.connect(self.open_edit_on_double_click)
        self.refresh()

    def open_edit_on_double_click(self, row, col):
        self.edit_selected()

    def refresh(self):
        self.products = get_all_products()
        rows = [(p.id, p.barcode or "", p.name, p.category,
                 f"{p.price:.2f}", int(p.stock_qty), p.unit)
                for p in self.products]
        self.populate(rows)

    def get_selected_product(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t("common.warning"), t("products.select_first"))
            return None
        product_id = int(self.table.item(row, 0).text())
        return next((p for p in self.products if p.id == product_id), None)

    def open_add_dialog(self):
        dlg = ProductDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            add_product(data["name"], data["category"], data["price"],
                        data["stock_qty"], data["unit"], data["barcode"],
                        supplier_id=data["supplier_id"],
                        cost_price=data["cost_price"])
            self.refresh()

    def edit_selected(self):
        product = self.get_selected_product()
        if not product:
            return
        dlg = ProductDialog(self, product=product)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            update_product(product.id,
                           name=data["name"],
                           barcode=data["barcode"],
                           category=data["category"],
                           supplier_id=data["supplier_id"],
                           price=data["price"],
                           cost_price=data["cost_price"],
                           stock_qty=data["stock_qty"],
                           unit=data["unit"])
            self.refresh()

    def delete_selected(self):
        product = self.get_selected_product()
        if not product:
            return
        reply = QMessageBox.question(self, t("common.confirm_delete"),
                                     t("products.del_confirm", name=product.name),
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            delete_product(product.id)
            self.refresh()
