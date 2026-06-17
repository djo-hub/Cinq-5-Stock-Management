from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QFrame, QHeaderView
)
from PyQt6.QtCore import Qt
from app.i18n import t
from app.ui.base_table import NoFocusDelegate

PROFILE_STYLE = """
    QDialog { background-color: #0f172a; color: #f1f5f9; }
    QLabel  { color: #f1f5f9; border: none; }
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
"""


class StatCard(QFrame):
    def __init__(self, label, value, color="#f59e0b"):
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


class SupplierProfileDialog(QDialog):
    def __init__(self, supplier, parent=None):
        super().__init__(parent)
        self.supplier = supplier
        self.setWindowTitle(f"Supplier — {supplier.name}")
        self.setMinimumSize(700, 520)
        self.setStyleSheet(PROFILE_STYLE)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(16)

        # ── Header ──
        header = QHBoxLayout()
        icon = QLabel("🏭")
        icon.setStyleSheet("font-size: 32px;")
        info = QVBoxLayout()
        name_lbl = QLabel(supplier.name)
        name_lbl.setStyleSheet("font-size: 22px; font-weight: bold; color: #f59e0b;")
        parts = []
        if supplier.contact_person: parts.append(f"👤 {supplier.contact_person}")
        if supplier.phone:          parts.append(f"📞 {supplier.phone}")
        if supplier.email:          parts.append(f"✉️ {supplier.email}")
        if supplier.address:        parts.append(f"📍 {supplier.address}")
        details = QLabel("    ".join(parts) if parts else t("sup_profile.no_contact"))
        details.setStyleSheet("color: #94a3b8; font-size: 12px;")
        info.addWidget(name_lbl)
        info.addWidget(details)
        header.addWidget(icon)
        header.addLayout(info)
        header.addStretch()
        layout.addLayout(header)

        # ── Stat cards ──
        products = supplier.products
        total_products = len(products)
        categories = len({p.category for p in products})
        total_value = sum(p.price * p.stock_qty for p in products)
        total_stock = sum(p.stock_qty for p in products)

        cards = QHBoxLayout()
        cards.setSpacing(12)
        cards.addWidget(StatCard(t("sup_profile.total_products"),   str(total_products)))
        cards.addWidget(StatCard(t("sup_profile.categories"),       str(categories),     "#3b82f6"))
        cards.addWidget(StatCard(t("sup_profile.units_in_stock"),   str(total_stock),    "#22c55e"))
        cards.addWidget(StatCard(t("sup_profile.stock_value"),f"{total_value:,.0f}","#f59e0b"))
        layout.addLayout(cards)

        # ── Products table ──
        section = QLabel(t("sup_profile.supplied_products"))
        section.setStyleSheet("font-size: 15px; font-weight: bold; color: #f1f5f9;")
        layout.addWidget(section)

        table = QTableWidget(0, 5)
        table.setHorizontalHeaderLabels(
            [t("sup_profile.col_id"), t("sup_profile.col_name"), t("sup_profile.col_category"),
             t("sup_profile.col_price"), t("sup_profile.col_stock")])
        h = table.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        h.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        h.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        h.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        h.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        table.setColumnWidth(0, 50)
        table.setColumnWidth(2, 110)
        table.setColumnWidth(3, 120)
        table.setColumnWidth(4, 80)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setShowGrid(False)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.verticalHeader().setDefaultSectionSize(38)
        table.setItemDelegate(NoFocusDelegate(table))
        table.setRowCount(len(products))

        for r, p in enumerate(products):
            for c, val in enumerate([p.id, p.name, p.category,
                                     f"{p.price:,.2f}", int(p.stock_qty)]):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(r, c, item)

        layout.addWidget(table)

        # ── Notes ──
        if supplier.notes and supplier.notes.strip():
            notes = QLabel(f"📝  {supplier.notes}")
            notes.setStyleSheet("color: #64748b; font-size: 12px;")
            notes.setWordWrap(True)
            layout.addWidget(notes)

        # ── Close ──
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        close_btn = QPushButton(t("sup_profile.close"))
        close_btn.setObjectName("close_btn")
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)
