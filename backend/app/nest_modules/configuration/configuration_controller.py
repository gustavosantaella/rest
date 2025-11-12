"""
Controlador de configuración usando PyNest
"""
from nest.core import Controller, Get, Post, Put, Delete, Depends
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
from .configuration_service import ConfigurationService
from ...core.database import get_db
from ...models.user import User
from ...schemas.configuration import (
    BusinessConfigurationResponse, BusinessConfigurationUpdate,
    PartnerCreate, PartnerUpdate, PartnerResponse
)
from ...utils.dependencies import get_current_user, get_current_active_admin


@Controller("api/configuration")
class ConfigurationController:
    """Controlador para rutas de configuración"""
    
    def __init__(self, service: ConfigurationService):
        self.service = service
    
    @Get("/")
    def get_configuration(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> BusinessConfigurationResponse:
        """Obtener configuración del negocio"""
        return self.service.get_configuration(current_user.business_id, db)
    
    @Put("/")
    def update_configuration(
        self,
        config_update: BusinessConfigurationUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> BusinessConfigurationResponse:
        """Actualizar configuración del negocio"""
        return self.service.update_configuration(
            config_update,
            current_user.business_id,
            db
        )
    
    # Endpoints de Partners
    @Get("/partners")
    def get_partners(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[PartnerResponse]:
        """Obtener socios del negocio"""
        return self.service.get_partners(current_user.business_id, db)
    
    @Post("/partners", status_code=status.HTTP_201_CREATED)
    def create_partner(
        self,
        partner: PartnerCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> PartnerResponse:
        """Crear nuevo socio"""
        return self.service.create_partner(partner, current_user.business_id, db)
    
    @Put("/partners/{partner_id}")
    def update_partner(
        self,
        partner_id: int,
        partner_update: PartnerUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> PartnerResponse:
        """Actualizar socio"""
        return self.service.update_partner(
            partner_id,
            partner_update,
            current_user.business_id,
            db
        )
    
    @Delete("/partners/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_partner(
        self,
        partner_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ):
        """Eliminar socio"""
        self.service.delete_partner(partner_id, current_user.business_id, db)
        return None

