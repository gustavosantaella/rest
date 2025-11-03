from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
import enum
from app.database import Base

class PaymentMethodType(str, enum.Enum):
    PAGO_MOVIL = "pago_movil"
    TRANSFERENCIA = "transferencia"
    EFECTIVO = "efectivo"
    BOLIVARES = "bolivares"
    DOLARES = "dolares"
    EUROS = "euros"

class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Nombre descriptivo: "Pago Móvil Banco X"
    type = Column(SQLEnum(PaymentMethodType), nullable=False)
    
    # Para Pago Móvil
    phone = Column(String, nullable=True)
    
    # Para ambos (Pago Móvil y Transferencia)
    dni = Column(String, nullable=True)
    bank = Column(String, nullable=True)
    account_holder = Column(String, nullable=True)  # Nombre del titular
    
    # Para Transferencia Bancaria
    account_number = Column(String, nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete

