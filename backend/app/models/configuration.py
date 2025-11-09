from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class BusinessConfiguration(Base):
    __tablename__ = "business_configuration"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Información del negocio
    business_name = Column(String, nullable=False)  # Nombre del local
    slug = Column(String, unique=True, index=True)  # Slug único para URL pública
    legal_name = Column(String)  # Razón social
    rif = Column(String, unique=True, index=True)  # RIF o identificación fiscal
    
    # Contacto
    phone = Column(String)
    email = Column(String)
    address = Column(Text)
    
    # Configuración fiscal
    tax_rate = Column(Float, default=0.16)  # Tasa de impuesto (16% por defecto)
    currency = Column(String, default="USD")  # Moneda
    
    # Logo
    logo_url = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    partners = relationship("Partner", back_populates="business", cascade="all, delete-orphan")
    users = relationship("User", back_populates="business")
    customers = relationship("Customer", back_populates="business")


class Partner(Base):
    __tablename__ = "partners"
    
    id = Column(Integer, primary_key=True, index=True)
    business_config_id = Column(Integer, ForeignKey("business_configuration.id", ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    
    # Información del socio
    participation_percentage = Column(Float, nullable=False)  # Porcentaje de participación
    investment_amount = Column(Float, default=0)  # Monto de inversión
    
    # Fechas
    join_date = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    notes = Column(Text)  # Notas adicionales
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    business = relationship("BusinessConfiguration", back_populates="partners")
    user = relationship("User")

