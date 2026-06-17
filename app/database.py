import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base


def _get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(".")


_db_path = os.path.join(_get_app_dir(), "business.db")
DATABASE_URL = f"sqlite:///{_db_path}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

_session = None

def get_session():
    global _session
    if _session is None:
        _session = SessionLocal()
    return _session

def init_db():
    from app.models import product, client, invoice, debt, stock, category, supplier
    Base.metadata.create_all(bind=engine)
    _migrate()

def _migrate():
    """Add columns introduced after the initial schema without losing data."""
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE products ADD COLUMN supplier_id INTEGER"))
            conn.commit()
        except Exception:
            pass  # column already exists
        try:
            conn.execute(text("ALTER TABLE products ADD COLUMN cost_price REAL DEFAULT 0"))
            conn.commit()
        except Exception:
            pass  # column already exists
