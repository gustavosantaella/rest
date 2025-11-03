from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from ..models.user import UserRole


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.WAITER
    dni: Optional[str] = None
    country: Optional[str] = None
    business_id: Optional[int] = None


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str
    role: Optional[UserRole] = UserRole.WAITER  # Rol por defecto si no se especifica
    dni: Optional[str] = None
    country: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    dni: Optional[str] = None
    country: Optional[str] = None


# Simple role info para evitar importación circular
class SimpleRoleInfo(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    business_name: Optional[str] = None  # Nombre del negocio al que pertenece
    custom_roles: List[SimpleRoleInfo] = []  # Roles personalizados asignados
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    
    
class LoginRequest(BaseModel):
    username: str
    password: str

