"""
Controlador de permisos usando PyNest
"""
from nest.core import Controller, Get, Depends
from sqlalchemy.orm import Session
from typing import List
from .permissions_service import PermissionsService
from ...core.database import get_db
from ...models.user import User
from ...utils.dependencies import get_current_user


@Controller("api/permissions")
class PermissionsController:
    """Controlador para rutas de permisos"""
    
    def __init__(self, service: PermissionsService):
        self.service = service
    
    @Get("/")
    def get_permissions(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Obtener todos los permisos"""
        return self.service.get_all_permissions(db)


@Controller("api/system-permissions")
class SystemPermissionsController:
    """Controlador para permisos del sistema"""
    
    def __init__(self, service: PermissionsService):
        self.service = service
    
    @Get("/by-module")
    def get_permissions_by_module(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Obtener permisos agrupados por módulo"""
        return self.service.get_permissions_by_module(db)

