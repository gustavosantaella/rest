from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_configuration.id", ondelete='CASCADE'), nullable=False, index=True)
    
    # Campos del formulario
    nombre = Column(String, nullable=False, index=True)
    apellido = Column(String, nullable=True)
    dni = Column(String, nullable=True, index=True)
    telefono = Column(String, nullable=True)
    correo = Column(String, nullable=True)
    
    # Campos de auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    
    # Relaciones
    business = relationship("BusinessConfiguration", back_populates="customers")
    orders = relationship("Order", back_populates="customer")

