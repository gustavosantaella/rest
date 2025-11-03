from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base


class UnitType(str, enum.Enum):
    UNIT = "unit"  # Por unidad
    WEIGHT_GRAM = "weight_gram"  # Por gramo
    WEIGHT_KG = "weight_kg"  # Por kilogramo
    VOLUME_ML = "volume_ml"  # Por mililitro
    VOLUME_L = "volume_l"  # Por litro
    BULK = "bulk"  # A granel/masivo


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    unit_type = Column(Enum(UnitType), default=UnitType.UNIT, nullable=False)
    
    # Precios
    purchase_price = Column(Float, nullable=False)  # Precio de compra
    sale_price = Column(Float, nullable=False)  # Precio de venta
    
    # Inventario
    stock = Column(Float, default=0)  # Stock actual
    min_stock = Column(Float, default=0)  # Stock mínimo para alerta
    
    # Mostrar en catálogo (selector de órdenes)
    show_in_catalog = Column(Boolean, default=False)  # Por defecto no se muestra
    
    # Imagen del producto
    image_url = Column(String, nullable=True)  # URL de la imagen del producto
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    category = relationship("Category", back_populates="products")

