"""
Internationalization module — English / French translations.
Usage:  from app.i18n import t
        label.setText(t("sidebar.dashboard"))
"""

from app.config import load_settings

# ── Translation dictionaries ─────────────────────────────────────────────────

EN = {
    # ── Sidebar / Main Window ──
    "sidebar.dashboard":    "Dashboard",
    "sidebar.products":     "Products",
    "sidebar.suppliers":    "Suppliers",
    "sidebar.clients":      "Clients",
    "sidebar.invoices":     "Invoices",
    "sidebar.debts":        "Debts",
    "sidebar.settings":     "Settings",
    "sidebar.logout":       "Logout",
    "window.title":         "5-Cinq Manager",
    "logout.confirm_title": "Confirm Logout",
    "logout.confirm_msg":   "Are you sure you want to logout?",

    # ── Login ──
    "login.title":          "5-Cinq Manager",
    "login.subtitle":       "Sign in to continue",
    "login.username":       "Username",
    "login.password":       "Password",
    "login.btn":            "Login",
    "login.failed_title":   "Login Failed",
    "login.failed_msg":     "Invalid username or password.",

    # ── Dashboard ──
    "dash.title":           "Dashboard Overview",
    "dash.section_stock":   "PRODUCTS & STOCK",
    "dash.section_finance": "FINANCE",
    "dash.section_analytics":"ANALYTICS",
    "dash.section_revenue": "MONTHLY REVENUE",
    "dash.section_oos":     "OUT OF STOCK PRODUCTS",
    "dash.chart_revenue":   "Revenue Over Months",
    "dash.chart_profit":    "Profit Over Months",
    "dash.chart_month":     "Month",
    "dash.chart_amount":    "Amount",
    "dash.total_products":  "TOTAL PRODUCTS",
    "dash.total_in_stock":  "TOTAL IN STOCK",
    "dash.low_stock":       "LOW STOCK ITEMS",
    "dash.out_of_stock":    "OUT OF STOCK",
    "dash.total_income":    "TOTAL INCOME (DA)",
    "dash.unpaid_invoices": "UNPAID INVOICES",
    "dash.total_debts":     "TOTAL DEBTS (DA)",
    "dash.total_profit":    "TOTAL PROFIT (DA)",
    "dash.profit_hint":     "Revenue \u2212 Cost",
    "dash.paid_only":       "Paid invoices only",
    "dash.stock_label":     "Stock: {qty}",
    "dash.all_in_stock":    "All products are in stock.",
    "dash.units":           "≤ {n} units",

    # ── Base Table ──
    "table.add":            "Add",
    "table.search":         "Search...",
    "table.prev":           "← Prev",
    "table.next":           "Next →",
    "table.showing":        "Showing {start}–{end} of {total} items",
    "table.no_items":       "No items",
    "table.sort_default":   "Sort: Default",
    "table.sort_low_high":  "{col} ↑ Low to High",
    "table.sort_high_low":  "{col} ↓ High to Low",

    # ── Products ──
    "products.title":       "Products & Stock",
    "products.col_id":      "ID",
    "products.col_barcode": "Barcode",
    "products.col_name":    "Name",
    "products.col_category":"Category",
    "products.col_price":   "Price (DA)",
    "products.col_stock":   "Stock",
    "products.col_unit":    "Unit",
    "products.edit":        "Edit",
    "products.delete":      "Delete",
    "products.add_title":   "New Product",
    "products.edit_title":  "Edit Product",
    "products.add_win":     "Add New Product",
    "products.edit_win":    "Edit Product",
    "products.name":        "Name:",
    "products.barcode":     "Barcode:",
    "products.category":    "Category:",
    "products.supplier":    "Supplier:",
    "products.price":       "Price:",
    "products.cost_price":  "Cost Price:",
    "products.stock_qty":   "Stock Qty:",
    "products.unit":        "Unit:",
    "products.save":        "Save Product",
    "products.update":      "Update Product",
    "products.cancel":      "Cancel",
    "products.name_req":    "Product name is required.",
    "products.del_confirm": "Delete product '{name}'?",
    "products.select_first":"Select a product first.",
    "products.none_supplier":"— None —",

    # ── Categories ──
    "cat.title":            "Manage Categories",
    "cat.win_title":        "Manage Categories",
    "cat.placeholder":      "New category name...",
    "cat.add":              "＋ Add",
    "cat.delete":           "Delete Selected",
    "cat.close":            "Close",
    "cat.select_warn":      "Select a category to delete.",
    "cat.del_confirm":      "Delete category '{name}'?",

    # ── Suppliers ──
    "suppliers.title":      "Suppliers",
    "suppliers.col_id":     "ID",
    "suppliers.col_company":"Company",
    "suppliers.col_contact":"Contact",
    "suppliers.col_phone":  "Phone",
    "suppliers.col_email":  "Email",
    "suppliers.col_products":"Products",
    "suppliers.edit":       "Edit",
    "suppliers.delete":     "Delete",
    "suppliers.add_title":  "New Supplier",
    "suppliers.edit_title": "Edit Supplier",
    "suppliers.add_win":    "Add New Supplier",
    "suppliers.edit_win":   "Edit Supplier",
    "suppliers.company":    "Company Name:",
    "suppliers.contact":    "Contact Person:",
    "suppliers.phone":      "Phone:",
    "suppliers.email":      "Email:",
    "suppliers.address":    "Address:",
    "suppliers.notes":      "Notes:",
    "suppliers.save":       "Save Supplier",
    "suppliers.update":     "Update Supplier",
    "suppliers.cancel":     "Cancel",
    "suppliers.name_req":   "Company name is required.",
    "suppliers.del_confirm":"Delete supplier '{name}'?",
    "suppliers.del_unlink": "\n\n⚠️  {count} product(s) will be unlinked (not deleted).",
    "suppliers.select_first":"Select a supplier first.",

    # ── Clients ──
    "clients.title":        "Clients",
    "clients.col_id":       "ID",
    "clients.col_name":     "Name",
    "clients.col_phone":    "Phone",
    "clients.col_email":    "Email",
    "clients.col_address":  "Address",
    "clients.edit":         "Edit",
    "clients.delete":       "Delete",
    "clients.add_title":    "New Client",
    "clients.edit_title":   "Edit Client",
    "clients.add_win":      "Add New Client",
    "clients.edit_win":     "Edit Client",
    "clients.name":         "Name:",
    "clients.phone":        "Phone:",
    "clients.email":        "Email:",
    "clients.address":      "Address:",
    "clients.save":         "Save Client",
    "clients.update":       "Update Client",
    "clients.cancel":       "Cancel",
    "clients.name_req":     "Client name is required.",
    "clients.del_confirm":  "Delete client '{name}'?",
    "clients.select_first": "Select a client first.",

    # ── Invoices ──
    "invoices.title":       "Invoices",
    "invoices.col_id":      "ID",
    "invoices.col_client":  "Client",
    "invoices.col_date":    "Date",
    "invoices.col_total":   "Total (DA)",
    "invoices.col_status":  "Status",
    "invoices.new":         "New Invoice",
    "invoices.mark_paid":   "Mark Paid",
    "invoices.mark_unpaid": "Mark Unpaid",
    "invoices.print_pdf":   "Print PDF",
    "invoices.delete":      "Delete",
    "invoices.select_first":"Select an invoice first.",
    "invoices.del_confirm": "Delete Invoice #{id} for {client} ({total} DA)?\n\nThis will also remove the linked debt.",
    "invoices.new_title":   "New Invoice",
    "invoices.new_win":     "New Invoice",
    "invoices.client":      "Client:",
    "invoices.col_product": "Product",
    "invoices.col_available":"Available",
    "invoices.col_qty":     "Qty",
    "invoices.col_unit_price":"Unit Price",
    "invoices.col_subtotal":"Subtotal",
    "invoices.add_item":    "Add Item",
    "invoices.total":       "Total: {amount} DA",
    "invoices.save":        "Save Invoice",
    "invoices.cancel":      "Cancel",
    "invoices.pick_product":"— click to pick —",
    "invoices.no_product":  "Row {row}: No product selected.\nClick the product name to pick one.",
    "invoices.min_item":    "Add at least one item.",
    "invoices.insuff_stock":"❌ Cannot save invoice!\n\nProduct: {product}\nAvailable: {available}\nRequested: {requested}\n\nPlease reduce the quantity.",
    "invoices.insuff_title":"Insufficient Stock",

    # ── Debts ──
    "debts.title":          "Debts & Payments",
    "debts.col_id":         "ID",
    "debts.col_client":     "Client",
    "debts.col_due":        "Due",
    "debts.col_paid":       "Paid",
    "debts.col_remaining":  "Remaining",
    "debts.col_status":     "Status",
    "debts.record_payment": "Record Payment",
    "debts.select_first":   "Select a debt row first.",
    "debts.pay_title":      "Record Payment",
    "debts.pay_amount":     "Amount Paid (DA):",

    # ── Client Profile ──
    "profile.total_invoices":   "Total Invoices",
    "profile.total_spent":      "Total Spent",
    "profile.outstanding_debt": "Outstanding Debt",
    "profile.paid_unpaid":      "Paid / Unpaid",
    "profile.invoice_history":  "Invoice History",
    "profile.col_id":           "ID",
    "profile.col_date":         "Date",
    "profile.col_total":        "Total (DA)",
    "profile.col_status":       "Status",
    "profile.view":             "View",
    "profile.close":            "Close",

    # ── Invoice Detail ──
    "inv_detail.col_product":   "Product",
    "inv_detail.col_qty":       "Qty",
    "inv_detail.col_unit_price":"Unit Price",
    "inv_detail.col_subtotal":  "Subtotal",
    "inv_detail.total":         "Total:  {amount} DA",
    "inv_detail.print_pdf":     "Print PDF",
    "inv_detail.close":         "Close",
    "inv_detail.mark_paid":     "Mark as Paid",
    "inv_detail.mark_unpaid":   "Mark as Unpaid",

    # ── Supplier Profile ──
    "sup_profile.total_products":   "Total Products",
    "sup_profile.categories":       "Categories",
    "sup_profile.units_in_stock":   "Units in Stock",
    "sup_profile.stock_value":      "Stock Value (DA)",
    "sup_profile.supplied_products":"Supplied Products",
    "sup_profile.col_id":           "ID",
    "sup_profile.col_name":         "Name",
    "sup_profile.col_category":     "Category",
    "sup_profile.col_price":        "Price (DA)",
    "sup_profile.col_stock":        "Stock",
    "sup_profile.close":            "Close",
    "sup_profile.no_contact":       "No contact details",

    # ── Product Picker ──
    "picker.title":         "Select a Product",
    "picker.win_title":     "Select Product",
    "picker.search":        "Search by name, category, barcode...",
    "picker.out_of_stock":  "Out of stock",
    "picker.stock":         "Stock: {qty}",
    "picker.count":         "{total} products  •  {in_stock} in stock  •  {out} out of stock",

    # ── Settings ──
    "settings.title":       "Settings",
    "settings.tab_business":"Business",
    "settings.tab_invoice": "Invoice",
    "settings.tab_security":"Security",
    "settings.tab_language":"Language",
    "settings.tab_system":  "System",
    "settings.save":        "Save Changes",
    "settings.saved_title": "Settings Saved",
    "settings.saved_msg":   "Your settings have been saved successfully.\nChanges to business info will apply to new invoices.",

    # Settings — Business
    "settings.biz_header":      "BUSINESS INFORMATION",
    "settings.biz_name":        "Business Name",
    "settings.biz_address":     "Address",
    "settings.biz_phone":       "Phone Number",
    "settings.biz_email":       "Email Address",
    "settings.biz_hint":        "These details appear on every generated invoice PDF.",

    # Settings — Invoice
    "settings.inv_header":      "INVOICE & STOCK PARAMETERS",
    "settings.inv_currency":    "Currency Symbol",
    "settings.inv_tva":         "TVA Rate (%)",
    "settings.inv_threshold":   "Low Stock Threshold",
    "settings.inv_hint":        "Currency symbol is shown on invoices and debt records.\nProducts at or below the low-stock threshold are flagged on the dashboard.",

    # Settings — Security
    "settings.sec_login":       "LOGIN CREDENTIALS",
    "settings.sec_username":    "Username",
    "settings.sec_change_pwd":  "CHANGE PASSWORD",
    "settings.sec_current":     "Current Password",
    "settings.sec_new":         "New Password",
    "settings.sec_confirm":     "Confirm Password",
    "settings.sec_hint":        "Leave password fields blank to keep the current password.",
    "settings.sec_empty_user":  "Username cannot be empty.",
    "settings.sec_wrong_pwd":   "Current password is incorrect.",
    "settings.sec_empty_new":   "New password cannot be empty.",
    "settings.sec_mismatch":    "New passwords do not match.",

    # Settings — Language
    "settings.lang_header":     "LANGUAGE / LANGUE",
    "settings.lang_hint":       "The interface language will change after restarting the application.",

    # Settings — System
    "settings.sys_about":       "ABOUT THE APPLICATION",
    "settings.sys_app_name":    "Application Name",
    "settings.sys_version":     "Version",
    "settings.sys_release":     "Release Date",
    "settings.sys_description": "Description",
    "settings.sys_desc_text":   "Desktop business management — invoices, clients, stock & debts",
    "settings.sys_license":     "License",
    "settings.sys_license_text":"Private / All rights reserved",
    "settings.sys_dev":         "DEVELOPER INFORMATION",
    "settings.sys_developer":   "Developer",
    "settings.sys_contact":     "Contact",
    "settings.sys_built_with":  "Built With",
    "settings.backup_btn":      "Download Backup",
    "settings.backup_ok_title": "Backup Complete",
    "settings.backup_ok_msg":   "Database backed up successfully to:\n{path}",
    "settings.backup_err":      "Backup failed: {error}",

    # ── Status ──
    "status.paid":          "PAID",
    "status.unpaid":        "UNPAID",
    "status.paid_lower":    "paid",
    "status.unpaid_lower":  "unpaid",
    "status.pending":       "Pending",
    "status.settled":       "Settled",

    # ── PDF ──
    "pdf.invoice_num":      "Invoice #:",
    "pdf.date":             "Date:",
    "pdf.client":           "Client:",
    "pdf.phone":            "Phone:",
    "pdf.col_num":          "#",
    "pdf.col_product":      "Product",
    "pdf.col_qty":          "Qty",
    "pdf.col_unit_price":   "Unit Price",
    "pdf.col_total":        "Total",
    "pdf.total":            "TOTAL",
    "pdf.subtotal":         "SUBTOTAL",
    "pdf.tva":              "TVA ({rate}%)",
    "pdf.status":           "Status:",
    "pdf.notes":            "Notes:",

    # ── Date ──
    "date.format":          "{weekday}, {month} {day} {year}",

    # Common
    "common.validation":    "Validation",
    "common.warning":       "Warning",
    "common.error":         "Error",
    "common.confirm":       "Confirm",
    "common.confirm_delete":"Confirm Delete",
    "common.yes":           "Yes",
    "common.no":            "No",
}

FR = {
    # ── Sidebar / Main Window ──
    "sidebar.dashboard":    "Tableau de bord",
    "sidebar.products":     "Produits",
    "sidebar.suppliers":    "Fournisseurs",
    "sidebar.clients":      "Clients",
    "sidebar.invoices":     "Factures",
    "sidebar.debts":        "Dettes",
    "sidebar.settings":     "Paramètres",
    "sidebar.logout":       "Déconnexion",
    "window.title":         "5-Cinq Manager",
    "logout.confirm_title": "Confirmer la déconnexion",
    "logout.confirm_msg":   "Êtes-vous sûr de vouloir vous déconnecter ?",

    # ── Login ──
    "login.title":          "5-Cinq Manager",
    "login.subtitle":       "Connectez-vous pour continuer",
    "login.username":       "Nom d'utilisateur",
    "login.password":       "Mot de passe",
    "login.btn":            "Connexion",
    "login.failed_title":   "Échec de connexion",
    "login.failed_msg":     "Nom d'utilisateur ou mot de passe invalide.",

    # ── Dashboard ──
    "dash.title":           "Aperçu du tableau de bord",
    "dash.section_stock":   "PRODUITS & STOCK",
    "dash.section_finance": "FINANCES",
    "dash.section_analytics":"ANALYTIQUE",
    "dash.section_revenue": "REVENU MENSUEL",
    "dash.section_oos":     "PRODUITS EN RUPTURE DE STOCK",
    "dash.chart_revenue":   "Revenu sur les mois",
    "dash.chart_profit":    "Profit sur les mois",
    "dash.chart_month":     "Mois",
    "dash.chart_amount":    "Montant",
    "dash.total_products":  "TOTAL PRODUITS",
    "dash.total_in_stock":  "TOTAL EN STOCK",
    "dash.low_stock":       "STOCK FAIBLE",
    "dash.out_of_stock":    "RUPTURE DE STOCK",
    "dash.total_income":    "REVENU TOTAL (DA)",
    "dash.unpaid_invoices": "FACTURES IMPAYÉES",
    "dash.total_debts":     "TOTAL DETTES (DA)",
    "dash.total_profit":    "BÉNÉFICE TOTAL (DA)",
    "dash.profit_hint":     "Revenu \u2212 Co\u00fbt",
    "dash.paid_only":       "Factures payées uniquement",
    "dash.stock_label":     "Stock : {qty}",
    "dash.all_in_stock":    "Tous les produits sont en stock.",
    "dash.units":           "≤ {n} unités",

    # ── Base Table ──
    "table.add":            "Ajouter",
    "table.search":         "Rechercher...",
    "table.prev":           "← Préc.",
    "table.next":           "Suiv. →",
    "table.showing":        "Affichage {start}–{end} sur {total} éléments",
    "table.no_items":       "Aucun élément",
    "table.sort_default":   "Tri : Par défaut",
    "table.sort_low_high":  "{col} ↑ Croissant",
    "table.sort_high_low":  "{col} ↓ Décroissant",

    # ── Products ──
    "products.title":       "Produits & Stock",
    "products.col_id":      "ID",
    "products.col_barcode": "Code-barres",
    "products.col_name":    "Nom",
    "products.col_category":"Catégorie",
    "products.col_price":   "Prix (DA)",
    "products.col_stock":   "Stock",
    "products.col_unit":    "Unité",
    "products.edit":        "Modifier",
    "products.delete":      "Supprimer",
    "products.add_title":   "Nouveau Produit",
    "products.edit_title":  "Modifier Produit",
    "products.add_win":     "Ajouter un produit",
    "products.edit_win":    "Modifier le produit",
    "products.name":        "Nom :",
    "products.barcode":     "Code-barres :",
    "products.category":    "Catégorie :",
    "products.supplier":    "Fournisseur :",
    "products.price":       "Prix :",
    "products.cost_price":  "Prix d'achat :",
    "products.stock_qty":   "Qté en stock :",
    "products.unit":        "Unité :",
    "products.save":        "Enregistrer",
    "products.update":      "Mettre à jour",
    "products.cancel":      "Annuler",
    "products.name_req":    "Le nom du produit est requis.",
    "products.del_confirm": "Supprimer le produit « {name} » ?",
    "products.select_first":"Sélectionnez d'abord un produit.",
    "products.none_supplier":"— Aucun —",

    # ── Categories ──
    "cat.title":            "Gérer les catégories",
    "cat.win_title":        "Gérer les catégories",
    "cat.placeholder":      "Nom de la nouvelle catégorie...",
    "cat.add":              "＋ Ajouter",
    "cat.delete":           "Supprimer la sélection",
    "cat.close":            "Fermer",
    "cat.select_warn":      "Sélectionnez une catégorie à supprimer.",
    "cat.del_confirm":      "Supprimer la catégorie « {name} » ?",

    # ── Suppliers ──
    "suppliers.title":      "Fournisseurs",
    "suppliers.col_id":     "ID",
    "suppliers.col_company":"Entreprise",
    "suppliers.col_contact":"Contact",
    "suppliers.col_phone":  "Téléphone",
    "suppliers.col_email":  "E-mail",
    "suppliers.col_products":"Produits",
    "suppliers.edit":       "Modifier",
    "suppliers.delete":     "Supprimer",
    "suppliers.add_title":  "Nouveau Fournisseur",
    "suppliers.edit_title": "Modifier Fournisseur",
    "suppliers.add_win":    "Ajouter un fournisseur",
    "suppliers.edit_win":   "Modifier le fournisseur",
    "suppliers.company":    "Nom de l'entreprise :",
    "suppliers.contact":    "Personne de contact :",
    "suppliers.phone":      "Téléphone :",
    "suppliers.email":      "E-mail :",
    "suppliers.address":    "Adresse :",
    "suppliers.notes":      "Notes :",
    "suppliers.save":       "Enregistrer",
    "suppliers.update":     "Mettre à jour",
    "suppliers.cancel":     "Annuler",
    "suppliers.name_req":   "Le nom de l'entreprise est requis.",
    "suppliers.del_confirm":"Supprimer le fournisseur « {name} » ?",
    "suppliers.del_unlink": "\n\n⚠️  {count} produit(s) seront dissociés (non supprimés).",
    "suppliers.select_first":"Sélectionnez d'abord un fournisseur.",

    # ── Clients ──
    "clients.title":        "Clients",
    "clients.col_id":       "ID",
    "clients.col_name":     "Nom",
    "clients.col_phone":    "Téléphone",
    "clients.col_email":    "E-mail",
    "clients.col_address":  "Adresse",
    "clients.edit":         "Modifier",
    "clients.delete":       "Supprimer",
    "clients.add_title":    "Nouveau Client",
    "clients.edit_title":   "Modifier Client",
    "clients.add_win":      "Ajouter un client",
    "clients.edit_win":     "Modifier le client",
    "clients.name":         "Nom :",
    "clients.phone":        "Téléphone :",
    "clients.email":        "E-mail :",
    "clients.address":      "Adresse :",
    "clients.save":         "Enregistrer",
    "clients.update":       "Mettre à jour",
    "clients.cancel":       "Annuler",
    "clients.name_req":     "Le nom du client est requis.",
    "clients.del_confirm":  "Supprimer le client « {name} » ?",
    "clients.select_first": "Sélectionnez d'abord un client.",

    # ── Invoices ──
    "invoices.title":       "Factures",
    "invoices.col_id":      "ID",
    "invoices.col_client":  "Client",
    "invoices.col_date":    "Date",
    "invoices.col_total":   "Total (DA)",
    "invoices.col_status":  "Statut",
    "invoices.new":         "Nouvelle Facture",
    "invoices.mark_paid":   "Marquer payée",
    "invoices.mark_unpaid": "Marquer impayée",
    "invoices.print_pdf":   "Imprimer PDF",
    "invoices.delete":      "Supprimer",
    "invoices.select_first":"Sélectionnez d'abord une facture.",
    "invoices.del_confirm": "Supprimer la facture #{id} pour {client} ({total} DA) ?\n\nLa dette associée sera également supprimée.",
    "invoices.new_title":   "Nouvelle Facture",
    "invoices.new_win":     "Nouvelle Facture",
    "invoices.client":      "Client :",
    "invoices.col_product": "Produit",
    "invoices.col_available":"Disponible",
    "invoices.col_qty":     "Qté",
    "invoices.col_unit_price":"Prix unitaire",
    "invoices.col_subtotal":"Sous-total",
    "invoices.add_item":    "Ajouter un article",
    "invoices.total":       "Total : {amount} DA",
    "invoices.save":        "Enregistrer la facture",
    "invoices.cancel":      "Annuler",
    "invoices.pick_product":"— cliquez pour choisir —",
    "invoices.no_product":  "Ligne {row} : Aucun produit sélectionné.\nCliquez sur le nom du produit pour en choisir un.",
    "invoices.min_item":    "Ajoutez au moins un article.",
    "invoices.insuff_stock":"❌ Impossible d'enregistrer la facture !\n\nProduit : {product}\nDisponible : {available}\nDemandé : {requested}\n\nVeuillez réduire la quantité.",
    "invoices.insuff_title":"Stock insuffisant",

    # ── Debts ──
    "debts.title":          "Dettes & Paiements",
    "debts.col_id":         "ID",
    "debts.col_client":     "Client",
    "debts.col_due":        "Dû",
    "debts.col_paid":       "Payé",
    "debts.col_remaining":  "Restant",
    "debts.col_status":     "Statut",
    "debts.record_payment": "Enregistrer un paiement",
    "debts.select_first":   "Sélectionnez d'abord une ligne de dette.",
    "debts.pay_title":      "Enregistrer un paiement",
    "debts.pay_amount":     "Montant payé (DA) :",

    # ── Client Profile ──
    "profile.total_invoices":   "Total Factures",
    "profile.total_spent":      "Total Dépensé",
    "profile.outstanding_debt": "Dette en cours",
    "profile.paid_unpaid":      "Payées / Impayées",
    "profile.invoice_history":  "Historique des factures",
    "profile.col_id":           "ID",
    "profile.col_date":         "Date",
    "profile.col_total":        "Total (DA)",
    "profile.col_status":       "Statut",
    "profile.view":             "Voir",
    "profile.close":            "Fermer",

    # ── Invoice Detail ──
    "inv_detail.col_product":   "Produit",
    "inv_detail.col_qty":       "Qté",
    "inv_detail.col_unit_price":"Prix unitaire",
    "inv_detail.col_subtotal":  "Sous-total",
    "inv_detail.total":         "Total :  {amount} DA",
    "inv_detail.print_pdf":     "Imprimer PDF",
    "inv_detail.close":         "Fermer",
    "inv_detail.mark_paid":     "Marquer comme payée",
    "inv_detail.mark_unpaid":   "Marquer comme impayée",

    # ── Supplier Profile ──
    "sup_profile.total_products":   "Total Produits",
    "sup_profile.categories":       "Catégories",
    "sup_profile.units_in_stock":   "Unités en stock",
    "sup_profile.stock_value":      "Valeur du stock (DA)",
    "sup_profile.supplied_products":"Produits fournis",
    "sup_profile.col_id":           "ID",
    "sup_profile.col_name":         "Nom",
    "sup_profile.col_category":     "Catégorie",
    "sup_profile.col_price":        "Prix (DA)",
    "sup_profile.col_stock":        "Stock",
    "sup_profile.close":            "Fermer",
    "sup_profile.no_contact":       "Aucun détail de contact",

    # ── Product Picker ──
    "picker.title":         "Sélectionner un produit",
    "picker.win_title":     "Sélectionner un produit",
    "picker.search":        "Rechercher par nom, catégorie, code-barres...",
    "picker.out_of_stock":  "Rupture de stock",
    "picker.stock":         "Stock : {qty}",
    "picker.count":         "{total} produits  •  {in_stock} en stock  •  {out} en rupture",

    # ── Settings ──
    "settings.title":       "Paramètres",
    "settings.tab_business":"Entreprise",
    "settings.tab_invoice": "Facture",
    "settings.tab_security":"Sécurité",
    "settings.tab_language":"Langue",
    "settings.tab_system":  "Système",
    "settings.save":        "Enregistrer",
    "settings.saved_title": "Paramètres enregistrés",
    "settings.saved_msg":   "Vos paramètres ont été enregistrés avec succès.\nLes modifications des informations d'entreprise s'appliqueront aux nouvelles factures.",

    # Settings — Business
    "settings.biz_header":      "INFORMATIONS DE L'ENTREPRISE",
    "settings.biz_name":        "Nom de l'entreprise",
    "settings.biz_address":     "Adresse",
    "settings.biz_phone":       "Numéro de téléphone",
    "settings.biz_email":       "Adresse e-mail",
    "settings.biz_hint":        "Ces informations apparaissent sur chaque facture PDF générée.",

    # Settings — Invoice
    "settings.inv_header":      "PARAMÈTRES FACTURE & STOCK",
    "settings.inv_currency":    "Symbole de devise",
    "settings.inv_tva":         "Taux TVA (%)",
    "settings.inv_threshold":   "Seuil de stock faible",
    "settings.inv_hint":        "Le symbole de devise apparaît sur les factures et les relevés de dettes.\nLes produits au ou en dessous du seuil de stock faible sont signalés sur le tableau de bord.",

    # Settings — Security
    "settings.sec_login":       "IDENTIFIANTS DE CONNEXION",
    "settings.sec_username":    "Nom d'utilisateur",
    "settings.sec_change_pwd":  "CHANGER LE MOT DE PASSE",
    "settings.sec_current":     "Mot de passe actuel",
    "settings.sec_new":         "Nouveau mot de passe",
    "settings.sec_confirm":     "Confirmer le mot de passe",
    "settings.sec_hint":        "Laissez les champs vides pour conserver le mot de passe actuel.",
    "settings.sec_empty_user":  "Le nom d'utilisateur ne peut pas être vide.",
    "settings.sec_wrong_pwd":   "Le mot de passe actuel est incorrect.",
    "settings.sec_empty_new":   "Le nouveau mot de passe ne peut pas être vide.",
    "settings.sec_mismatch":    "Les nouveaux mots de passe ne correspondent pas.",

    # Settings — Language
    "settings.lang_header":     "LANGUAGE / LANGUE",
    "settings.lang_hint":       "La langue de l'interface changera après le redémarrage de l'application.",

    # Settings — System
    "settings.sys_about":       "À PROPOS DE L'APPLICATION",
    "settings.sys_app_name":    "Nom de l'application",
    "settings.sys_version":     "Version",
    "settings.sys_release":     "Date de sortie",
    "settings.sys_description": "Description",
    "settings.sys_desc_text":   "Gestion d'entreprise de bureau — factures, clients, stock et dettes",
    "settings.sys_license":     "Licence",
    "settings.sys_license_text":"Privé / Tous droits réservés",
    "settings.sys_dev":         "INFORMATIONS DU DÉVELOPPEUR",
    "settings.sys_developer":   "Développeur",
    "settings.sys_contact":     "Contact",
    "settings.sys_built_with":  "Construit avec",
    "settings.backup_btn":      "Télécharger la sauvegarde",
    "settings.backup_ok_title": "Sauvegarde terminée",
    "settings.backup_ok_msg":   "Base de données sauvegardée avec succès vers :\n{path}",
    "settings.backup_err":      "Échec de la sauvegarde : {error}",

    # ── Status ──
    "status.paid":          "PAYÉE",
    "status.unpaid":        "IMPAYÉE",
    "status.paid_lower":    "payée",
    "status.unpaid_lower":  "impayée",
    "status.pending":       "En attente",
    "status.settled":       "Réglée",

    # ── PDF ──
    "pdf.invoice_num":      "Facture N° :",
    "pdf.date":             "Date :",
    "pdf.client":           "Client :",
    "pdf.phone":            "Téléphone :",
    "pdf.col_num":          "#",
    "pdf.col_product":      "Produit",
    "pdf.col_qty":          "Qté",
    "pdf.col_unit_price":   "Prix unitaire",
    "pdf.col_total":        "Total",
    "pdf.total":            "TOTAL",
    "pdf.subtotal":         "SOUS-TOTAL",
    "pdf.tva":              "TVA ({rate}%)",
    "pdf.status":           "Statut :",
    "pdf.notes":            "Notes :",

    # ── Date ──
    "date.format":          "{weekday} {day} {month} {year}",

    # Common
    "common.validation":    "Validation",
    "common.warning":       "Avertissement",
    "common.error":         "Erreur",
    "common.confirm":       "Confirmer",
    "common.confirm_delete":"Confirmer la suppression",
    "common.yes":           "Oui",
    "common.no":            "Non",
}

_LANGUAGES = {"en": EN, "fr": FR}

_FR_DAYS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
_FR_MONTHS = [
    "", "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]
_EN_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
_EN_MONTHS = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def get_language() -> str:
    """Return the currently configured language code ('en' or 'fr')."""
    return load_settings().get("language", "en")


def t(key: str, **kwargs) -> str:
    """
    Look up a translation key and return the localised string.
    Supports keyword formatting: t("dash.units", n=5) → "≤ 5 units"
    Falls back to English if the key is missing in the active language.
    """
    lang = get_language()
    table = _LANGUAGES.get(lang, EN)
    text = table.get(key, EN.get(key, key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text


def format_date(dt) -> str:
    """
    Format a date/datetime object using the current language.
    Returns e.g. "Monday, March 17 2026" or "lundi 17 mars 2026".
    """
    lang = get_language()
    if lang == "fr":
        weekday = _FR_DAYS[dt.weekday()]
        month = _FR_MONTHS[dt.month]
    else:
        weekday = _EN_DAYS[dt.weekday()]
        month = _EN_MONTHS[dt.month]
    return t("date.format", weekday=weekday, month=month, day=dt.day, year=dt.year)


def translate_status(status: str) -> str:
    """Translate a database status value ('paid'/'unpaid'/'pending'/'settled') to current language."""
    key = f"status.{status}"
    result = t(key)
    if result == key:
        return status.upper()
    return result
