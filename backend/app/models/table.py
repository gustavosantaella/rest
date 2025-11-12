from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
import enum
from ..database import Base


class TableStatus(str, enum.Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    CLEANING = "cleaning"


class Table(Base):
    __tablename__ = "tables"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_configuration.id"), nullable=False, index=True)
    number = Column(String, nullable=False, index=True)
    capacity = Column(Integer, nullable=False)
    status = Column(Enum(TableStatus), default=TableStatus.AVAILABLE, nullable=False)
    location = Column(String)  # Zona del restaurante (terraza, interior, etc.)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete

