from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.product import UnitType


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    unit_type: UnitType = UnitType.UNIT
    purchase_price: float
    sale_price: float
    stock: float = 0
    min_stock: float = 0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    unit_type: Optional[UnitType] = None
    purchase_price: Optional[float] = None
    sale_price: Optional[float] = None
    stock: Optional[float] = None
    min_stock: Optional[float] = None


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

