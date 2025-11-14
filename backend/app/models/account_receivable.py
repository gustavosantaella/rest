from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base


class AccountStatus(str, enum.Enum):
    PENDING = "pending"      # Pendiente
    PARTIAL = "partial"      # Parcialmente pagado
    PAID = "paid"           # Pagado
    OVERDUE = "overdue"     # Vencido


class AccountReceivable(Base):
    """Cuentas por Cobrar - Dinero que nos deben los clientes"""
    __tablename__ = "accounts_receivable"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_configuration.id", ondelete='CASCADE'), nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete='SET NULL'), nullable=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete='SET NULL'), nullable=True, index=True)  # Orden relacionada
    
    # Información de la cuenta
    invoice_number = Column(String, index=True)  # Número de factura
    description = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)  # Monto total
    amount_paid = Column(Float, default=0.0)  # Monto pagado
    amount_pending = Column(Float, nullable=False)  # Monto pendiente
    
    # Fechas
    issue_date = Column(DateTime(timezone=True), server_default=func.now())  # Fecha de emisión
    due_date = Column(DateTime(timezone=True), nullable=False)  # Fecha de vencimiento
    paid_date = Column(DateTime(timezone=True), nullable=True)  # Fecha de pago completo
    
    # Estado
    status = Column(Enum(AccountStatus), default=AccountStatus.PENDING, nullable=False, index=True)
    
    # Información adicional
    notes = Column(Text)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relaciones
    business = relationship("BusinessConfiguration")
    customer = relationship("Customer")
    order = relationship("Order", backref="account_receivable")
    payments = relationship("AccountReceivablePayment", back_populates="account", cascade="all, delete-orphan")


class AccountReceivablePayment(Base):
    """Pagos de Cuentas por Cobrar"""
    __tablename__ = "account_receivable_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts_receivable.id", ondelete='CASCADE'), nullable=False)
    
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    payment_method = Column(String)  # Efectivo, transferencia, etc.
    reference = Column(String)  # Número de referencia
    notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    account = relationship("AccountReceivable", back_populates="payments")

