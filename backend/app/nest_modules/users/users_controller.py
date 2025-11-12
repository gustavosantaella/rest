"""
Controlador de usuarios usando PyNest
"""

from nest.core import Controller, Get, Post, Put, Delete, Depends
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
from .users_service import UsersService
from ...core.database import get_db
from ...models.user import User
from ...schemas.user import UserResponse, UserUpdate, UserCreate
from ...utils.dependencies import get_current_user, get_current_active_admin


@Controller("api/users")
class UsersController:
    """Controlador para rutas de usuarios"""

    def __init__(self, users_service: UsersService):
        self.users_service = users_service

    @Get("/me")
    def read_users_me(
        self,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> UserResponse:
        """Obtener información del usuario actual"""
        return self.users_service.get_current_user_info(current_user, db)

    @Get("/")
    def read_users(
        self,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin),
    ) -> List[UserResponse]:
        """Obtener lista de usuarios del negocio"""
        users = self.users_service.get_users(current_user.business_id, skip, limit, db)
        return [self.users_service.build_user_response(u, db) for u in users]

    @Post("/", status_code=status.HTTP_201_CREATED)
    def create_user(
        self,
        user_data: UserCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin),
    ) -> UserResponse:
        """Crear un nuevo usuario en el negocio del administrador actual"""
        user = self.users_service.create_user(user_data, current_user.business_id, db)
        return self.users_service.build_user_response(user, db)

    @Get("/{user_id}")
    def read_user(
        self,
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin),
    ) -> UserResponse:
        """Obtener usuario por ID"""
        user = self.users_service.get_user_by_id(user_id, current_user.business_id, db)
        return self.users_service.build_user_response(user, db)

    @Put("/{user_id}")
    def update_user(
        self,
        user_id: int,
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin),
    ) -> UserResponse:
        """Actualizar usuario existente"""
        user = self.users_service.update_user(
            user_id, user_update, current_user.business_id, db
        )
        return self.users_service.build_user_response(user, db)

    @Delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_user(
        self,
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin),
    ):
        """Eliminar usuario (soft delete)"""
        self.users_service.delete_user(user_id, current_user.business_id, db)
        return None
