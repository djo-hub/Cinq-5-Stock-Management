from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"
    id             = Column(Integer, primary_key=True, autoincrement=True)
    name           = Column(String, nullable=False)
    contact_person = Column(String, default="")
    phone          = Column(String, default="")
    email          = Column(String, default="")
    address        = Column(String, default="")
    notes          = Column(String, default="")

    products = relationship("Product", back_populates="supplier")
