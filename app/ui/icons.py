"""
Centralised icon helper using qtawesome (Material Design Icons 6).

Usage:
    from app.ui.icons import qicon, icon_pixmap
    btn.setIcon(qicon("check_circle", "#22c55e"))
    lbl.setPixmap(icon_pixmap("package", "#3498db", 24))
"""

import qtawesome as qta
from PyQt6.QtGui import QIcon, QPixmap

# ── Icon name registry ─────────────────────────────────────────────────────
# Mapping of short friendly names → qtawesome icon identifiers (mdi6 set).
ICONS = {
    # Dashboard stat cards
    "package":           "mdi6.package-variant",
    "check_circle":      "mdi6.check-circle",
    "alert_circle":      "mdi6.alert-circle",
    "close_circle":      "mdi6.close-circle",
    "cash_multiple":     "mdi6.cash-multiple",
    "file_alert":        "mdi6.file-document-alert-outline",
    "cash_off":          "mdi6.cash-remove",
    "chart_bar":         "mdi6.chart-bar",

    # Dashboard out-of-stock list
    "alert_dot":         "mdi6.alert-decagram",
    "check_outline":     "mdi6.check-circle-outline",

    # Action buttons
    "mark_paid":         "mdi6.check-decagram",
    "mark_unpaid":       "mdi6.close-octagon",
    "pdf":               "mdi6.file-pdf-box",
    "trash":             "mdi6.trash-can-outline",
    "pencil":            "mdi6.pencil-outline",
    "plus_circle":       "mdi6.plus-circle",
    "cash_plus":         "mdi6.cash-plus",
    "magnify":           "mdi6.magnify",

    # Sidebar
    "dashboard":         "mdi6.view-dashboard",
    "products":          "mdi6.package-variant-closed",
    "suppliers":         "mdi6.truck-delivery",
    "clients":           "mdi6.account-group",
    "invoices":          "mdi6.receipt",
    "debts":             "mdi6.credit-card-clock-outline",
    "settings":          "mdi6.cog",
    "logout":            "mdi6.logout",

    # Misc
    "add_item":          "mdi6.plus-box",
    "delete_row":        "mdi6.trash-can",
    "gear":              "mdi6.cog-outline",

    # Settings tabs & section headers
    "business":          "mdi6.office-building",
    "invoice":           "mdi6.file-document-outline",
    "security":          "mdi6.shield-lock",
    "language":          "mdi6.web",
    "system":            "mdi6.monitor",
    "info":              "mdi6.information-outline",
    "developer":         "mdi6.code-braces",
    "account":           "mdi6.account",
    "lock":              "mdi6.lock",
    "save":              "mdi6.content-save",
    "backup":            "mdi6.database-export",
}


def qicon(name: str, color: str = "white", size: int = 18) -> QIcon:
    """Return a QIcon for the given friendly name."""
    icon_id = ICONS.get(name, name)  # fallback: use raw name
    return qta.icon(icon_id, color=color, options=[{"scale_factor": 1.0}])


def icon_pixmap(name: str, color: str = "white", size: int = 24) -> QPixmap:
    """Return a QPixmap for the given friendly name (useful for QLabels)."""
    icon_id = ICONS.get(name, name)
    ico = qta.icon(icon_id, color=color)
    return ico.pixmap(size, size)
