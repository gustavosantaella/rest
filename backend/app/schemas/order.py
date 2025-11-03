from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..models.order import OrderStatus, PaymentMethod


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: float
    notes: Optional[str] = None


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: float
    unit_price: float
    subtotal: float
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    table_id: Optional[int] = None
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    payment_method: Optional[PaymentMethod] = None
    discount: Optional[float] = None
    notes: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    user_id: int
    status: OrderStatus
    payment_method: Optional[PaymentMethod] = None
    subtotal: float
    tax: float
    discount: float
    total: float
    created_at: datetime
    paid_at: Optional[datetime] = None
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True

