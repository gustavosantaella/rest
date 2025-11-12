"""
Repositorio de autenticación - Operaciones de base de datos
"""
from sqlalchemy.orm import Session
from typing import Optional
from ...models.user import User, UserRole
from ...models.configuration import BusinessConfiguration


class AuthRepository:
    """Repositorio para operaciones de BD de autenticación"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_user_by_email(self, email: str) -> Optional[User]:
        """Buscar usuario por email (en todos los negocios, para login/registro)"""
        return self.db.query(User).filter(
            User.email == email,
            User.deleted_at.is_(None)
        ).first()
    
    def find_user_by_username(self, username: str) -> Optional[User]:
        """Buscar usuario por username (en todos los negocios, para login)"""
        return self.db.query(User).filter(
            User.username == username,
            User.deleted_at.is_(None)
        ).first()
    
    def find_business_by_slug(self, slug: str) -> Optional[BusinessConfiguration]:
        """Buscar negocio por slug"""
        return self.db.query(BusinessConfiguration).filter(
            BusinessConfiguration.slug == slug
        ).first()
    
    def create_business(self, business_data: dict) -> BusinessConfiguration:
        """Crear nuevo negocio"""
        business = BusinessConfiguration(**business_data)
        self.db.add(business)
        self.db.flush()  # Para obtener el ID sin commit
        return business
    
    def create_user(self, user_data: dict) -> User:
        """Crear nuevo usuario"""
        user = User(**user_data)
        self.db.add(user)
        return user
    
    def commit(self):
        """Commit de la transacción"""
        self.db.commit()
    
    def rollback(self):
        """Rollback de la transacción"""
        self.db.rollback()
    
    def refresh(self, obj):
        """Refresh de un objeto"""
        self.db.refresh(obj)

