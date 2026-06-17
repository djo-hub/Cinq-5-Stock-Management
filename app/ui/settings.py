import os
import sys
import platform as _platform

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QLineEdit, QSpinBox, QStackedWidget,
    QScrollArea, QMessageBox, QSizePolicy, QApplication
)
from PyQt6.QtCore import Qt, PYQT_VERSION_STR
from app.config import load_settings, save_settings, SETTINGS_PATH, verify_password, hash_password
from app.i18n import t, get_language
from app.ui.icons import qicon, icon_pixmap

# ── Shared style constants ────────────────────────────────────────────────────
PAGE_STYLE = "background: #0f172a;"

CARD_STYLE = """
    QFrame#settings_card {
        background-color: #1e293b;
        border-radius: 12px;
        border: 1px solid #334155;
    }
"""

TAB_BTN_STYLE = """
    QPushButton {
        background-color: #1e293b;
        color: #94a3b8;
        border: 1px solid #334155;
        padding: 9px 20px;
        font-size: 13px;
        font-weight: bold;
        border-radius: 8px;
        min-width: 110px;
    }
    QPushButton:hover  { background-color: #263450; color: #f1f5f9; }
    QPushButton:checked {
        background-color: #f59e0b;
        color: white;
        border: 1px solid #f59e0b;
    }
"""

FIELD_STYLE = """
    QLineEdit, QSpinBox {
        background-color: #0f172a;
        color: #f1f5f9;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 13px;
        min-height: 18px;
    }
    QLineEdit:focus, QSpinBox:focus { border: 1px solid #f59e0b; }
    QSpinBox::up-button, QSpinBox::down-button {
        background: #1e293b;
        border-radius: 3px;
        width: 18px;
    }
    QSpinBox::up-button:hover, QSpinBox::down-button:hover { background: #334155; }
"""

SAVE_BTN_STYLE = """
    QPushButton {
        background: #f59e0b; color: white; border: none;
        padding: 10px 28px; border-radius: 8px;
        font-size: 13px; font-weight: bold;
    }
    QPushButton:hover { background: #d97706; }
"""

PASSWORD_LABEL_STYLE = "color: #64748b; font-size: 11px; padding-left: 2px;"

LANG_BTN_STYLE = """
    QPushButton {{
        background-color: #1e293b;
        color: #94a3b8;
        border: 2px solid #334155;
        border-radius: 10px;
        padding: 14px 20px;
        font-size: 14px;
        font-weight: bold;
        min-width: 180px;
        min-height: 50px;
    }}
    QPushButton:hover {{
        background-color: #263450;
        color: #f1f5f9;
        border-color: #475569;
    }}
"""

LANG_BTN_ACTIVE_STYLE = """
    QPushButton {{
        background-color: #f59e0b;
        color: white;
        border: 2px solid #f59e0b;
        border-radius: 10px;
        padding: 14px 20px;
        font-size: 14px;
        font-weight: bold;
        min-width: 180px;
        min-height: 50px;
    }}
"""


# ── Helpers ───────────────────────────────────────────────────────────────────

def _divider():
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFixedHeight(1)
    line.setStyleSheet("background-color: #334155; margin: 0px;")
    return line


def _section_header(icon_name: str, title: str) -> QWidget:
    """Small icon + uppercase label, like the dashboard section titles."""
    w = QWidget()
    w.setStyleSheet("background: transparent;")
    row = QHBoxLayout(w)
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(6)
    icon_lbl = QLabel()
    icon_lbl.setPixmap(icon_pixmap(icon_name, "#f59e0b", 18))
    icon_lbl.setStyleSheet("background: transparent;")
    title_lbl = QLabel(title)
    title_lbl.setStyleSheet(
        "color: #f59e0b; font-size: 12px; font-weight: bold; "
        "letter-spacing: 1px; background: transparent;"
    )
    row.addWidget(icon_lbl)
    row.addWidget(title_lbl)
    row.addStretch()
    return w


def _field_row(label_text: str, widget: QWidget) -> QWidget:
    """Label on left (fixed width) + input widget on right."""
    w = QWidget()
    w.setStyleSheet("background: transparent;")
    row = QHBoxLayout(w)
    row.setContentsMargins(0, 4, 0, 4)
    row.setSpacing(16)
    lbl = QLabel(label_text)
    lbl.setStyleSheet("color: #94a3b8; font-size: 13px; background: transparent;")
    lbl.setFixedWidth(190)
    row.addWidget(lbl)
    row.addWidget(widget)
    return w


def _make_line_edit(placeholder: str = "", echo_password: bool = False) -> QLineEdit:
    le = QLineEdit()
    le.setPlaceholderText(placeholder)
    le.setStyleSheet(FIELD_STYLE)
    if echo_password:
        le.setEchoMode(QLineEdit.EchoMode.Password)
    return le


def _info_row(label_text: str, value: str, copyable: bool = False) -> QWidget:
    """Read-only label pair used in the System tab."""
    w = QWidget()
    w.setStyleSheet("background: transparent;")
    row = QHBoxLayout(w)
    row.setContentsMargins(0, 4, 0, 4)
    row.setSpacing(16)
    lbl = QLabel(label_text)
    lbl.setStyleSheet("color: #64748b; font-size: 13px; background: transparent;")
    lbl.setFixedWidth(190)
    val = QLabel(value)
    val.setStyleSheet("color: #f1f5f9; font-size: 13px; background: transparent;")
    val.setWordWrap(True)
    val.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    row.addWidget(lbl)
    row.addWidget(val, 1)
    if copyable:
        copy_btn = QPushButton("Copy")
        copy_btn.setFixedWidth(54)
        copy_btn.setStyleSheet(
            "QPushButton { background: #1e293b; color: #94a3b8; border: 1px solid #334155;"
            " border-radius: 5px; padding: 4px 8px; font-size: 11px; }"
            "QPushButton:hover { background: #263450; color: #f1f5f9; }"
        )
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(value))
        row.addWidget(copy_btn)
    return w


def _settings_card(inner_layout: QVBoxLayout) -> QFrame:
    """Wraps a VBoxLayout in a styled card frame."""
    card = QFrame()
    card.setObjectName("settings_card")
    card.setStyleSheet(CARD_STYLE)
    card.setLayout(inner_layout)
    return card


# ── Individual tab pages ──────────────────────────────────────────────────────

class BusinessTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # ── Card ──
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(24, 20, 24, 24)
        card_layout.setSpacing(12)

        card_layout.addWidget(_section_header("business", t("settings.biz_header")))
        card_layout.addWidget(_divider())
        card_layout.addSpacing(4)

        cfg = load_settings()

        self.name_input    = _make_line_edit("e.g. MY BUSINESS")
        self.address_input = _make_line_edit("e.g. 123 Street, Algiers")
        self.phone_input   = _make_line_edit("e.g. +213 XX XX XX XX")
        self.email_input   = _make_line_edit("e.g. contact@mybusiness.com")

        self.name_input.setText(cfg.get("business_name", ""))
        self.address_input.setText(cfg.get("business_address", ""))
        self.phone_input.setText(cfg.get("business_phone", ""))
        self.email_input.setText(cfg.get("business_email", ""))

        card_layout.addWidget(_field_row(t("settings.biz_name"),    self.name_input))
        card_layout.addWidget(_field_row(t("settings.biz_address"),          self.address_input))
        card_layout.addWidget(_field_row(t("settings.biz_phone"),     self.phone_input))
        card_layout.addWidget(_field_row(t("settings.biz_email"),    self.email_input))

        layout.addWidget(_settings_card(card_layout))

        hint = QLabel(t("settings.biz_hint"))
        hint.setStyleSheet("color: #64748b; font-size: 11px; padding-left: 4px;")
        layout.addWidget(hint)

    def collect(self) -> dict:
        return {
            "business_name":    self.name_input.text().strip(),
            "business_address": self.address_input.text().strip(),
            "business_phone":   self.phone_input.text().strip(),
            "business_email":   self.email_input.text().strip(),
        }


class InvoiceTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        cfg = load_settings()

        # ── Card ──
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(24, 20, 24, 24)
        card_layout.setSpacing(12)

        card_layout.addWidget(_section_header("invoice", t("settings.inv_header")))
        card_layout.addWidget(_divider())
        card_layout.addSpacing(4)

        self.currency_input = _make_line_edit("e.g. DA")
        self.currency_input.setText(cfg.get("currency", "DA"))
        self.currency_input.setMaximumWidth(120)

        self.tva_input = _make_line_edit("e.g. 19.0")
        self.tva_input.setText(str(cfg.get("tva_rate", 0.0)))
        self.tva_input.setMaximumWidth(120)

        self.threshold_spin = QSpinBox()
        self.threshold_spin.setStyleSheet(FIELD_STYLE)
        self.threshold_spin.setRange(1, 9999)
        self.threshold_spin.setValue(int(cfg.get("low_stock_threshold", 5)))
        self.threshold_spin.setMaximumWidth(120)

        card_layout.addWidget(_field_row(t("settings.inv_currency"),      self.currency_input))
        card_layout.addWidget(_field_row(t("settings.inv_tva"),            self.tva_input))
        card_layout.addWidget(_field_row(t("settings.inv_threshold"),  self.threshold_spin))

        layout.addWidget(_settings_card(card_layout))

        hint = QLabel(t("settings.inv_hint"))
        hint.setStyleSheet("color: #64748b; font-size: 11px; padding-left: 4px;")
        layout.addWidget(hint)
        layout.addStretch()

    def collect(self) -> dict:
        return {
            "currency":            self.currency_input.text().strip() or "DA",
            "tva_rate":            float(self.tva_input.text().strip() or 0.0),
            "low_stock_threshold": self.threshold_spin.value(),
        }


class SecurityTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # ── Username card ──
        user_layout = QVBoxLayout()
        user_layout.setContentsMargins(24, 20, 24, 24)
        user_layout.setSpacing(12)

        user_layout.addWidget(_section_header("account", t("settings.sec_login")))
        user_layout.addWidget(_divider())
        user_layout.addSpacing(4)

        cfg = load_settings()

        self.username_input = _make_line_edit(t("settings.sec_username"))
        self.username_input.setText(cfg.get("username", "admin"))

        user_layout.addWidget(_field_row(t("settings.sec_username"), self.username_input))
        layout.addWidget(_settings_card(user_layout))

        # ── Password card ──
        pwd_layout = QVBoxLayout()
        pwd_layout.setContentsMargins(24, 20, 24, 24)
        pwd_layout.setSpacing(12)

        pwd_layout.addWidget(_section_header("lock", t("settings.sec_change_pwd")))
        pwd_layout.addWidget(_divider())
        pwd_layout.addSpacing(4)

        self.current_pwd   = _make_line_edit(t("settings.sec_current"),  echo_password=True)
        self.new_pwd       = _make_line_edit(t("settings.sec_new"),       echo_password=True)
        self.confirm_pwd   = _make_line_edit(t("settings.sec_confirm"), echo_password=True)

        pwd_layout.addWidget(_field_row(t("settings.sec_current"),  self.current_pwd))
        pwd_layout.addWidget(_field_row(t("settings.sec_new"),      self.new_pwd))
        pwd_layout.addWidget(_field_row(t("settings.sec_confirm"),  self.confirm_pwd))

        hint = QLabel(t("settings.sec_hint"))
        hint.setStyleSheet(PASSWORD_LABEL_STYLE)
        pwd_layout.addWidget(hint)

        layout.addWidget(_settings_card(pwd_layout))

    def validate_and_collect(self) -> dict | None:
        """Returns updated security fields or None if validation fails."""
        cfg = load_settings()
        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(None, t("common.validation"), t("settings.sec_empty_user"))
            return None

        cur  = self.current_pwd.text()
        new  = self.new_pwd.text()
        conf = self.confirm_pwd.text()

        # If any password field is filled, treat it as a password change
        if cur or new or conf:
            if not verify_password(cur, cfg.get("password", "")):
                QMessageBox.warning(None, t("common.validation"), t("settings.sec_wrong_pwd"))
                return None
            if not new:
                QMessageBox.warning(None, t("common.validation"), t("settings.sec_empty_new"))
                return None
            if new != conf:
                QMessageBox.warning(None, t("common.validation"), t("settings.sec_mismatch"))
                return None
            return {"username": username, "password": hash_password(new)}

        return {"username": username}


class LanguageTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(24, 20, 24, 24)
        card_layout.setSpacing(16)

        card_layout.addWidget(_section_header("language", t("settings.lang_header")))
        card_layout.addWidget(_divider())
        card_layout.addSpacing(8)

        # Language buttons
        self.selected_lang = get_language()

        btn_row = QHBoxLayout()
        btn_row.setSpacing(16)

        self.en_btn = QPushButton("  English")
        self.en_btn.setIcon(qicon("language", "#f1f5f9"))
        self.fr_btn = QPushButton("  Français")
        self.fr_btn.setIcon(qicon("language", "#f1f5f9"))

        for btn in [self.en_btn, self.fr_btn]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.en_btn.clicked.connect(lambda: self._select("en"))
        self.fr_btn.clicked.connect(lambda: self._select("fr"))

        btn_row.addWidget(self.en_btn)
        btn_row.addWidget(self.fr_btn)
        btn_row.addStretch()

        card_layout.addLayout(btn_row)
        self._update_btn_styles()

        layout.addWidget(_settings_card(card_layout))

        hint = QLabel(t("settings.lang_hint"))
        hint.setStyleSheet("color: #64748b; font-size: 11px; padding-left: 4px;")
        layout.addWidget(hint)

    def _select(self, lang: str):
        self.selected_lang = lang
        self._update_btn_styles()

    def _update_btn_styles(self):
        if self.selected_lang == "en":
            self.en_btn.setStyleSheet(LANG_BTN_ACTIVE_STYLE)
            self.fr_btn.setStyleSheet(LANG_BTN_STYLE)
        else:
            self.en_btn.setStyleSheet(LANG_BTN_STYLE)
            self.fr_btn.setStyleSheet(LANG_BTN_ACTIVE_STYLE)

    def collect(self) -> dict:
        return {"language": self.selected_lang}


class SystemTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # ── About the application ──
        about_layout = QVBoxLayout()
        about_layout.setContentsMargins(24, 20, 24, 24)
        about_layout.setSpacing(12)
        about_layout.addWidget(_section_header("info", t("settings.sys_about")))
        about_layout.addWidget(_divider())
        about_layout.addSpacing(4)
        about_layout.addWidget(_info_row(t("settings.sys_app_name"), "5-Cinq Manager"))
        about_layout.addWidget(_info_row(t("settings.sys_version"),          "1.0.0"))
        about_layout.addWidget(_info_row(t("settings.sys_release"),     "March 2026"))
        about_layout.addWidget(_info_row(t("settings.sys_description"),
            t("settings.sys_desc_text")))
        about_layout.addWidget(_info_row(t("settings.sys_license"), t("settings.sys_license_text")))
        layout.addWidget(_settings_card(about_layout))

        # ── Developer information ──
        dev_layout = QVBoxLayout()
        dev_layout.setContentsMargins(24, 20, 24, 24)
        dev_layout.setSpacing(12)
        dev_layout.addWidget(_section_header("developer", t("settings.sys_dev")))
        dev_layout.addWidget(_divider())
        dev_layout.addSpacing(4)
        dev_layout.addWidget(_info_row(t("settings.sys_developer"),   "5-Cinq Dev By : Abid Djoghlal"))
        dev_layout.addWidget(_info_row(t("settings.sys_contact"),     "djoghlal.abid@univ-khenchela.dz"))
        dev_layout.addWidget(_info_row(t("settings.sys_built_with"),
            "Python  ·  PyQt6  ·  SQLite  ·  SQLAlchemy"))
        layout.addWidget(_settings_card(dev_layout))

        # ── Database Backup ──
        backup_layout = QVBoxLayout()
        backup_layout.setContentsMargins(24, 20, 24, 24)
        backup_layout.setSpacing(12)
        backup_layout.addWidget(_section_header("backup", "DATABASE BACKUP"))
        backup_layout.addWidget(_divider())
        backup_layout.addSpacing(4)

        backup_btn = QPushButton(f"  {t('settings.backup_btn')}")
        backup_btn.setIcon(qicon("backup", "#f1f5f9"))
        backup_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        backup_btn.setStyleSheet(
            "QPushButton { background: #22c55e; color: white; border: none;"
            " border-radius: 8px; padding: 10px 24px; font-size: 13px; font-weight: bold; }"
            "QPushButton:hover { background: #16a34a; }"
        )
        backup_btn.clicked.connect(self._download_backup)
        backup_layout.addWidget(backup_btn)

        layout.addWidget(_settings_card(backup_layout))

    def _download_backup(self):
        from PyQt6.QtWidgets import QFileDialog
        from datetime import datetime
        import shutil

        # Locate the database file
        from app.database import _db_path

        default_name = f"business_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        dest, _ = QFileDialog.getSaveFileName(
            self, t("settings.backup_btn"), default_name,
            "SQLite Database (*.db);;All Files (*)"
        )
        if not dest:
            return  # user cancelled

        try:
            shutil.copy2(_db_path, dest)
            QMessageBox.information(
                self, t("settings.backup_ok_title"),
                t("settings.backup_ok_msg", path=dest)
            )
        except Exception as e:
            QMessageBox.critical(
                self, t("common.error"),
                t("settings.backup_err", error=str(e))
            )



# ── Main Settings Widget ──────────────────────────────────────────────────────

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(PAGE_STYLE)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # Scrollable container
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }"
                             "QScrollBar:vertical { background: #1e293b; width: 8px; border-radius: 4px; }"
                             "QScrollBar::handle:vertical { background: #334155; border-radius: 4px; }")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        main = QVBoxLayout(container)
        main.setContentsMargins(30, 30, 30, 30)
        main.setSpacing(20)

        # ── Page title ──
        title = QLabel(t("settings.title"))
        title.setStyleSheet("color: #f1f5f9; font-size: 28px; font-weight: bold;")
        main.addWidget(title)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #1e293b;")
        main.addWidget(sep)

        # ── Tab bar ──
        tab_bar = QHBoxLayout()
        tab_bar.setSpacing(8)
        tab_bar.setContentsMargins(0, 0, 0, 0)

        self.tab_buttons: list[QPushButton] = []
        tabs = [
            ("business", t("settings.tab_business")),
            ("invoice", t("settings.tab_invoice")),
            ("security", t("settings.tab_security")),
            ("language", t("settings.tab_language")),
            ("system", t("settings.tab_system")),
        ]
        for icon_name, label in tabs:
            btn = QPushButton(f"  {label}")
            btn.setIcon(qicon(icon_name, "#94a3b8"))
            btn.setCheckable(True)
            btn.setStyleSheet(TAB_BTN_STYLE)
            btn.clicked.connect(lambda _, b=btn: self._switch_tab(b))
            tab_bar.addWidget(btn)
            self.tab_buttons.append(btn)

        tab_bar.addStretch()
        main.addLayout(tab_bar)

        # ── Tab content stack ──
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: transparent;")

        self.business_tab = BusinessTab()
        self.invoice_tab  = InvoiceTab()
        self.security_tab = SecurityTab()
        self.language_tab = LanguageTab()
        self.system_tab   = SystemTab()

        self.stack.addWidget(self.business_tab)
        self.stack.addWidget(self.invoice_tab)
        self.stack.addWidget(self.security_tab)
        self.stack.addWidget(self.language_tab)
        self.stack.addWidget(self.system_tab)

        main.addWidget(self.stack)
        main.addStretch()

        scroll.setWidget(container)
        outer.addWidget(scroll)

        # ── Separator line ──
        sep_footer = QFrame()
        sep_footer.setFrameShape(QFrame.Shape.HLine)
        sep_footer.setFixedHeight(1)
        sep_footer.setStyleSheet("background-color: #1e293b;")
        outer.addWidget(sep_footer)

        # ── Save button (fixed footer, outside scroll area) ──
        self.save_btn_container = QWidget()
        self.save_btn_container.setStyleSheet("background: transparent;")
        btn_row = QHBoxLayout(self.save_btn_container)
        btn_row.setContentsMargins(30, 16, 30, 16)
        btn_row.addStretch()
        save_btn = QPushButton(t("settings.save"))
        save_btn.setStyleSheet(SAVE_BTN_STYLE)
        save_btn.clicked.connect(self._save)
        btn_row.addWidget(save_btn)
        outer.addWidget(self.save_btn_container)

        # Select first tab
        self.tab_buttons[0].setChecked(True)
        self.stack.setCurrentIndex(0)

    # ── Slots ─────────────────────────────────────────────────────────────────

    def _switch_tab(self, clicked_btn: QPushButton):
        for i, btn in enumerate(self.tab_buttons):
            btn.setChecked(btn is clicked_btn)
            if btn is clicked_btn:
                self.stack.setCurrentIndex(i)
                # Hide save button on System tab (index 4) — it's read-only
                self.save_btn_container.setVisible(i != 4)

    def _save(self):
        cfg = load_settings()

        # Collect business
        cfg.update(self.business_tab.collect())

        # Collect invoice
        cfg.update(self.invoice_tab.collect())

        # Collect security (with validation)
        sec = self.security_tab.validate_and_collect()
        if sec is None:
            return  # validation failed — abort save
        cfg.update(sec)

        # Collect language
        cfg.update(self.language_tab.collect())

        save_settings(cfg)

        # Clear password fields after save
        self.security_tab.current_pwd.clear()
        self.security_tab.new_pwd.clear()
        self.security_tab.confirm_pwd.clear()

        QMessageBox.information(self, t("settings.saved_title"), t("settings.saved_msg"))

    def refresh(self):
        """Re-load values when navigating back to this page."""
        cfg = load_settings()

        self.business_tab.name_input.setText(cfg.get("business_name", ""))
        self.business_tab.address_input.setText(cfg.get("business_address", ""))
        self.business_tab.phone_input.setText(cfg.get("business_phone", ""))
        self.business_tab.email_input.setText(cfg.get("business_email", ""))

        self.invoice_tab.currency_input.setText(cfg.get("currency", "DA"))
        self.invoice_tab.threshold_spin.setValue(int(cfg.get("low_stock_threshold", 5)))

        self.security_tab.username_input.setText(cfg.get("username", "admin"))
        self.security_tab.current_pwd.clear()
        self.security_tab.new_pwd.clear()
        self.security_tab.confirm_pwd.clear()

        # Refresh language tab selection
        self.language_tab.selected_lang = cfg.get("language", "en")
        self.language_tab._update_btn_styles()
