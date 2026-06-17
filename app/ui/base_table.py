from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
    QAbstractItemView, QApplication, QStyledItemDelegate, QStyleOptionViewItem,
    QComboBox
)
from PyQt6.QtCore import Qt, QEvent, QPoint
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QAbstractItemView, QStyle
from app.i18n import t
from app.ui.icons import qicon


class NoFocusDelegate(QStyledItemDelegate):
    """Removes the dotted focus rectangle from table cells."""
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.state &= ~QStyle.StateFlag.State_HasFocus

TABLE_STYLE = """
    QTableWidget {
        background-color: #0f172a;
        alternate-background-color: #1e293b;
        color: #f1f5f9;
        gridline-color: #1e293b;
        border: none;
        font-size: 13px;
    }
    QTableWidget::item {
        padding: 10px 14px;
        border: none;
    }
    QTableWidget::item:focus {
        border: none;
        outline: none;
    }
    QTableWidget::item:selected {
        background-color: #f59e0b !important;
        color: #1c1917;
    }
    QHeaderView::section {
        background-color: #1e293b;
        color: #f59e0b;
        padding: 10px 8px;
        border: none;
        font-weight: bold;
        font-size: 13px;
        border-bottom: 2px solid #f59e0b;
    }
    QScrollBar:vertical {
        background: #1e293b;
        width: 8px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical {
        background: #334155;
        border-radius: 4px;
    }
"""

PAGE_STYLE = "background: #0f172a;"
SEARCH_STYLE = """
    QLineEdit {
        background-color: #1e293b;
        color: #f1f5f9;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 9px 14px;
        font-size: 13px;
    }
    QLineEdit:focus { border: 1px solid #f59e0b; }
"""
SORT_COMBO_STYLE = """
    QComboBox {
        background-color: #1e293b;
        color: #f1f5f9;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 9px 14px;
        font-size: 13px;
        min-width: 180px;
    }
    QComboBox:focus { border: 1px solid #f59e0b; }
    QComboBox::drop-down {
        border: none; background: #334155;
        width: 24px; border-radius: 0 8px 8px 0;
    }
    QComboBox QAbstractItemView {
        background: #1e293b; color: #f1f5f9;
        selection-background-color: #f59e0b;
        border: 1px solid #334155;
    }
"""
ADD_BTN_STYLE = """
    QPushButton {
        background: #f59e0b; color: white; border: none;
        padding: 9px 22px; border-radius: 8px;
        font-size: 13px; font-weight: bold;
    }
    QPushButton:hover { background: #d97706; }
"""
PAGINATION_BTN_STYLE = """
    QPushButton {
        background: #1e293b; color: #94a3b8;
        border: 1px solid #334155;
        padding: 6px 10px; border-radius: 6px;
        font-size: 12px; font-weight: bold;
        min-width: 34px;
    }
    QPushButton:hover { background: #263450; color: #f1f5f9; }
    QPushButton:disabled { background: #0f172a; color: #334155; border-color: #1e293b; }
"""
PAGE_BTN_ACTIVE_STYLE = """
    QPushButton {
        background: #f59e0b; color: white;
        border: 1px solid #f59e0b;
        padding: 6px 10px; border-radius: 6px;
        font-size: 12px; font-weight: bold;
        min-width: 34px;
    }
"""


class ClickableTableWidget(QTableWidget):
    """
    Subclass that overrides mousePressEvent to always select
    the correct row based on Y position — bypassing cell widgets.
    """
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            row = self.rowAt(pos.y())
            if row >= 0:
                self.selectRow(row)
        super().mousePressEvent(event)

    def _select_row_from_child(self, global_pos):
        """Called by child widgets to select their parent row."""
        local_pos = self.viewport().mapFromGlobal(global_pos)
        row = self.rowAt(local_pos.y())
        if row >= 0:
            self.selectRow(row)


class RowSelectFilter(QWidget):
    """Event filter installed on cell widgets to propagate clicks to the table."""
    def __init__(self, table: ClickableTableWidget):
        super().__init__()
        self.table = table

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                try:
                    global_pos = obj.mapToGlobal(event.pos())
                    self.table._select_row_from_child(global_pos)
                except Exception:
                    pass
        return False


class BaseTableWidget(QWidget):
    PAGE_SIZE = 11

    def __init__(self, title, columns):
        super().__init__()
        self._current_page = 0
        self.all_rows = []
        self._filtered_rows = []

        self.setStyleSheet(PAGE_STYLE)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(14)

        # Top bar
        top = QHBoxLayout()
        lbl = QLabel(title)
        lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #f1f5f9;")
        top.addWidget(lbl)
        top.addStretch()
        self.add_btn = QPushButton(t("table.add"))
        self.add_btn.setIcon(qicon("plus_circle", "white"))
        self.add_btn.setStyleSheet(ADD_BTN_STYLE)
        top.addWidget(self.add_btn)
        layout.addLayout(top)

        # Search + Sort row
        search_sort_row = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText(t("table.search"))
        self.search.setStyleSheet(SEARCH_STYLE)
        self.search.addAction(qicon("magnify", "#94a3b8"), QLineEdit.ActionPosition.LeadingPosition)
        self.search.textChanged.connect(self.filter_table)
        search_sort_row.addWidget(self.search)

        self.sort_combo = QComboBox()
        self.sort_combo.setStyleSheet(SORT_COMBO_STYLE)
        self.sort_combo.addItem(t("table.sort_default"), None)
        self.sort_combo.currentIndexChanged.connect(lambda: self._apply_sort())
        self.sort_combo.setVisible(False)  # hidden until sortable columns are set
        search_sort_row.addWidget(self.sort_combo)
        layout.addLayout(search_sort_row)

        # Table
        self.table = ClickableTableWidget()
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setStyleSheet(TABLE_STYLE)
        self.table.setItemDelegate(NoFocusDelegate(self.table))
        self.table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.table.verticalHeader().setDefaultSectionSize(40)
        layout.addWidget(self.table)

        # Pagination bar
        pag_bar = QHBoxLayout()
        pag_bar.setSpacing(6)

        self._info_label = QLabel()
        self._info_label.setStyleSheet("color: #64748b; font-size: 12px;")
        pag_bar.addWidget(self._info_label)
        pag_bar.addStretch()

        self._prev_btn = QPushButton(t("table.prev"))
        self._prev_btn.setStyleSheet(PAGINATION_BTN_STYLE)
        self._prev_btn.clicked.connect(lambda: self._go_to_page(self._current_page - 1))
        pag_bar.addWidget(self._prev_btn)

        # Numbered page buttons go here (rebuilt on each update)
        self._page_btns_container = QHBoxLayout()
        self._page_btns_container.setSpacing(4)
        pag_bar.addLayout(self._page_btns_container)

        self._next_btn = QPushButton(t("table.next"))
        self._next_btn.setStyleSheet(PAGINATION_BTN_STYLE)
        self._next_btn.clicked.connect(lambda: self._go_to_page(self._current_page + 1))
        pag_bar.addWidget(self._next_btn)

        layout.addLayout(pag_bar)

        # Shared event filter for cell widgets
        self._row_filter = RowSelectFilter(self.table)

    # ── Pagination helpers ─────────────────────────────────────────────────────

    def _total_pages(self):
        n = len(self._filtered_rows)
        return max(1, (n + self.PAGE_SIZE - 1) // self.PAGE_SIZE)

    def _go_to_page(self, page):
        self._current_page = max(0, min(page, self._total_pages() - 1))
        self._render_page()
        self._update_pagination()

    def _render_page(self):
        start = self._current_page * self.PAGE_SIZE
        end = start + self.PAGE_SIZE
        self._render(self._filtered_rows[start:end])

    def _page_range(self, current, total):
        """Return list of page indices (None = ellipsis) to show in the nav bar."""
        if total <= 7:
            return list(range(total))
        shown = sorted({0, total - 1, max(0, current - 1), current, min(total - 1, current + 1)})
        result = []
        prev = -2
        for p in shown:
            if p - prev > 1:
                result.append(None)
            result.append(p)
            prev = p
        return result

    def _update_pagination(self):
        total = self._total_pages()
        total_rows = len(self._filtered_rows)
        start = self._current_page * self.PAGE_SIZE + 1
        end = min(start + self.PAGE_SIZE - 1, total_rows)

        if total_rows == 0:
            self._info_label.setText(t("table.no_items"))
        else:
            self._info_label.setText(t("table.showing", start=start, end=end, total=total_rows))

        self._prev_btn.setEnabled(self._current_page > 0)
        self._next_btn.setEnabled(self._current_page < total - 1)

        # Rebuild numbered page buttons
        while self._page_btns_container.count():
            item = self._page_btns_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        prev_was_ellipsis = False
        for p in self._page_range(self._current_page, total):
            if p is None:
                if not prev_was_ellipsis:
                    dots = QLabel("…")
                    dots.setStyleSheet("color: #64748b; padding: 0 4px; font-size: 13px;")
                    self._page_btns_container.addWidget(dots)
                prev_was_ellipsis = True
            else:
                btn = QPushButton(str(p + 1))
                btn.setFixedWidth(34)
                if p == self._current_page:
                    btn.setStyleSheet(PAGE_BTN_ACTIVE_STYLE)
                else:
                    btn.setStyleSheet(PAGINATION_BTN_STYLE)
                btn.clicked.connect(lambda _, n=p: self._go_to_page(n))
                self._page_btns_container.addWidget(btn)
                prev_was_ellipsis = False

    # ── Public API ─────────────────────────────────────────────────────────────

    def set_sortable_columns(self, columns):
        """Register sortable numeric columns.
        columns: list of (display_name, column_index) tuples.
        """
        self.sort_combo.blockSignals(True)
        self.sort_combo.clear()
        self.sort_combo.addItem(t("table.sort_default"), None)
        for name, col_idx in columns:
            self.sort_combo.addItem(
                t("table.sort_low_high", col=name), (col_idx, False)
            )
            self.sort_combo.addItem(
                t("table.sort_high_low", col=name), (col_idx, True)
            )
        self.sort_combo.setVisible(True)
        self.sort_combo.blockSignals(False)

    def _apply_sort(self):
        """Sort _filtered_rows numerically by the selected column."""
        data = self.sort_combo.currentData()
        if data is None:
            # Restore original order (re-filter from all_rows)
            text = self.search.text()
            if text:
                self._filtered_rows = [
                    r for r in self.all_rows
                    if any(text.lower() in str(v).lower() for v in r)
                ]
            else:
                self._filtered_rows = list(self.all_rows)
        else:
            col_idx, reverse = data
            def sort_key(row):
                try:
                    return float(str(row[col_idx]).replace(",", ""))
                except (ValueError, IndexError):
                    return 0.0
            self._filtered_rows.sort(key=sort_key, reverse=reverse)
        self._current_page = 0
        self._render_page()
        self._update_pagination()

    def set_cell_widget(self, row, col, widget):
        self._install_filter(widget)
        self.table.setCellWidget(row, col, widget)

    def _install_filter(self, widget):
        widget.installEventFilter(self._row_filter)
        for child in widget.findChildren(QWidget):
            child.installEventFilter(self._row_filter)

    def populate(self, rows):
        self.all_rows = rows
        text = self.search.text()
        if text:
            self._filtered_rows = [r for r in rows
                                    if any(text.lower() in str(v).lower() for v in r)]
        else:
            self._filtered_rows = list(rows)
        self._apply_sort()

    def _render(self, rows):
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(r, c, item)

    def filter_table(self, text):
        if not hasattr(self, "all_rows"):
            return
        self._filtered_rows = [r for r in self.all_rows
                                if any(text.lower() in str(v).lower() for v in r)]
        self._apply_sort()
