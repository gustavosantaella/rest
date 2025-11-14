from pydantic import BaseModel, field_validator, model_validator
from typing import Optional, List
from datetime import datetime
from ..models.order import OrderStatus, PaymentMethod
from .order_payment import OrderPaymentCreate, OrderPaymentResponse


class OrderItemCreate(BaseModel):
    product_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    quantity: float
    notes: Optional[str] = None
    source_type: Optional[str] = "product"  # 'product' o 'menu'
    
    @model_validator(mode='after')
    def validate_ids(self):
        # Al menos uno de los dos IDs debe existir
        if not self.product_id and not self.menu_item_id:
            raise ValueError('Debe proporcionar product_id o menu_item_id')
        return self
    
    class Config:
        extra = "ignore"  # Ignorar campos extras no definidos


class OrderItemResponse(BaseModel):
    id: int
    product_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    source_type: Optional[str] = "product"
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
    customer_id: Optional[int] = None
    # Campos deprecated - mantener por compatibilidad
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]
    payments: List[OrderPaymentCreate] = []  # Opcional - se puede pagar después
    
    class Config:
        extra = "ignore"  # Ignorar campos extras no definidos


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


class UpdateOrderItems(BaseModel):
    items: List[OrderItemCreate]
