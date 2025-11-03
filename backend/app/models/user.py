from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    WAITER = "waiter"
    CASHIER = "cashier"
    CHEF = "chef"  # Cocinero


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_configuration.id", ondelete='CASCADE'), nullable=True, index=True)
    username = Column(String, index=True, nullable=False)  # Ya no es unique globalmente
    email = Column(String, index=True, nullable=False)  # Ya no es unique globalmente
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.WAITER, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Información adicional del perfil
    dni = Column(String, index=True)  # Ya no es unique globalmente
    country = Column(String)  # País
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    
    # Relaciones
    business = relationship("BusinessConfiguration", back_populates="users")
    permissions = relationship("UserPermission", back_populates="user", uselist=False, cascade="all, delete-orphan")
    custom_roles = relationship("Role", secondary="user_roles", back_populates="users")

