"""
Repositorio de roles - Operaciones de base de datos
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ...models.role_permission import Role
from ...models.user import User


class RolesRepository:
    """Repositorio para operaciones de BD de roles"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self, business_id: int, skip: int = 0, limit: int = 100) -> List[Role]:
        """Obtener todos los roles de un negocio"""
        return self.db.query(Role).filter(
            Role.business_id == business_id,
            Role.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    
    def find_by_id(self, role_id: int, business_id: int) -> Optional[Role]:
        """Buscar rol por ID"""
        return self.db.query(Role).filter(
            Role.id == role_id,
            Role.business_id == business_id,
            Role.deleted_at.is_(None)
        ).first()
    
    def find_by_name(self, name: str, business_id: int) -> Optional[Role]:
        """Buscar rol por nombre"""
        return self.db.query(Role).filter(
            Role.name == name,
            Role.business_id == business_id,
            Role.deleted_at.is_(None)
        ).first()
    
    def find_by_user_id(self, user_id: int, business_id: int) -> List[Role]:
        """Obtener roles de un usuario"""
        user = self.db.query(User).filter(
            User.id == user_id,
            User.business_id == business_id
        ).first()
        
        return user.custom_roles if user and user.custom_roles else []
    
    def create(self, role_data: dict) -> Role:
        """Crear nuevo rol"""
        role = Role(**role_data)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def update(self, role: Role, update_data: dict) -> Role:
        """Actualizar rol"""
        for field, value in update_data.items():
            setattr(role, field, value)
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def soft_delete(self, role: Role) -> None:
        """Eliminar rol (soft delete)"""
        role.deleted_at = datetime.now()
        self.db.commit()

