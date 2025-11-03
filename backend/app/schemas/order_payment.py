from pydantic import BaseModel, Field
from typing import Optional

class OrderPaymentBase(BaseModel):
    payment_method_id: int
    amount: float = Field(..., gt=0, description="Monto del pago")
    reference: Optional[str] = Field(None, description="Número de referencia/comprobante")

class OrderPaymentCreate(OrderPaymentBase):
    pass

class OrderPaymentResponse(OrderPaymentBase):
    id: int
    order_id: int
    payment_method_name: Optional[str] = None  # Para mostrar el nombre del método
    
    class Config:
        from_attributes = True

