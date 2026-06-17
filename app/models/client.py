from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    phone = Column(String, default="")
    email = Column(String, default="")
    address = Column(String, default="")
    created_at = Column(DateTime, default=datetime.now)
