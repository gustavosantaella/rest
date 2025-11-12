"""
Repositorio de perfil - Operaciones de base de datos
"""
from sqlalchemy.orm import Session
from typing import Optional
from ...models.user import User


class ProfileRepository:
    """Repositorio para operaciones de BD de perfil"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_user_by_email(self, email: str, exclude_user_id: int) -> Optional[User]:
        """Buscar otro usuario con el mismo email"""
        return self.db.query(User).filter(
            User.email == email,
            User.id != exclude_user_id
        ).first()
    
    def find_user_by_dni(self, dni: str, exclude_user_id: int) -> Optional[User]:
        """Buscar otro usuario con el mismo DNI"""
        return self.db.query(User).filter(
            User.dni == dni,
            User.id != exclude_user_id
        ).first()
    
    def update_user(self, user: User, update_data: dict) -> User:
        """Actualizar datos del usuario"""
        for field, value in update_data.items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_password(self, user: User, hashed_password: str):
        """Actualizar contraseña del usuario"""
        user.hashed_password = hashed_password
        self.db.commit()

