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
    payment_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class AccountReceivableBase(BaseModel):
    customer_id: Optional[int] = None
    invoice_number: Optional[str] = None
    description: str
    amount: float
    due_date: datetime
    notes: Optional[str] = None


class AccountReceivableCreate(AccountReceivableBase):
    pass


class AccountReceivableUpdate(BaseModel):
    customer_id: Optional[int] = None
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
    
    class Config:
        from_attributes = True

