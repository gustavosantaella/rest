from pydantic import BaseModel, EmailStr
from typing import Optional


class ProfileUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    dni: Optional[str] = None
    country: Optional[str] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str

