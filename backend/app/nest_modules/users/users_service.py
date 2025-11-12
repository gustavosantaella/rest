"""
Servicio de usuarios usando PyNest
"""
from nest.core import Injectable
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from ...models.user import User
from ...models.configuration import BusinessConfiguration
from ...schemas.user import UserCreate, UserUpdate, UserResponse
from ...utils.security import get_password_hash


@Injectable
class UsersService:
    """Servicio para manejo de usuarios"""
    
    def __init__(self):
        pass
    
    def build_user_response(self, user: User, db: Session) -> UserResponse:
        """Construye respuesta del usuario con el nombre del negocio y roles personalizados"""
        business_name = None
        if user.business_id:
            business = db.query(BusinessConfiguration).filter(
                BusinessConfiguration.id == user.business_id
            ).first()
            if business:
                business_name = business.business_name
        
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            dni=user.dni,
            country=user.country,
            business_id=user.business_id,
            is_active=user.is_active,
            created_at=user.created_at,
            business_name=business_name,
            custom_roles=[{"id": r.id, "name": r.name} for r in user.custom_roles] if user.custom_roles else []
        )
    
    def get_current_user_info(self, user: User, db: Session) -> UserResponse:
        """Obtener información del usuario actual"""
        return self.build_user_response(user, db)
    
    def create_user(
        self,
        user_data: UserCreate,
        business_id: int,
        db: Session
    ) -> User:
        """Crear nuevo usuario"""
        # Verificar email duplicado
        existing = db.query(User).filter(
            User.email == user_data.email,
            User.business_id == business_id,
            User.deleted_at.is_(None)
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado en tu negocio"
            )
        
        # Verificar username duplicado
        existing = db.query(User).filter(
            User.username == user_data.username,
            User.business_id == business_id,
            User.deleted_at.is_(None)
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está registrado en tu negocio"
            )
        
        # Crear usuario
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            business_id=business_id,
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            role=user_data.role,
            dni=user_data.dni,
            country=user_data.country,
            is_active=True,
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    def get_users(
        self,
        business_id: int,
        skip: int,
        limit: int,
        db: Session
    ) -> List[User]:
        """Obtener lista de usuarios"""
        return db.query(User).options(
            joinedload(User.custom_roles)
        ).filter(
            User.business_id == business_id,
            User.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    
    def get_user_by_id(self, user_id: int, business_id: int, db: Session) -> User:
        """Obtener usuario por ID"""
        user = db.query(User).filter(
            User.id == user_id,
            User.business_id == business_id,
            User.deleted_at.is_(None)
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        return user
    
    def update_user(
        self,
        user_id: int,
        user_update: UserUpdate,
        business_id: int,
        db: Session
    ) -> User:
        """Actualizar usuario"""
        user = self.get_user_by_id(user_id, business_id, db)
        
        update_data = user_update.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        # No permitir cambiar business_id
        if "business_id" in update_data:
            del update_data["business_id"]
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    def delete_user(self, user_id: int, business_id: int, db: Session) -> None:
        """Eliminar usuario (soft delete)"""
        user = self.get_user_by_id(user_id, business_id, db)
        
        # No permitir eliminar el último administrador
        admin_count = db.query(User).filter(
            User.business_id == business_id,
            User.role == "admin",
            User.is_active == True,
            User.deleted_at.is_(None)
        ).count()
        
        if user.role == "admin" and admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes eliminar el último administrador del negocio"
            )
        
        user.deleted_at = datetime.now()
        db.commit()

