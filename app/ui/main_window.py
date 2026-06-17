from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from app.i18n import t
from app.ui.icons import qicon
from app.ui.dashboard import DashboardWidget
from app.ui.products import ProductsWidget
from app.ui.suppliers import SuppliersWidget
from app.ui.clients import ClientsWidget
from app.ui.invoices import InvoicesWidget
from app.ui.debts import DebtsWidget
from app.ui.settings import SettingsWidget
from app.utils import resource_path

SIDEBAR_STYLE = """
    QWidget#sidebar {
        background-color: #1e293b;
    }
    QPushButton {
        background-color: transparent;
        color: #f1f5f9;
        border: none;
        padding: 14px 20px;
        text-align: left;
        font-size: 14px;
        border-radius: 6px;
    }
    QPushButton:hover { background-color: #334155; }
    QPushButton:checked { background-color: #f59e0b; color: #1c1917; font-weight: bold; }
"""

class MainWindow(QMainWindow):
    logout_requested = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle(t("window.title"))
        self.setMinimumSize(1100, 700)
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        sidebar = QWidget(objectName="sidebar")
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet(SIDEBAR_STYLE)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(10, 20, 10, 20)
        sb_layout.setSpacing(5)

        from PyQt6.QtGui import QPixmap
        logo_lbl = QLabel()
        logo_lbl.setPixmap(QPixmap(resource_path("assets/icon.png")).scaled(
            150, 150, Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation))
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_lbl.setStyleSheet("background: transparent; padding: 10px;")
        sb_layout.addWidget(logo_lbl)
        sb_layout.addSpacing(10)

        self.stack = QStackedWidget()
        self.pages = {
            "Dashboard": DashboardWidget(),
            "Products":  ProductsWidget(),
            "Suppliers": SuppliersWidget(),
            "Clients":   ClientsWidget(),
            "Invoices":  InvoicesWidget(),
            "Debts":     DebtsWidget(),
            "Settings":  SettingsWidget(),
        }
        icons = {
            "Dashboard": qicon("dashboard", "#f1f5f9"),
            "Products":  qicon("products", "#f1f5f9"),
            "Suppliers": qicon("suppliers", "#f1f5f9"),
            "Clients":   qicon("clients", "#f1f5f9"),
            "Invoices":  qicon("invoices", "#f1f5f9"),
            "Debts":     qicon("debts", "#f1f5f9"),
            "Settings":  qicon("settings", "#f1f5f9"),
        }
        sidebar_keys = {
            "Dashboard": "sidebar.dashboard",
            "Products":  "sidebar.products",
            "Suppliers": "sidebar.suppliers",
            "Clients":   "sidebar.clients",
            "Invoices":  "sidebar.invoices",
            "Debts":     "sidebar.debts",
            "Settings":  "sidebar.settings",
        }
        self.nav_buttons = []

        for name, widget in self.pages.items():
            self.stack.addWidget(widget)
            label = t(sidebar_keys[name])
            btn = QPushButton(f"  {label}")
            btn.setIcon(icons[name])
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, n=name: self.navigate(n))
            sb_layout.addWidget(btn)
            self.nav_buttons.append((name, btn))

        sb_layout.addStretch()

        # Logout button — pinned at bottom
        logout_btn = QPushButton(f"  {t('sidebar.logout')}")
        logout_btn.setIcon(qicon("logout", "#ef4444"))
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ef4444;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #ef4444;
                color: white;
                border-color: #ef4444;
            }
        """)
        logout_btn.clicked.connect(self._logout)
        sb_layout.addWidget(logout_btn)

        layout.addWidget(sidebar)
        layout.addWidget(self.stack)

        self.navigate("Dashboard")

    def navigate(self, name):
        page_names = list(self.pages.keys())
        self.stack.setCurrentIndex(page_names.index(name))
        for n, btn in self.nav_buttons:
            btn.setChecked(n == name)
        if hasattr(self.pages[name], "refresh"):
            self.pages[name].refresh()

    def _logout(self):
        reply = QMessageBox.question(
            self,
            t("logout.confirm_title"),
            t("logout.confirm_msg"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()
            self.close()
