from app.database import get_session
from app.models.category import Category

def get_all_categories():
    session = get_session()
    return session.query(Category).order_by(Category.name).all()

def get_category_names():
    return [c.name for c in get_all_categories()]

def add_category(name):
    session = get_session()
    name = name.strip()
    if not name:
        return None
    exists = session.query(Category).filter_by(name=name).first()
    if exists:
        return exists
    c = Category(name=name)
    session.add(c)
    session.commit()
    return c

def delete_category(name):
    session = get_session()
    c = session.query(Category).filter_by(name=name).first()
    if c:
        session.delete(c)
        session.commit()
