"""
Servicio de usuarios usando PyNest - Solo lógica de negocio
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from .users_repository import UserRepository, BusinessRepository
from ...models.user import User
from ...schemas.user import UserCreate, UserUpdate, UserResponse
from ...utils.security import get_password_hash


@Injectable
class UsersService:
    """Servicio para lógica de negocio de usuarios"""
    
    def __init__(self):
        pass
    
    def build_user_response(self, user: User, db: Session) -> UserResponse:
        """Construye respuesta del usuario con el nombre del negocio y roles personalizados"""
        business_repo = BusinessRepository(db)
        business_name = None
        
        if user.business_id:
            business = business_repo.find_by_id(user.business_id)
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
        """Crear nuevo usuario con validaciones"""
        user_repo = UserRepository(db)
        
        # Validar email duplicado
        if user_repo.find_by_email(user_data.email, business_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado en tu negocio"
            )
        
        # Validar username duplicado
        if user_repo.find_by_username(user_data.username, business_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está registrado en tu negocio"
            )
        
        # Crear usuario
        user_dict = {
            'business_id': business_id,
            'username': user_data.username,
            'email': user_data.email,
            'full_name': user_data.full_name,
            'hashed_password': get_password_hash(user_data.password),
            'role': user_data.role,
            'dni': user_data.dni,
            'country': user_data.country,
            'is_active': True,
        }
        return user_repo.create(user_dict)
    
    def get_users(
        self,
        business_id: int,
        skip: int,
        limit: int,
        db: Session
    ) -> List[User]:
        """Obtener lista de usuarios"""
        user_repo = UserRepository(db)
        return user_repo.find_all(business_id, skip, limit)
    
    def get_user_by_id(self, user_id: int, business_id: int, db: Session) -> User:
        """Obtener usuario por ID con validación"""
        user_repo = UserRepository(db)
        user = user_repo.find_by_id(user_id, business_id)
        
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
        """Actualizar usuario con validaciones"""
        user_repo = UserRepository(db)
        
        # Validar que el usuario existe
        user = user_repo.find_by_id(user_id, business_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Preparar datos de actualización
        update_data = user_update.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        # No permitir cambiar business_id
        if "business_id" in update_data:
            del update_data["business_id"]
        
        return user_repo.update(user, update_data)
    
    def delete_user(self, user_id: int, business_id: int, db: Session) -> None:
        """Eliminar usuario (soft delete) con validaciones"""
        user_repo = UserRepository(db)
        
        # Validar que el usuario existe
        user = user_repo.find_by_id(user_id, business_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # No permitir eliminar el último administrador
        if user.role == "admin":
            admin_count = user_repo.count_admins(business_id)
            if admin_count <= 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No puedes eliminar el último administrador del negocio"
                )
        
        user_repo.soft_delete(user)


