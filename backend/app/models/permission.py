from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class UserPermission(Base):
    __tablename__ = "user_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    
    # Permisos por módulo
    can_access_dashboard = Column(Boolean, default=True)
    can_access_inventory = Column(Boolean, default=False)
    can_access_products = Column(Boolean, default=False)
    can_access_menu = Column(Boolean, default=False)
    can_access_tables = Column(Boolean, default=False)
    can_access_orders = Column(Boolean, default=False)
    can_access_users = Column(Boolean, default=False)
    can_access_configuration = Column(Boolean, default=False)
    can_access_reports = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con el usuario
    user = relationship("User", back_populates="permissions")

