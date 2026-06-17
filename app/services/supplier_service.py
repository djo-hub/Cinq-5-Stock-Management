from app.database import get_session
from app.models.supplier import Supplier


def get_all_suppliers():
    session = get_session()
    return session.query(Supplier).all()


def add_supplier(name, contact_person="", phone="", email="", address="", notes=""):
    session = get_session()
    s = Supplier(name=name, contact_person=contact_person,
                 phone=phone, email=email, address=address, notes=notes)
    session.add(s)
    session.commit()
    return s


def update_supplier(supplier_id, **kwargs):
    session = get_session()
    s = session.query(Supplier).get(supplier_id)
    if s:
        for k, v in kwargs.items():
            setattr(s, k, v)
        session.commit()


def delete_supplier(supplier_id):
    session = get_session()
    s = session.query(Supplier).get(supplier_id)
    if s:
        for p in s.products:
            p.supplier_id = None
        session.delete(s)
        session.commit()
