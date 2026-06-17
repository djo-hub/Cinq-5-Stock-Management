from app.database import get_session
from app.models.product import Product
from app.models.stock import StockMovement

def get_all_products():
    session = get_session()
    return session.query(Product).all()

def get_product_by_barcode(barcode):
    session = get_session()
    return session.query(Product).filter_by(barcode=barcode).first()

def add_product(name, category, price, stock_qty, unit, barcode="", supplier_id=None, cost_price=0.0):
    session = get_session()
    p = Product(name=name, category=category, price=price,
                stock_qty=int(stock_qty), unit=unit, barcode=barcode,
                supplier_id=supplier_id, cost_price=cost_price)
    session.add(p)
    session.commit()
    return p

def update_product(product_id, **kwargs):
    session = get_session()
    p = session.query(Product).get(product_id)
    if "stock_qty" in kwargs:
        kwargs["stock_qty"] = int(kwargs["stock_qty"])
    for k, v in kwargs.items():
        setattr(p, k, v)
    session.commit()

def delete_product(product_id):
    session = get_session()
    p = session.query(Product).get(product_id)
    if p:
        session.delete(p)
        session.commit()

def adjust_stock(product_id, qty, movement_type, note=""):
    session = get_session()
    p = session.query(Product).get(product_id)
    if movement_type == "in":
        p.stock_qty += int(qty)
    else:
        p.stock_qty -= int(qty)
    mv = StockMovement(product_id=product_id, movement_type=movement_type,
                       qty=int(qty), note=note)
    session.add(mv)
    session.commit()
