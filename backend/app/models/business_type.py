"""
Modelo de tipos de negocios
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class BusinessType(Base):
    __tablename__ = "business_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)  # Restaurant, Kiosko, etc.
    slug = Column(String, unique=True, nullable=False, index=True)  # restaurant, kiosko, etc.
    description = Column(Text, nullable=True)  # Descripción del tipo de negocio
    
    # Configuración de características
    has_menu = Column(Boolean, default=True)  # Muestra opción de Menú
    has_tables = Column(Boolean, default=True)  # Muestra opción de Mesas
    has_ingredients = Column(Boolean, default=True)  # Permite ingredientes en menú
    has_menu_statistics = Column(Boolean, default=True)  # Muestra estadísticas de menú
    has_product_statistics = Column(Boolean, default=True)  # Muestra estadísticas de productos
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    businesses = relationship("BusinessConfiguration", back_populates="business_type")

