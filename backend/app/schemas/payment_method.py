from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class PaymentMethodType(str, Enum):
    PAGO_MOVIL = "pago_movil"
    TRANSFERENCIA = "transferencia"
    EFECTIVO = "efectivo"
    BOLIVARES = "bolivares"
    DOLARES = "dolares"
    EUROS = "euros"

class PaymentMethodBase(BaseModel):
    name: str = Field(..., description="Nombre descriptivo del método de pago")
    type: PaymentMethodType
    phone: Optional[str] = None
    dni: Optional[str] = None
    bank: Optional[str] = None
    account_holder: Optional[str] = None
    account_number: Optional[str] = None
    is_active: bool = True

class PaymentMethodCreate(PaymentMethodBase):
    @validator('phone', 'dni', 'bank', 'account_holder', always=True)
    def validate_pago_movil_fields(cls, v, values):
        if 'type' in values and values['type'] == PaymentMethodType.PAGO_MOVIL:
            # Para pago móvil, estos campos son requeridos
            field_name = cls.__fields__[v].name if hasattr(cls.__fields__.get(v, None), 'name') else None
            if field_name in ['phone', 'dni', 'bank', 'account_holder']:
                if not v:
                    raise ValueError(f'{field_name} es requerido para Pago Móvil')
        return v
    
    @validator('account_number', 'dni', 'bank', 'account_holder', always=True)
    def validate_transferencia_fields(cls, v, values):
        if 'type' in values and values['type'] == PaymentMethodType.TRANSFERENCIA:
            # Para transferencia, estos campos son requeridos
            field_name = cls.__fields__[v].name if hasattr(cls.__fields__.get(v, None), 'name') else None
            if field_name in ['account_number', 'dni', 'bank', 'account_holder']:
                if not v:
                    raise ValueError(f'{field_name} es requerido para Transferencia Bancaria')
        return v

class PaymentMethodUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    dni: Optional[str] = None
    bank: Optional[str] = None
    account_holder: Optional[str] = None
    account_number: Optional[str] = None
    is_active: Optional[bool] = None

class PaymentMethodResponse(PaymentMethodBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

