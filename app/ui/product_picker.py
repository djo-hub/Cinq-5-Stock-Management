from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QScrollArea, QWidget, QGridLayout, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from app.i18n import t

PICKER_STYLE = """
    QDialog { background-color: #16212e; color: white; }
    QLineEdit {
        background-color: #1e2a38; color: #ecf0f1;
        border: 1px solid #3d5166; border-radius: 8px;
        padding: 10px 14px; font-size: 14px;
    }
    QLineEdit:focus { border: 1px solid #1abc9c; }
    QScrollArea { border: none; background: transparent; }
    QWidget#scroll_content { background: transparent; }
"""

CARD_NORMAL = """
    QFrame {
        background-color: #1e2a38;
        border: 2px solid #2c3e50;
        border-radius: 10px;
    }
    QFrame:hover {
        border: 2px solid #1abc9c;
        background-color: #243447;
    }
"""

CARD_OUT = """
    QFrame {
        background-color: #1a1a2e;
        border: 2px solid #333;
        border-radius: 10px;
    }
"""


class ProductCard(QFrame):
    clicked = pyqtSignal(object)

    def __init__(self, product):
        super().__init__()
        self.product = product
        self._in_stock = product.stock_qty > 0
        self.setStyleSheet(CARD_NORMAL if self._in_stock else CARD_OUT)
        # No fixed width — let the grid stretch it
        self.setFixedHeight(115)
        self.setCursor(
            Qt.CursorShape.PointingHandCursor if self._in_stock
            else Qt.CursorShape.ForbiddenCursor
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(3)

        name_lbl = QLabel(product.name)
        name_lbl.setWordWrap(True)
        name_lbl.setStyleSheet(
            f"color: {'#ecf0f1' if self._in_stock else '#555'};"
            "font-size: 12px; font-weight: bold; border: none;"
        )
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cat_lbl = QLabel(product.category)
        cat_lbl.setStyleSheet("color: #7f8c8d; font-size: 11px; border: none;")
        cat_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        price_lbl = QLabel(f"{product.price:.0f} DA")
        price_lbl.setStyleSheet(
            "color: #1abc9c; font-size: 13px; font-weight: bold; border: none;"
        )
        price_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        stock_color = (
            "#e74c3c" if product.stock_qty <= 0
            else "#e67e22" if product.stock_qty < 5
            else "#2ecc71"
        )
        stock_text = (
            t("picker.out_of_stock") if product.stock_qty <= 0
            else t("picker.stock", qty=int(product.stock_qty))
        )
        stock_lbl = QLabel(stock_text)
        stock_lbl.setStyleSheet(
            f"color: {stock_color}; font-size: 11px; border: none;"
        )
        stock_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(name_lbl)
        layout.addWidget(cat_lbl)
        layout.addWidget(price_lbl)
        layout.addWidget(stock_lbl)

    def mousePressEvent(self, event):
        if self._in_stock and event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.product)


class ProductPickerDialog(QDialog):
    product_selected = pyqtSignal(object)

    CARD_MIN_WIDTH = 150
    CARD_SPACING = 12

    def __init__(self, products, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("picker.win_title"))
        self.setMinimumSize(500, 480)
        self.resize(720, 520)
        self.setStyleSheet(PICKER_STYLE)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )
        self.all_products = products
        self.current_products = list(products)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(14)

        title = QLabel(t("picker.title"))
        title.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #1abc9c;"
        )
        layout.addWidget(title)

        self.search = QLineEdit()
        self.search.setPlaceholderText(t("picker.search"))
        self.search.textChanged.connect(self.filter_products)
        layout.addWidget(self.search)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_content = QWidget(objectName="scroll_content")
        self.scroll_content.setStyleSheet("background: transparent;")
        self.grid = QGridLayout(self.scroll_content)
        self.grid.setSpacing(self.CARD_SPACING)
        self.grid.setContentsMargins(4, 4, 4, 4)
        self.scroll.setWidget(self.scroll_content)
        layout.addWidget(self.scroll)

        self.count_lbl = QLabel()
        self.count_lbl.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        layout.addWidget(self.count_lbl)

        self.render_products(self.current_products)

    def _calc_cols(self):
        available = self.scroll.viewport().width() - 20
        cols = max(1, available // (self.CARD_MIN_WIDTH + self.CARD_SPACING))
        return int(cols)

    def render_products(self, products):
        # Fully clear grid layout
        while self.grid.count():
            item = self.grid.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()

        # Remove all column stretch settings
        for col in range(self.grid.columnCount()):
            self.grid.setColumnStretch(col, 0)

        cols = self._calc_cols()

        # Set equal stretch for each column so cards fill the row
        for col in range(cols):
            self.grid.setColumnStretch(col, 1)

        for idx, product in enumerate(products):
            card = ProductCard(product)
            card.clicked.connect(self.on_product_selected)
            self.grid.addWidget(card, idx // cols, idx % cols)

        # Add stretch at bottom so cards don't spread vertically
        self.grid.setRowStretch(
            (len(products) - 1) // cols + 1 if products else 0, 1
        )

        total = len(products)
        in_stock = sum(1 for p in products if p.stock_qty > 0)
        self.count_lbl.setText(
            t("picker.count", total=total, in_stock=in_stock, out=total - in_stock)
        )

    def filter_products(self, text):
        text = text.lower()
        self.current_products = [
            p for p in self.all_products
            if text in p.name.lower()
            or text in p.category.lower()
            or text in (p.barcode or "").lower()
        ]
        self.render_products(self.current_products)

    def resizeEvent(self, event):
        """Re-render grid when window is resized so columns adjust."""
        super().resizeEvent(event)
        self.render_products(self.current_products)

    def on_product_selected(self, product):
        self.product_selected.emit(product)
        self.accept()
