"""First-run setup wizard for Manager application.

Guides users through initial configuration on first launch or when
settings.json is missing.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QSpinBox, QComboBox, QCheckBox, QWidget, QStackedLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from app.config import save_settings, hash_password
from app.i18n import t
from app.logger import get_logger


logger = get_logger()


WIZARD_STYLE = """
    QDialog {
        background-color: #0f172a;
    }
    QLabel#title {
        color: #f1f5f9;
        font-size: 20px;
        font-weight: bold;
    }
    QLabel#subtitle {
        color: #94a3b8;
        font-size: 12px;
    }
    QLabel {
        color: #f1f5f9;
        font-size: 12px;
    }
    QLineEdit, QSpinBox, QComboBox {
        background-color: #1e293b;
        color: #f1f5f9;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 8px 10px;
        font-size: 11px;
        min-height: 32px;
    }
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
        border: 1px solid #f59e0b;
    }
    QPushButton {
        background-color: #334155;
        color: #f1f5f9;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 12px;
        font-weight: bold;
        min-width: 80px;
    }
    QPushButton:hover {
        background-color: #475569;
    }
    QPushButton#next_btn {
        background-color: #f59e0b;
        color: white;
    }
    QPushButton#next_btn:hover {
        background-color: #d97706;
    }
    QCheckBox {
        color: #f1f5f9;
        spacing: 6px;
    }
    QCheckBox::indicator {
        width: 16px;
        height: 16px;
    }
"""


class FirstRunWizard(QDialog):
    """Multi-step first-run setup wizard."""
    
    setup_complete = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("5-Cinq Manager — Initial Setup")
        self.setFixedSize(500, 550)
        self.setStyleSheet(WIZARD_STYLE)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.setModal(True)
        
        self.current_page = 0
        self.config_data = {}
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(16)
        
        self.stack = QStackedLayout()
        self.main_layout.addLayout(self.stack)

        self.nav_widget = None

        self.create_pages()
        self.show_page(0)
    
    def create_pages(self):
        """Create all wizard pages."""
        self.pages = [
            self.create_welcome_page(),
            self.create_business_page(),
            self.create_credentials_page(),
            self.create_settings_page(),
            self.create_confirm_page(),
        ]
        for page in self.pages:
            self.stack.addWidget(page)
    
    def create_welcome_page(self):
        """Welcome page with introduction."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(16)
        
        title = QLabel("Welcome to 5-Cinq Manager")
        title.setObjectName("title")
        
        subtitle = QLabel("Let's set up your business management system")
        subtitle.setObjectName("subtitle")
        
        description = QLabel(
            "This wizard will help you configure 5-Cinq Manager for your business.\n\n"
            "You'll be asked to provide:\n"
            "• Business information\n"
            "• Login credentials\n"
            "• Currency and localization settings\n\n"
            "You can always change these settings later in the app."
        )
        description.setStyleSheet("color: #cbd5e1; line-height: 1.6;")
        description.setWordWrap(True)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(24)
        layout.addWidget(description)
        layout.addStretch()
        
        return container
    
    def create_business_page(self):
        """Business information page."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(16)
        
        title = QLabel("Business Information")
        title.setObjectName("title")
        
        subtitle = QLabel("Tell us about your business")
        subtitle.setObjectName("subtitle")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        
        # Business name
        name_label = QLabel("Business Name:")
        self.business_name = QLineEdit()
        self.business_name.setPlaceholderText("e.g., Djo Management")
        self.business_name.setText("MY BUSINESS")
        
        # Address
        address_label = QLabel("Address:")
        self.business_address = QLineEdit()
        self.business_address.setPlaceholderText("e.g., 123 Business Street")
        self.business_address.setText("123 Business Street, Algiers, Algeria")
        
        # Phone
        phone_label = QLabel("Phone Number:")
        self.business_phone = QLineEdit()
        self.business_phone.setPlaceholderText("e.g., +213 XX XX XX XX")
        self.business_phone.setText("+213 XX XX XX XX")
        
        # Email
        email_label = QLabel("Email:")
        self.business_email = QLineEdit()
        self.business_email.setPlaceholderText("e.g., info@mybusiness.com")
        
        layout.addWidget(name_label)
        layout.addWidget(self.business_name)
        layout.addWidget(address_label)
        layout.addWidget(self.business_address)
        layout.addWidget(phone_label)
        layout.addWidget(self.business_phone)
        layout.addWidget(email_label)
        layout.addWidget(self.business_email)
        layout.addStretch()
        
        return container
    
    def create_credentials_page(self):
        """Login credentials page."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(16)
        
        title = QLabel("Admin Credentials")
        title.setObjectName("title")
        
        subtitle = QLabel("Set your login credentials")
        subtitle.setObjectName("subtitle")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        
        # Username
        username_label = QLabel("Username:")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username for login")
        self.username.setText("admin")
        
        # Password
        password_label = QLabel("Password:")
        password_note = QLabel("(minimum 6 characters)")
        password_note.setStyleSheet("color: #94a3b8; font-size: 11px; margin-top: -8px;")
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter a strong password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Confirm password
        confirm_label = QLabel("Confirm Password:")
        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Re-enter your password")
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        
        layout.addWidget(username_label)
        layout.addWidget(self.username)
        layout.addSpacing(8)
        layout.addWidget(password_label)
        layout.addWidget(password_note)
        layout.addWidget(self.password)
        layout.addWidget(confirm_label)
        layout.addWidget(self.confirm_password)
        layout.addStretch()
        
        return container
    
    def create_settings_page(self):
        """Localization and business settings page."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(16)
        
        title = QLabel("Business Settings")
        title.setObjectName("title")
        
        subtitle = QLabel("Configure your preferences")
        subtitle.setObjectName("subtitle")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        
        # Currency
        currency_label = QLabel("Currency:")
        self.currency = QComboBox()
        self.currency.addItems(["DA", "USD", "EUR", "GBP"])
        self.currency.setCurrentText("DA")
        
        # Language
        language_label = QLabel("Language:")
        self.language = QComboBox()
        self.language.addItems(["English", "Français"])
        self.language.setCurrentIndex(0)
        
        # TVA rate
        tva_label = QLabel("VAT Rate (%):")
        self.tva_rate = QSpinBox()
        self.tva_rate.setRange(0, 100)
        self.tva_rate.setSingleStep(1)
        self.tva_rate.setValue(19)
        
        # Low stock threshold
        threshold_label = QLabel("Low Stock Warning (units):")
        self.low_stock_threshold = QSpinBox()
        self.low_stock_threshold.setRange(1, 1000)
        self.low_stock_threshold.setSingleStep(1)
        self.low_stock_threshold.setValue(5)
        
        layout.addWidget(currency_label)
        layout.addWidget(self.currency)
        layout.addWidget(language_label)
        layout.addWidget(self.language)
        layout.addWidget(tva_label)
        layout.addWidget(self.tva_rate)
        layout.addWidget(threshold_label)
        layout.addWidget(self.low_stock_threshold)
        layout.addStretch()
        
        return container
    
    def create_confirm_page(self):
        """Review and confirm settings."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(16)
        
        title = QLabel("Review & Confirm")
        title.setObjectName("title")
        
        subtitle = QLabel("Check your settings before proceeding")
        subtitle.setObjectName("subtitle")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        
        self.summary = QLabel()
        self.summary.setStyleSheet("color: #cbd5e1; line-height: 1.8; font-family: Courier;")
        self.summary.setWordWrap(True)
        
        layout.addWidget(self.summary)
        layout.addStretch()
        
        return container
    
    def update_summary(self):
        """Update the confirmation page summary."""
        summary_text = f"""
Business Name:        {self.business_name.text()}
Address:              {self.business_address.text()}
Phone:                {self.business_phone.text()}
Email:                {self.business_email.text()}

Username:             {self.username.text()}

Currency:             {self.currency.currentText()}
Language:             {self.language.currentText()}
VAT Rate:             {self.tva_rate.value()}%
Low Stock Threshold:  {self.low_stock_threshold.value()} units
        """.strip()
        self.summary.setText(summary_text)
    
    def show_page(self, page_num):
        """Display a specific page."""
        self.stack.setCurrentIndex(page_num)

        # Remove existing nav controls first (if any)
        if hasattr(self, 'nav_layout'):
            while self.nav_layout.count():
                item = self.nav_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        # Add navigation buttons
        self.nav_layout = QHBoxLayout()
        self.nav_layout.setSpacing(8)
        
        self.back_btn = QPushButton("← Back")
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setEnabled(page_num > 0)
        
        self.next_btn = QPushButton("Next →" if page_num < len(self.pages) - 1 else "Finish Setup")
        self.next_btn.setObjectName("next_btn")
        self.next_btn.clicked.connect(self.go_next)

        self.nav_layout.addWidget(self.back_btn)
        self.nav_layout.addStretch()
        self.nav_layout.addWidget(self.next_btn)

        # If nav widget was previously added, remove it first
        if hasattr(self, 'nav_widget') and self.nav_widget is not None:
            self.main_layout.removeWidget(self.nav_widget)
            self.nav_widget.deleteLater()

        self.nav_widget = QWidget()
        self.nav_widget.setLayout(self.nav_layout)
        self.main_layout.addWidget(self.nav_widget)

        self.current_page = page_num
    
    def go_back(self):
        """Go to previous page."""
        if self.current_page > 0:
            self.show_page(self.current_page - 1)
    
    def go_next(self):
        """Validate current page and go to next."""
        # Validate current page
        if not self.validate_page(self.current_page):
            return
        
        if self.current_page == len(self.pages) - 2:
            # Update summary before confirmation
            self.update_summary()
        
        if self.current_page < len(self.pages) - 1:
            self.show_page(self.current_page + 1)
        else:
            # Finish setup
            self.finish_setup()
    
    def validate_page(self, page_num):
        """Validate the current page data."""
        try:
            if page_num == 1:  # Business info
                if not self.business_name.text().strip():
                    QMessageBox.warning(self, "Validation Error", "Please enter a business name.")
                    return False
                if not self.business_address.text().strip():
                    QMessageBox.warning(self, "Validation Error", "Please enter a business address.")
                    return False
                return True
            
            elif page_num == 2:  # Credentials
                username = self.username.text().strip()
                password = self.password.text()
                confirm = self.confirm_password.text()
                
                if not username or len(username) < 3:
                    QMessageBox.warning(self, "Validation Error", "Username must be at least 3 characters.")
                    return False
                
                if len(password) < 6:
                    QMessageBox.warning(self, "Validation Error", "Password must be at least 6 characters.")
                    return False
                
                if password != confirm:
                    QMessageBox.warning(self, "Validation Error", "Passwords do not match.")
                    return False
                
                return True
            
            return True
        
        except Exception as e:
            logger.exception(f"Error validating page {page_num}")
            QMessageBox.critical(self, "Error", f"Validation error: {str(e)}")
            return False
    
    def finish_setup(self):
        """Save configuration and close wizard."""
        try:
            config = {
                "business_name": self.business_name.text().strip(),
                "business_address": self.business_address.text().strip(),
                "business_phone": self.business_phone.text().strip(),
                "business_email": self.business_email.text().strip(),
                "currency": self.currency.currentText(),
                "language": "fr" if self.language.currentText() == "Français" else "en",
                "tva_rate": float(self.tva_rate.value()),
                "low_stock_threshold": self.low_stock_threshold.value(),
                "username": self.username.text().strip(),
                "password": hash_password(self.password.text()),
            }
            
            save_settings(config)
            logger.info(f"First-run setup completed: business='{config['business_name']}'")
            
            QMessageBox.information(
                self,
                "Setup Complete",
                "5-Cinq Manager has been configured successfully!\n\n"
                "You can now log in with your credentials."
            )
            
            self.setup_complete.emit()
            self.accept()
        
        except Exception as e:
            logger.log_exception(e, "First-run setup finish")
            QMessageBox.critical(
                self,
                "Setup Error",
                f"Failed to save configuration:\n{str(e)}"
            )
