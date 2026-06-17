from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QSizePolicy, QGridLayout
)
from PyQt6.QtCore import Qt
from app.services.dashboard_service import (
    get_dashboard_stats, get_monthly_revenue, get_monthly_profit
)
from app.config import get as cfg_get
from app.i18n import t, format_date
from app.ui.icons import icon_pixmap
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


CARD_STYLE = """
    QFrame#card {{
        background-color: #1e293b;
        border-radius: 14px;
        border-left: 5px solid {accent};
        border-right: none;
        border-top: none;
        border-bottom: none;
    }}
    QFrame#card:hover {{ background-color: #263450; }}
"""

WARN_ROW_STYLE = """
    QFrame#warn_row {{
        background-color: #1e293b;
        border-radius: 8px;
    }}
    QFrame#warn_row:hover {{ background-color: #263450; }}
"""


def make_divider():
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFixedHeight(1)
    line.setStyleSheet("background-color: #1e293b;")
    return line


def make_section_title(text):
    lbl = QLabel(text)
    lbl.setStyleSheet("color: #f59e0b; font-size: 12px; font-weight: bold; letter-spacing: 1px;")
    return lbl


def create_revenue_chart():
    """Create a line chart for monthly revenue."""
    data = get_monthly_revenue(months=6)
    months = [label for label, _ in data]
    revenues = [value for _, value in data]
    
    fig = Figure(figsize=(6, 3), dpi=100, facecolor='#1e293b', edgecolor='none')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#0f172a')
    
    ax.plot(months, revenues, marker='o', linewidth=2, color='#3498db', markersize=6, label='Revenue')
    ax.fill_between(range(len(months)), revenues, alpha=0.3, color='#3498db')
    
    ax.set_title(t('dash.chart_revenue'), color='#f59e0b', fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel(t('dash.chart_month'), color='#94a3b8', fontsize=10)
    ax.set_ylabel(t('dash.chart_amount'), color='#94a3b8', fontsize=10)
    ax.grid(True, alpha=0.2, color='#475569')
    ax.tick_params(colors='#94a3b8', labelsize=9)
    
    for spine in ax.spines.values():
        spine.set_color('#475569')
    
    fig.tight_layout()
    
    canvas = FigureCanvas(fig)
    canvas.setParent(None)
    canvas.setMaximumHeight(350)
    return canvas


def create_profit_chart():
    """Create a line chart for monthly profit."""
    data = get_monthly_profit(months=6)
    months = [label for label, _ in data]
    profits = [value for _, value in data]
    
    fig = Figure(figsize=(6, 3), dpi=100, facecolor='#1e293b', edgecolor='none')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#0f172a')
    
    ax.plot(months, profits, marker='s', linewidth=2, color='#f39c12', markersize=6, label='Profit')
    ax.fill_between(range(len(months)), profits, alpha=0.3, color='#f39c12')
    
    ax.set_title(t('dash.chart_profit'), color='#f59e0b', fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel(t('dash.chart_month'), color='#94a3b8', fontsize=10)
    ax.set_ylabel(t('dash.chart_amount'), color='#94a3b8', fontsize=10)
    ax.grid(True, alpha=0.2, color='#475569')
    ax.tick_params(colors='#94a3b8', labelsize=9)
    
    for spine in ax.spines.values():
        spine.set_color('#475569')
    
    fig.tight_layout()
    
    canvas = FigureCanvas(fig)
    canvas.setParent(None)
    canvas.setMaximumHeight(350)
    return canvas





def make_stat_card(icon_name, title, value, accent, subtitle=None):
    card = QFrame()
    card.setObjectName("card")
    card.setStyleSheet(CARD_STYLE.format(accent=accent))
    card.setFixedHeight(110)

    layout = QHBoxLayout(card)
    layout.setContentsMargins(16, 14, 16, 14)
    layout.setSpacing(12)

    icon_lbl = QLabel()
    icon_lbl.setFixedSize(46, 46)
    icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    icon_lbl.setPixmap(icon_pixmap(icon_name, accent, 26))
    icon_lbl.setStyleSheet(f"""
        QLabel {{
            background-color: {accent}28;
            border-radius: 23px;
        }}
    """)

    text_col = QVBoxLayout()
    text_col.setSpacing(2)

    t_lbl = QLabel(title)
    t_lbl.setStyleSheet("color: #94a3b8; font-size: 10px; font-weight: 600; letter-spacing: 1px;")
    t_lbl.setWordWrap(True)

    v = QLabel(str(value))
    v.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")

    text_col.addWidget(t_lbl)
    text_col.addWidget(v)

    if subtitle:
        s = QLabel(subtitle)
        s.setStyleSheet("color: #64748b; font-size: 10px;")
        text_col.addWidget(s)

    layout.addWidget(icon_lbl)
    layout.addLayout(text_col)
    return card


class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def refresh(self):
        old_layout = self.layout()
        if old_layout:
            QWidget().setLayout(old_layout)  # detach and discard old layout
        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet("background-color: #0f172a;")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { 
                border: none; 
                background: transparent; 
            }
            QScrollBar:vertical {
                background-color: #0f172a;
                width: 10px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background-color: #475569;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #64748b;
            }
        """)

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        main = QVBoxLayout(container)
        main.setContentsMargins(30, 30, 30, 30)
        main.setSpacing(22)

        # ── Header ──────────────────────────────────────────
        from datetime import datetime
        now = datetime.now()
        title = QLabel(t("dash.title"))
        title.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")

        date_lbl = QLabel(format_date(now))
        date_lbl.setStyleSheet("color: #64748b; font-size: 12px;")

        main.addWidget(title)
        main.addWidget(date_lbl)
        main.addWidget(make_divider())

        stats = get_dashboard_stats()

        # ── Row 1: Stock Stats ──
        main.addWidget(make_section_title(t("dash.section_stock")))
        grid1_widget = QWidget()
        grid1_widget.setStyleSheet("background: transparent;")
        grid1 = QGridLayout(grid1_widget)
        grid1.setSpacing(14)
        grid1.setContentsMargins(0, 0, 0, 0)

        cards1 = [
            make_stat_card("package", t("dash.total_products"),  stats["total_products"],          "#3498db"),
            make_stat_card("check_circle", t("dash.total_in_stock"),  f'{stats["total_in_stock"]} pcs', "#1abc9c"),
            make_stat_card("alert_circle", t("dash.low_stock"), stats["low_stock"],               "#e67e22", t("dash.units", n=cfg_get('low_stock_threshold'))),
            make_stat_card("close_circle", t("dash.out_of_stock"),    len(stats["out_of_stock"]),        "#e74c3c"),
        ]
        for i, card in enumerate(cards1):
            grid1.addWidget(card, 0, i)
            grid1.setColumnStretch(i, 1)

        main.addWidget(grid1_widget)
        main.addWidget(make_divider())

        # ── Row 2: Financial Stats ──
        main.addWidget(make_section_title(t("dash.section_finance")))
        grid2_widget = QWidget()
        grid2_widget.setStyleSheet("background: transparent;")
        grid2 = QGridLayout(grid2_widget)
        grid2.setSpacing(14)
        grid2.setContentsMargins(0, 0, 0, 0)

        cards2 = [
            make_stat_card("cash_multiple", t("dash.total_income"), f'{stats["total_income"]:,.0f}',   "#2ecc71", t("dash.paid_only")),
            make_stat_card("file_alert", t("dash.unpaid_invoices"),    stats["unpaid_invoices"],           "#e74c3c"),
            make_stat_card("cash_off", t("dash.total_debts"),  f'{stats["total_debts"]:,.0f}',    "#9b59b6"),
            make_stat_card("chart_bar", t("dash.total_profit"),      f'{stats["total_profit"]:,.0f}', "#f39c12", t("dash.profit_hint")),
        ]
        for i, card in enumerate(cards2):
            grid2.addWidget(card, 0, i)
            grid2.setColumnStretch(i, 1)

        main.addWidget(grid2_widget)
        main.addWidget(make_divider())

        # ── Charts Section ──
        main.addWidget(make_section_title(t("dash.section_analytics")))
        
        # Revenue and Profit Charts (side by side)
        charts_row = QHBoxLayout()
        charts_row.setSpacing(14)
        
        revenue_canvas = create_revenue_chart()
        profit_canvas = create_profit_chart()
        
        charts_row.addWidget(revenue_canvas)
        charts_row.addWidget(profit_canvas)
        
        charts_row_widget = QWidget()
        charts_row_widget.setLayout(charts_row)
        charts_row_widget.setStyleSheet("background: transparent;")
        main.addWidget(charts_row_widget)
        
        main.addWidget(make_divider())

        # ── Out of Stock List ────────────────────────────────
        main.addWidget(make_section_title(t("dash.section_oos")))

        if stats["out_of_stock"]:
            for name, qty in stats["out_of_stock"]:
                row_frame = QFrame()
                row_frame.setObjectName("warn_row")
                row_frame.setStyleSheet(WARN_ROW_STYLE)
                row_frame.setFixedHeight(44)

                rl = QHBoxLayout(row_frame)
                rl.setContentsMargins(14, 0, 14, 0)

                dot = QLabel()
                dot.setPixmap(icon_pixmap("alert_dot", "#e74c3c", 16))
                name_lbl = QLabel(name)
                name_lbl.setStyleSheet("color: #dfe6e9; font-size: 13px;")
                qty_lbl = QLabel(t("dash.stock_label", qty=qty))
                qty_lbl.setStyleSheet("color: #e74c3c; font-size: 12px; font-weight: bold;")
                qty_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                rl.addWidget(dot)
                rl.addWidget(name_lbl)
                rl.addStretch()
                rl.addWidget(qty_lbl)
                main.addWidget(row_frame)
        else:
            ok_icon = QLabel()
            ok_icon.setPixmap(icon_pixmap("check_outline", "#22c55e", 18))
            ok_text = QLabel(t("dash.all_in_stock"))
            ok_text.setStyleSheet("color: #22c55e; font-size: 13px; padding: 8px 0;")
            ok_row = QHBoxLayout()
            ok_row.setContentsMargins(0, 0, 0, 0)
            ok_row.setSpacing(6)
            ok_row.addWidget(ok_icon)
            ok_row.addWidget(ok_text)
            ok_row.addStretch()
            ok_container = QWidget()
            ok_container.setStyleSheet("background: transparent;")
            ok_container.setLayout(ok_row)
            main.addWidget(ok_container)

        main.addStretch()

        scroll.setWidget(container)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)
