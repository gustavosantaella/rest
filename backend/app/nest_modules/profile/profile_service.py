"""
Servicio de perfil de usuario usando PyNest - Solo lógica de negocio
"""

from nest.core import Injectable
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .profile_repository import ProfileRepository
from ...models.user import User
from ...schemas.profile import ProfileUpdate, PasswordChange
from ...utils.security import verify_password, get_password_hash
from ...utils.dependencies import get_user_permissions


@Injectable
class ProfileService:
    """Servicio para lógica de negocio del perfil de usuario"""

    def __init__(self):
        pass

    def get_my_profile(self, user: User):
        """Obtener perfil del usuario actual"""
        return user

    def get_my_permissions(self, user: User):
        """Obtener permisos del usuario actual"""
        permissions = list(get_user_permissions(user))

        return {
            "user": user.username,
            "role": user.role,
            "custom_roles": (
                [{"id": r.id, "name": r.name} for r in user.custom_roles]
                if user.custom_roles
                else []
            ),
            "permissions": permissions,
            "total_permissions": len(permissions),
        }

    def update_profile(self, user: User, profile_update: ProfileUpdate, db: Session):
        """Actualizar perfil del usuario con validaciones"""
        profile_repo = ProfileRepository(db)
        update_data = profile_update.model_dump(exclude_unset=True)

        # Validar email duplicado
        if "email" in update_data:
            existing = profile_repo.find_user_by_email(update_data["email"], user.id)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está en uso por otro usuario",
                )

        # Validar DNI duplicado
        if "dni" in update_data and update_data["dni"]:
            existing = profile_repo.find_user_by_dni(update_data["dni"], user.id)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El DNI ya está en uso por otro usuario",
                )

        # Actualizar
        return profile_repo.update_user(user.id, update_data)

    def change_password(self, user: User, password_data: PasswordChange, db: Session):
        """Cambiar contraseña del usuario con validaciones"""
        profile_repo = ProfileRepository(db)

        # Validar contraseña actual
        if not verify_password(password_data.current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña actual es incorrecta",
            )

        # Actualizar contraseña
        hashed_password = get_password_hash(password_data.new_password)
        profile_repo.update_password(user.id, hashed_password)

        return {"message": "Contraseña actualizada exitosamente"}
