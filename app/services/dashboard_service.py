from app.database import SessionLocal
from app.models.product import Product
from app.models.invoice import Invoice, InvoiceItem
from app.models.debt import Debt
from app.config import get as cfg_get
import sqlalchemy
from datetime import datetime, timedelta
from collections import OrderedDict


def get_dashboard_stats():
    db = SessionLocal()
    try:
        # Products
        total_products  = db.query(Product).count()
        threshold       = int(cfg_get("low_stock_threshold") or 5)
        low_stock       = db.query(Product).filter(Product.stock_qty <= threshold, Product.stock_qty > 0).count()
        out_of_stock    = db.query(Product).filter(Product.stock_qty == 0).all()
        total_in_stock  = db.query(sqlalchemy.func.sum(Product.stock_qty)).scalar() or 0

        # Sales
        total_profit = db.query(
            sqlalchemy.func.sum(
                (InvoiceItem.unit_price - Product.cost_price) * InvoiceItem.qty
            )
        ).join(Product, InvoiceItem.product_id == Product.id).scalar() or 0

        total_income = db.query(
            sqlalchemy.func.sum(Invoice.total)
        ).filter(Invoice.status == "paid").scalar() or 0

        unpaid_invoices = db.query(Invoice).filter(Invoice.status == "unpaid").count()

        # Debts
        total_debts = db.query(
            sqlalchemy.func.sum(Debt.amount_due - Debt.amount_paid)
        ).scalar() or 0

        return {
            "total_products":  total_products,
            "low_stock":       low_stock,
            "out_of_stock":    [(p.name, p.stock_qty) for p in out_of_stock],
            "total_in_stock":  total_in_stock,
            "total_profit":    total_profit,
            "total_income":    total_income,
            "unpaid_invoices": unpaid_invoices,
            "total_debts":     total_debts,
        }
    finally:
        db.close()


def get_monthly_revenue(months=6):
    """Return a list of (month_label, total_revenue) for the last N months."""
    db = SessionLocal()
    try:
        today = datetime.now()
        # Build ordered dict with last N months initialised to 0
        buckets = OrderedDict()
        for i in range(months - 1, -1, -1):
            d = today - timedelta(days=i * 30)
            key = d.strftime("%Y-%m")
            buckets[key] = 0.0

        rows = (
            db.query(
                sqlalchemy.func.strftime("%Y-%m", Invoice.date).label("month"),
                sqlalchemy.func.sum(Invoice.total).label("revenue"),
            )
            .filter(Invoice.status == "paid")
            .group_by("month")
            .all()
        )

        for month_key, revenue in rows:
            if month_key in buckets:
                buckets[month_key] = float(revenue or 0)

        return list(buckets.items())
    finally:
        db.close()


def get_monthly_profit(months=6):
    """Return a list of (month_label, total_profit) for the last N months."""
    db = SessionLocal()
    try:
        today = datetime.now()
        buckets = OrderedDict()
        for i in range(months - 1, -1, -1):
            d = today - timedelta(days=i * 30)
            key = d.strftime("%Y-%m")
            buckets[key] = 0.0

        rows = (
            db.query(
                sqlalchemy.func.strftime("%Y-%m", Invoice.date).label("month"),
                sqlalchemy.func.sum(
                    (InvoiceItem.unit_price - Product.cost_price) * InvoiceItem.qty
                ).label("profit"),
            )
            .join(InvoiceItem, Invoice.id == InvoiceItem.invoice_id)
            .join(Product, InvoiceItem.product_id == Product.id)
            .filter(Invoice.status == "paid")
            .group_by("month")
            .all()
        )

        for month_key, profit in rows:
            if month_key in buckets:
                buckets[month_key] = float(profit or 0)

        return list(buckets.items())
    finally:
        db.close()


def get_debts_by_client(limit=10):
    """Return a list of (client_name, total_debt) for debts grouped by client."""
    from app.models.client import Client
    
    db = SessionLocal()
    try:
        rows = (
            db.query(
                Client.name,
                sqlalchemy.func.sum(Debt.amount_due - Debt.amount_paid).label("debt"),
            )
            .join(Client, Debt.client_id == Client.id)
            .filter((Debt.amount_due - Debt.amount_paid) > 0)
            .group_by(Client.id, Client.name)
            .order_by(sqlalchemy.desc("debt"))
            .limit(limit)
            .all()
        )
        
        return [(name, float(debt or 0)) for name, debt in rows]
    finally:
        db.close()
