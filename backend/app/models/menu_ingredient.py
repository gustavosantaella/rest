from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class MenuItemIngredient(Base):
    __tablename__ = "menu_item_ingredients_detail"
    
    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id", ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete='CASCADE'), nullable=False)
    quantity = Column(Float, nullable=False)  # Cantidad del ingrediente necesaria

