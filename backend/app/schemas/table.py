from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.table import TableStatus


class TableBase(BaseModel):
    number: str
    capacity: int
    location: Optional[str] = None


class TableCreate(TableBase):
    pass


class TableUpdate(BaseModel):
    number: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[TableStatus] = None
    location: Optional[str] = None


class TableResponse(TableBase):
    id: int
    status: TableStatus
    created_at: datetime
    
    class Config:
        from_attributes = True

