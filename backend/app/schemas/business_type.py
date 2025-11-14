"""
Schemas para tipos de negocios
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BusinessTypeBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    has_menu: bool = True
    has_tables: bool = True
    has_ingredients: bool = True
    has_menu_statistics: bool = True
    has_product_statistics: bool = True
    is_active: bool = True


class BusinessTypeCreate(BusinessTypeBase):
    pass


class BusinessTypeUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    has_menu: Optional[bool] = None
    has_tables: Optional[bool] = None
    has_ingredients: Optional[bool] = None
    has_menu_statistics: Optional[bool] = None
    has_product_statistics: Optional[bool] = None
    is_active: Optional[bool] = None


class BusinessTypeResponse(BusinessTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

