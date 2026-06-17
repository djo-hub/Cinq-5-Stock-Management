from sqlalchemy.orm import joinedload
from app.database import get_session
from app.models.debt import Debt
from app.models.invoice import Invoice

def get_all_debts():
    session = get_session()
    return (session.query(Debt)
            .options(joinedload(Debt.client))
            .filter_by(status="pending")
            .all())

def record_payment(debt_id, amount):
    session = get_session()
    d = session.query(Debt).get(debt_id)
    d.amount_paid += amount
    if d.amount_paid >= d.amount_due:
        d.status = "settled"
        # ✅ Mark the linked invoice as paid too
        if d.invoice_id:
            inv = session.query(Invoice).get(d.invoice_id)
            if inv:
                inv.status = "paid"
    session.commit()
