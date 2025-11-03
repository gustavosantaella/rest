from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


# Tabla de relación muchos a muchos entre MenuItem e Ingredientes (Products)
menu_item_ingredients = Table(
    'menu_item_ingredients',
    Base.metadata,
    Column('menu_item_id', Integer, ForeignKey('menu_items.id', ondelete='CASCADE'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id', ondelete='CASCADE'), primary_key=True),
    Column('quantity', Float, nullable=False)  # Cantidad del ingrediente necesaria
)


class MenuCategory(Base):
    __tablename__ = "menu_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    display_order = Column(Integer, default=0)  # Orden de visualización
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    
    menu_items = relationship("MenuItem", back_populates="category")


class MenuItem(Base):
    __tablename__ = "menu_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("menu_categories.id"), nullable=False)
    
    # Precios y configuración
    price = Column(Float, nullable=False)  # Precio de venta del platillo
    preparation_time = Column(Integer)  # Tiempo de preparación en minutos
    
    # Disponibilidad
    is_available = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)  # Platillo destacado/recomendado
    
    # Imágenes y extras
    image_url = Column(String)  # URL de la imagen del platillo
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    
    category = relationship("MenuCategory", back_populates="menu_items")
    # Ingredientes necesarios para preparar este platillo
    ingredients = relationship("Product", secondary=menu_item_ingredients, backref="menu_items")

