from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Product(Base):
    __tablename__ = "products"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    name        = Column(String, nullable=False)
    category    = Column(String, default="General")
    price       = Column(Float, nullable=False)
    stock_qty   = Column(Integer, default=0)
    unit        = Column(String, default="pcs")
    cost_price  = Column(Float, default=0.0)
    barcode     = Column(String, default="", nullable=True)
    created_at  = Column(DateTime, default=datetime.now)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)

    supplier = relationship("Supplier", back_populates="products")
