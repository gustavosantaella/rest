from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PermissionBase(BaseModel):
    can_access_dashboard: bool = True
    can_access_inventory: bool = False
    can_access_products: bool = False
    can_access_menu: bool = False
    can_access_tables: bool = False
    can_access_orders: bool = False
    can_access_users: bool = False
    can_access_configuration: bool = False
    can_access_reports: bool = False


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    can_access_dashboard: Optional[bool] = None
    can_access_inventory: Optional[bool] = None
    can_access_products: Optional[bool] = None
    can_access_menu: Optional[bool] = None
    can_access_tables: Optional[bool] = None
    can_access_orders: Optional[bool] = None
    can_access_users: Optional[bool] = None
    can_access_configuration: Optional[bool] = None
    can_access_reports: Optional[bool] = None


class PermissionResponse(PermissionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

