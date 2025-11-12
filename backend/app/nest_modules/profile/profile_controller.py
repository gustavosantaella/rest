"""
Controlador de perfil usando PyNest
"""
from nest.core import Controller, Get, Put, Post, Depends
from fastapi import status
from sqlalchemy.orm import Session
from .profile_service import ProfileService
from ...core.database import get_db
from ...models.user import User
from ...schemas.user import UserResponse
from ...schemas.profile import ProfileUpdate, PasswordChange
from ...utils.dependencies import get_current_user


@Controller("api/profile")
class ProfileController:
    """Controlador para rutas de perfil"""
    
    def __init__(self, profile_service: ProfileService):
        self.profile_service = profile_service
    
    @Get("/me")
    def get_my_profile(
        self,
        current_user: User = Depends(get_current_user)
    ) -> UserResponse:
        """Obtener perfil del usuario actual"""
        return self.profile_service.get_my_profile(current_user)
    
    @Get("/my-permissions")
    def get_my_permissions(
        self,
        current_user: User = Depends(get_current_user)
    ):
        """Ver todos los permisos del usuario actual"""
        return self.profile_service.get_my_permissions(current_user)
    
    @Put("/me")
    def update_my_profile(
        self,
        profile_update: ProfileUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> UserResponse:
        """Actualizar perfil del usuario actual"""
        return self.profile_service.update_profile(current_user, profile_update, db)
    
    @Post("/change-password", status_code=status.HTTP_200_OK)
    def change_password(
        self,
        password_data: PasswordChange,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        """Cambiar contraseña del usuario actual"""
        return self.profile_service.change_password(current_user, password_data, db)

