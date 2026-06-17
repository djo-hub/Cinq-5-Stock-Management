from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

from app.config import get as cfg_get, verify_password
from app.i18n import t
from app.utils import resource_path
from PyQt6.QtGui import QPixmap


LOGIN_STYLE = """
    QDialog {
        background-color: #0f172a;
    }
    QLabel#title {
        color: #f1f5f9;
        font-size: 22px;
        font-weight: bold;
    }
    QLabel#subtitle {
        color: #64748b;
        font-size: 12px;
    }
    QLabel {
        color: #f1f5f9;
        font-size: 13px;
    }
    QLineEdit {
        background-color: #1e293b;
        color: #f1f5f9;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px 14px;
        font-size: 12px;
        min-height: 18px;
    }
    QLineEdit:focus {
        border: 1px solid #f59e0b;
    }
    QPushButton#login_btn {
        background-color: #f59e0b;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 11px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton#login_btn:hover {
        background-color: #d97706;
    }
"""


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("5-Cinq Manager — Login")
        self.setFixedSize(420, 420)
        self.setStyleSheet(LOGIN_STYLE)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 36, 40, 36)
        layout.setSpacing(14)

        # Header — Your logo image
        logo = QLabel()
        logo_pixmap = QPixmap(resource_path("assets/icon.png"))
        if not logo_pixmap.isNull():
            logo.setPixmap(logo_pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("margin-bottom: 8px;")

        title = QLabel("5-Cinq Manager")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)


        subtitle = QLabel(t("login.subtitle"))
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(6)

        # Fields
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(t("login.username"))
        self.username_input.setMinimumHeight(48) 

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(t("login.password"))
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(48) 

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)

        # Login button
        login_btn = QPushButton(t("login.btn"))
        login_btn.setObjectName("login_btn")
        login_btn.clicked.connect(self.attempt_login)
        self.password_input.returnPressed.connect(self.attempt_login)
        self.username_input.returnPressed.connect(self.attempt_login)

        layout.addSpacing(4)
        layout.addWidget(login_btn)

    def attempt_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if username == cfg_get("username") and verify_password(password, cfg_get("password")):
            self.accept()
        else:
            QMessageBox.warning(self, t("login.failed_title"), t("login.failed_msg"))
            self.password_input.clear()
            self.password_input.setFocus()
