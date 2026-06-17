from app.database import get_session
from app.models.invoice import Invoice, InvoiceItem
from app.models.product import Product
from app.models.debt import Debt


class InsufficientStockError(Exception):
    def __init__(self, product_name, available, requested):
        self.product_name = product_name
        self.available = available
        self.requested = requested


def get_all_invoices():
    session = get_session()
    return session.query(Invoice).order_by(Invoice.id.desc()).all()


def create_invoice(client_id, items):
    session = get_session()
    total = 0
    invoice_items = []

    for item in items:
        product = session.query(Product).get(item["product_id"])
        if product.stock_qty < item["qty"]:
            raise InsufficientStockError(product.name, product.stock_qty, item["qty"])
        product.stock_qty -= item["qty"]
        subtotal = item["qty"] * item["unit_price"]
        total += subtotal
        invoice_items.append(InvoiceItem(
            product_id=item["product_id"],
            qty=item["qty"],
            unit_price=item["unit_price"]
        ))

    inv = Invoice(client_id=client_id, total=total,
                  status="unpaid", items=invoice_items)
    session.add(inv)
    session.flush()

    debt = Debt(
        client_id=client_id,
        invoice_id=inv.id,
        amount_due=total,
        amount_paid=0,
        status="pending"                   # ✅ correct value
    )
    session.add(debt)
    session.commit()
    return inv

def delete_invoice(invoice_id):
    session = get_session()
    # Delete linked debt first
    debt = session.query(Debt).filter_by(invoice_id=invoice_id).first()
    if debt:
        session.delete(debt)
    # Restore stock for each item before deleting
    inv = session.query(Invoice).get(invoice_id)
    if inv:
        for item in inv.items:
            product = session.query(Product).get(item.product_id)
            if product:
                product.stock_qty += item.qty
        session.delete(inv)
    session.commit()


def mark_paid(invoice_id):
    session = get_session()
    inv = session.query(Invoice).get(invoice_id)
    if inv:
        inv.status = "paid"
        debt = session.query(Debt).filter_by(invoice_id=invoice_id).first()
        if debt:
            debt.amount_paid = debt.amount_due
            debt.status = "settled"        # ✅ correct value
        session.commit()


def mark_unpaid(invoice_id):
    session = get_session()
    inv = session.query(Invoice).get(invoice_id)
    if inv:
        inv.status = "unpaid"
        debt = session.query(Debt).filter_by(invoice_id=invoice_id).first()
        if debt:
            debt.amount_paid = 0
            debt.status = "pending"        # ✅ correct value
        else:
            debt = Debt(
                client_id=inv.client_id,
                invoice_id=invoice_id,
                amount_due=inv.total,
                amount_paid=0,
                status="pending"           # ✅ correct value
            )
            session.add(debt)
        session.commit()
