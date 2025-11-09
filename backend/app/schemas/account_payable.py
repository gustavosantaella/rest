from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class AccountPayablePaymentBase(BaseModel):
    amount: float
    payment_method: Optional[str] = None
    reference: Optional[str] = None
    notes: Optional[str] = None


class AccountPayablePaymentCreate(AccountPayablePaymentBase):
    pass


class AccountPayablePaymentResponse(AccountPayablePaymentBase):
    id: int
    account_id: int
    payment_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class AccountPayableBase(BaseModel):
    supplier_name: str
    supplier_phone: Optional[str] = None
    supplier_email: Optional[EmailStr] = None
    invoice_number: Optional[str] = None
    description: str
    amount: float
    due_date: datetime
    notes: Optional[str] = None


class AccountPayableCreate(AccountPayableBase):
    pass


class AccountPayableUpdate(BaseModel):
    supplier_name: Optional[str] = None
    supplier_phone: Optional[str] = None
    supplier_email: Optional[EmailStr] = None
    invoice_number: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    due_date: Optional[datetime] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class AccountPayableResponse(AccountPayableBase):
    id: int
    business_id: int
    amount_paid: float
    amount_pending: float
    issue_date: datetime
    paid_date: Optional[datetime] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    payments: List[AccountPayablePaymentResponse] = []
    
    class Config:
        from_attributes = True

