from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterRequest(BaseModel):
    """Schema para el registro de un nuevo negocio con su administrador"""
    
    # Datos del usuario administrador
    email: EmailStr
    password: str
    full_name: str
    
    # Datos del negocio
    business_name: str
    legal_name: Optional[str] = None
    phone: Optional[str] = None

class RegisterResponse(BaseModel):
    """Respuesta del registro"""
    message: str
    business_slug: str
    user_email: str
    
    class Config:
        from_attributes = True

