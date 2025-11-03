from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Permission Schemas
class PermissionBase(BaseModel):
    code: str  # Ej: "products.create"
    name: str  # Ej: "Crear Productos"
    description: Optional[str] = None
    module: str  # Ej: "products", "orders", "users"


class PermissionCreate(PermissionBase):
    pass


class PermissionResponse(PermissionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Role Schemas
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True


class RoleCreate(RoleBase):
    permission_ids: List[int] = []  # IDs de permisos a asignar


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    permission_ids: Optional[List[int]] = None


class RoleResponse(RoleBase):
    id: int
    business_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    permissions: List[PermissionResponse] = []

    class Config:
        from_attributes = True


# User Roles Assignment
class UserRolesUpdate(BaseModel):
    role_ids: List[int]  # IDs de roles a asignar al usuario


class UserRolesResponse(BaseModel):
    user_id: int
    roles: List[RoleResponse]

    class Config:
        from_attributes = True

