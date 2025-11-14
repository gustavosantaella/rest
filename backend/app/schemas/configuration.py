from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .business_type import BusinessTypeResponse


class PartnerBase(BaseModel):
    user_id: int
    participation_percentage: float
    investment_amount: float = 0
    join_date: Optional[datetime] = None
    is_active: bool = True
    notes: Optional[str] = None


class PartnerCreate(PartnerBase):
    pass


class PartnerUpdate(BaseModel):
    participation_percentage: Optional[float] = None
    investment_amount: Optional[float] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class PartnerResponse(PartnerBase):
    id: int
    business_config_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Información del usuario
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    
    class Config:
        from_attributes = True


class BusinessConfigurationBase(BaseModel):
    business_name: str
    slug: Optional[str] = None
    legal_name: Optional[str] = None
    rif: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    tax_rate: float = 0.16
    currency: str = "USD"
    logo_url: Optional[str] = None
    business_type_id: Optional[int] = None


class BusinessConfigurationCreate(BusinessConfigurationBase):
    pass


class BusinessConfigurationUpdate(BaseModel):
    business_name: Optional[str] = None
    slug: Optional[str] = None
    legal_name: Optional[str] = None
    rif: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    tax_rate: Optional[float] = None
    currency: Optional[str] = None
    logo_url: Optional[str] = None
    business_type_id: Optional[int] = None


class BusinessConfigurationResponse(BusinessConfigurationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    partners: List[PartnerResponse] = []
    business_type: Optional[BusinessTypeResponse] = None  # Información del tipo de negocio
    
    class Config:
        from_attributes = True

