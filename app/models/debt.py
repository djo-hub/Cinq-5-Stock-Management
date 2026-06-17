from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Debt(Base):
    __tablename__ = "debts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    amount_due = Column(Float, default=0.0)
    amount_paid = Column(Float, default=0.0)
    due_date = Column(DateTime, nullable=True)
    status = Column(String, default="pending")  # pending / settled
    created_at = Column(DateTime, default=datetime.now)
    client = relationship("Client")
