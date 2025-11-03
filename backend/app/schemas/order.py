from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from ..models.order import OrderStatus, PaymentMethod
from .order_payment import OrderPaymentCreate, OrderPaymentResponse


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
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]
    payments: List[OrderPaymentCreate] = []  # Opcional - se puede pagar después


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    payment_method: Optional[PaymentMethod] = None
    discount: Optional[float] = None
    notes: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    user_id: int
    status: OrderStatus
    payment_method: Optional[PaymentMethod] = None  # Deprecated
    payment_status: str = "pending"
    subtotal: float
    tax: float
    discount: float
    total: float
    created_at: datetime
    paid_at: Optional[datetime] = None
    items: List[OrderItemResponse] = []
    payments: List[OrderPaymentResponse] = []
    
    class Config:
        from_attributes = True


class AddPaymentsToOrder(BaseModel):
    payments: List[OrderPaymentCreate]

