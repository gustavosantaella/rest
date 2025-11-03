from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MenuCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    display_order: int = 0
    is_active: bool = True


class MenuCategoryCreate(MenuCategoryBase):
    pass


class MenuCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


class MenuCategoryResponse(MenuCategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class IngredientItem(BaseModel):
    product_id: int
    quantity: float
    product_name: Optional[str] = None  # Para respuesta


class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    price: float
    preparation_time: Optional[int] = None
    is_available: bool = True
    is_featured: bool = False
    image_url: Optional[str] = None


class MenuItemCreate(MenuItemBase):
    ingredients: List[IngredientItem] = []


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None
    preparation_time: Optional[int] = None
    is_available: Optional[bool] = None
    is_featured: Optional[bool] = None
    image_url: Optional[str] = None
    ingredients: Optional[List[IngredientItem]] = None


class MenuItemResponse(MenuItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    ingredients: List[IngredientItem] = []
    
    class Config:
        from_attributes = True


class MenuItemPublicResponse(MenuItemBase):
    """Schema simplificado para catálogo público (sin ingredientes)"""
    id: int
    
    class Config:
        from_attributes = True

