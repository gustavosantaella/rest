from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


# Tabla de relación muchos a muchos entre Role y Permission
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)


# Tabla de relación muchos a muchos entre User y Role
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)


class Role(Base):
    """
    Roles personalizados del sistema
    Ej: "Mesero de Turno Mañana", "Supervisor de Cocina", etc.
    """
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_configuration.id", ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    
    # Relaciones
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    users = relationship("User", secondary=user_roles, back_populates="custom_roles")


class Permission(Base):
    """
    Permisos granulares del sistema
    Ej: "products.create", "orders.view", "reports.generate", etc.
    """
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)  # Ej: "products.create"
    name = Column(String, nullable=False)  # Ej: "Crear Productos"
    description = Column(Text)
    module = Column(String, nullable=False, index=True)  # Ej: "products", "orders", "users"
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

