"""
Servicio de configuración usando PyNest - Lógica de negocio
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .configuration_repository import ConfigurationRepository, PartnerRepository
from ...models.configuration import BusinessConfiguration, Partner
from ...schemas.configuration import BusinessConfigurationUpdate, PartnerCreate, PartnerUpdate


@Injectable
class ConfigurationService:
    """Servicio para lógica de negocio de configuración"""
    
    def __init__(self):
        pass
    
    def get_configuration(self, business_id: int, db: Session) -> BusinessConfiguration:
        """Obtener configuración del negocio"""
        repo = ConfigurationRepository(db)
        config = repo.find_by_business_id(business_id)
        
        if not config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se ha configurado el negocio aún"
            )
        
        return config
    
    def update_configuration(
        self,
        config_update: BusinessConfigurationUpdate,
        business_id: int,
        db: Session
    ) -> BusinessConfiguration:
        """Actualizar configuración del negocio"""
        repo = ConfigurationRepository(db)
        config = repo.find_by_business_id(business_id)
        
        if not config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se ha configurado el negocio aún"
            )
        
        update_data = config_update.model_dump(exclude_unset=True)
        return repo.update(config, update_data)
    
    # Métodos de Partners
    def get_partners(self, business_id: int, db: Session):
        """Obtener socios del negocio"""
        partner_repo = PartnerRepository(db)
        return partner_repo.find_all(business_id)
    
    def create_partner(self, partner_data: PartnerCreate, business_id: int, db: Session):
        """Crear nuevo socio"""
        partner_repo = PartnerRepository(db)
        
        partner_dict = partner_data.model_dump()
        partner_dict['business_config_id'] = business_id
        
        return partner_repo.create(partner_dict)
    
    def update_partner(
        self,
        partner_id: int,
        partner_update: PartnerUpdate,
        business_id: int,
        db: Session
    ):
        """Actualizar socio"""
        partner_repo = PartnerRepository(db)
        
        partner = partner_repo.find_by_id(partner_id, business_id)
        if not partner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Socio no encontrado"
            )
        
        update_data = partner_update.model_dump(exclude_unset=True)
        return partner_repo.update(partner, update_data)
    
    def delete_partner(self, partner_id: int, business_id: int, db: Session):
        """Eliminar socio"""
        partner_repo = PartnerRepository(db)
        
        partner = partner_repo.find_by_id(partner_id, business_id)
        if not partner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Socio no encontrado"
            )
        
        partner_repo.delete(partner)

