"""
Controlador de roles usando PyNest
"""
from nest.core import Controller, Get, Post, Delete, Depends
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
from .roles_service import RolesService
from ...core.database import get_db
from ...models.user import User
from ...utils.dependencies import get_current_user


@Controller("api/roles")
class RolesController:
    """Controlador para rutas de roles"""
    
    def __init__(self, service: RolesService):
        self.service = service
    
    @Get("/")
    def get_roles(
        self,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Obtener roles del negocio"""
        return self.service.get_roles(
            current_user.business_id,
            skip,
            limit,
            db
        )
    
    @Get("/user/{user_id}/roles")
    def get_user_roles(
        self,
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Obtener roles de un usuario"""
        return self.service.get_user_roles(
            user_id,
            current_user.business_id,
            db
        )
    
    @Get("/{role_id}")
    def get_role(
        self,
        role_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Obtener rol por ID"""
        return self.service.get_role_by_id(
            role_id,
            current_user.business_id,
            db
        )
    
    @Delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_role(
        self,
        role_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Eliminar rol"""
        self.service.delete_role(
            role_id,
            current_user.business_id,
            db
        )
        return None

