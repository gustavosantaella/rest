"""
Repositorio de usuarios - Operaciones de base de datos
"""
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from ...models.user import User
from ...models.configuration import BusinessConfiguration


class UserRepository:
    """Repositorio para operaciones de BD de usuarios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, user_id: int, business_id: int) -> Optional[User]:
        """Buscar usuario por ID en un negocio"""
        return self.db.query(User).filter(
            User.id == user_id,
            User.business_id == business_id,
            User.deleted_at.is_(None)
        ).first()
    
    def find_by_email(self, email: str, business_id: int) -> Optional[User]:
        """Buscar usuario por email en un negocio"""
        return self.db.query(User).filter(
            User.email == email,
            User.business_id == business_id,
            User.deleted_at.is_(None)
        ).first()
    
    def find_by_username(self, username: str, business_id: int) -> Optional[User]:
        """Buscar usuario por username en un negocio"""
        return self.db.query(User).filter(
            User.username == username,
            User.business_id == business_id,
            User.deleted_at.is_(None)
        ).first()
    
    def find_all(
        self,
        business_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Obtener todos los usuarios de un negocio"""
        return self.db.query(User).options(
            joinedload(User.custom_roles)
        ).filter(
            User.business_id == business_id,
            User.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    
    def create(self, user_data: dict) -> User:
        """Crear nuevo usuario"""
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user: User, update_data: dict) -> User:
        """Actualizar usuario existente"""
        for field, value in update_data.items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def soft_delete(self, user: User) -> None:
        """Eliminar usuario (soft delete)"""
        user.deleted_at = datetime.now()
        self.db.commit()
    
    def count_admins(self, business_id: int) -> int:
        """Contar administradores activos de un negocio"""
        return self.db.query(User).filter(
            User.business_id == business_id,
            User.role == "admin",
            User.is_active == True,
            User.deleted_at.is_(None)
        ).count()


class BusinessRepository:
    """Repositorio para operaciones de configuración de negocios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, business_id: int) -> Optional[BusinessConfiguration]:
        """Buscar configuración de negocio por ID"""
        return self.db.query(BusinessConfiguration).filter(
            BusinessConfiguration.id == business_id
        ).first()

