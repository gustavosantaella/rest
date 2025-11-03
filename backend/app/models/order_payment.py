from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class OrderPayment(Base):
    __tablename__ = "order_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"), nullable=False)
    amount = Column(Float, nullable=False)
    reference = Column(String, nullable=True)  # Número de referencia/comprobante
    
    # Relationships
    order = relationship("Order", back_populates="payments")
    payment_method = relationship("PaymentMethod")

