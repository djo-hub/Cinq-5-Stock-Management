from ..database import get_session
from ..models.client import Client

def get_all_clients():
    session = get_session()
    return session.query(Client).all()

def add_client(name, phone="", email="", address=""):
    session = get_session()
    c = Client(name=name, phone=phone, email=email, address=address)
    session.add(c)
    session.commit()
    return c

def update_client(client_id, **kwargs):
    session = get_session()
    c = session.query(Client).get(client_id)
    if c:
        for k, v in kwargs.items():
            setattr(c, k, v)
        session.commit()

def delete_client(client_id):
    session = get_session()
    c = session.query(Client).get(client_id)
    if c:
        session.delete(c)
        session.commit()
