"""
Controlador de tipos de negocios usando PyNest
"""

from nest.core import Controller, Get, Post, Put, Delete, Depends
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
from .business_types_service import BusinessTypesService
from ...core.database import get_db
from ...schemas.business_type import BusinessTypeCreate, BusinessTypeUpdate, BusinessTypeResponse
from ...utils.dependencies import get_current_user, get_current_active_admin
from ...models.user import User


@Controller("api/business-types")
class BusinessTypesController:
    """Controlador para rutas de tipos de negocios"""
    
    def __init__(self, service: BusinessTypesService):
        self.service = service
    
    @Get("/")
    def get_all(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[BusinessTypeResponse]:
        """Obtener todos los tipos de negocios activos"""
        return self.service.get_all(db)
    
    @Get("/{business_type_id}")
    def get_by_id(
        self,
        business_type_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> BusinessTypeResponse:
        """Obtener tipo de negocio por ID"""
        return self.service.get_by_id(business_type_id, db)
    
    @Post("/", status_code=status.HTTP_201_CREATED)
    def create(
        self,
        business_type: BusinessTypeCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> BusinessTypeResponse:
        """Crear nuevo tipo de negocio (solo admin)"""
        return self.service.create(business_type, db)
    
    @Put("/{business_type_id}")
    def update(
        self,
        business_type_id: int,
        business_type_update: BusinessTypeUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> BusinessTypeResponse:
        """Actualizar tipo de negocio (solo admin)"""
        return self.service.update(business_type_id, business_type_update, db)
    
    @Delete("/{business_type_id}", status_code=status.HTTP_200_OK)
    def delete(
        self,
        business_type_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> dict:
        """Eliminar tipo de negocio (solo admin)"""
        return self.service.delete(business_type_id, db)

