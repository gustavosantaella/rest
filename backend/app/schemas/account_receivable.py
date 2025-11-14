from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AccountReceivablePaymentBase(BaseModel):
    amount: float
    payment_method: Optional[str] = None
    reference: Optional[str] = None
    notes: Optional[str] = None


class AccountReceivablePaymentCreate(AccountReceivablePaymentBase):
    pass


class AccountReceivablePaymentResponse(AccountReceivablePaymentBase):
    id: int
    account_id: int
    payment_date: datetime  # Siempre debe tener un valor
    created_at: datetime
    
    @classmethod
    def model_validate(cls, obj, *, from_attributes=True):
        """Validar y asegurar que payment_date tenga un valor"""
        from datetime import datetime as dt
        # Si payment_date es None, usar created_at o fecha actual
        if hasattr(obj, 'payment_date') and obj.payment_date is None:
            if hasattr(obj, 'created_at') and obj.created_at:
                obj.payment_date = obj.created_at
            else:
                obj.payment_date = dt.now()
        return super().model_validate(obj, from_attributes=from_attributes)
    
    class Config:
        from_attributes = True


class AccountReceivableBase(BaseModel):
    customer_id: Optional[int] = None
    order_id: Optional[int] = None  # ID de la orden relacionada
    invoice_number: Optional[str] = None
    description: str
    amount: float
    due_date: datetime
    notes: Optional[str] = None


class AccountReceivableCreate(AccountReceivableBase):
    pass


class AccountReceivableUpdate(BaseModel):
    customer_id: Optional[int] = None
    order_id: Optional[int] = None
    invoice_number: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    due_date: Optional[datetime] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class AccountReceivableResponse(AccountReceivableBase):
    id: int
    business_id: int
    amount_paid: float
    amount_pending: float
    issue_date: datetime
    paid_date: Optional[datetime] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    payments: List[AccountReceivablePaymentResponse] = []
    customer_name: Optional[str] = None  # Nombre del cliente (calculado)
    
    @classmethod
    def model_validate(cls, obj, *, from_attributes=True):
        """Validar y asegurar que todos los pagos tengan payment_date válido"""
        from datetime import datetime as dt
        # Asegurar que todos los pagos tengan payment_date válido
        if hasattr(obj, 'payments') and obj.payments:
            for payment in obj.payments:
                if hasattr(payment, 'payment_date') and payment.payment_date is None:
                    if hasattr(payment, 'created_at') and payment.created_at:
                        payment.payment_date = payment.created_at
                    else:
                        payment.payment_date = dt.now()
        return super().model_validate(obj, from_attributes=from_attributes)
    
    class Config:
        from_attributes = True

