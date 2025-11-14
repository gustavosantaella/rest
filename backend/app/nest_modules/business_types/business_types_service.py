"""
Servicio de tipos de negocios
"""

from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from .business_types_repository import BusinessTypesRepository
from ...schemas.business_type import BusinessTypeCreate, BusinessTypeUpdate, BusinessTypeResponse
from ...models.business_type import BusinessType


@Injectable
class BusinessTypesService:
    """Servicio para lógica de negocio de tipos de negocios"""
    
    def get_all(self, db: Session) -> List[BusinessTypeResponse]:
        """Obtener todos los tipos de negocios activos"""
        repo = BusinessTypesRepository(db)
        types = repo.get_all()
        return [BusinessTypeResponse.model_validate(t, from_attributes=True) for t in types]
    
    def get_by_id(self, business_type_id: int, db: Session) -> BusinessTypeResponse:
        """Obtener tipo de negocio por ID"""
        repo = BusinessTypesRepository(db)
        business_type = repo.get_by_id(business_type_id)
        
        if not business_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de negocio no encontrado"
            )
        
        return BusinessTypeResponse.model_validate(business_type)
    
    def get_by_slug(self, slug: str, db: Session) -> BusinessTypeResponse:
        """Obtener tipo de negocio por slug"""
        repo = BusinessTypesRepository(db)
        business_type = repo.get_by_slug(slug)
        
        if not business_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de negocio no encontrado"
            )
        
        return BusinessTypeResponse.model_validate(business_type)
    
    def create(self, business_type_data: BusinessTypeCreate, db: Session) -> BusinessTypeResponse:
        """Crear nuevo tipo de negocio"""
        repo = BusinessTypesRepository(db)
        
        # Verificar si el slug ya existe
        existing = repo.get_by_slug(business_type_data.slug)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un tipo de negocio con este slug"
            )
        
        business_type = repo.create(business_type_data.model_dump())
        return BusinessTypeResponse.model_validate(business_type)
    
    def update(self, business_type_id: int, update_data: BusinessTypeUpdate, db: Session) -> BusinessTypeResponse:
        """Actualizar tipo de negocio"""
        repo = BusinessTypesRepository(db)
        
        # Si se actualiza el slug, verificar que no exista
        if update_data.slug:
            existing = repo.get_by_slug(update_data.slug)
            if existing and existing.id != business_type_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un tipo de negocio con este slug"
                )
        
        business_type = repo.update(business_type_id, update_data.model_dump(exclude_unset=True))
        
        if not business_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de negocio no encontrado"
            )
        
        return BusinessTypeResponse.model_validate(business_type)
    
    def delete(self, business_type_id: int, db: Session) -> dict:
        """Eliminar tipo de negocio"""
        repo = BusinessTypesRepository(db)
        success = repo.delete(business_type_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de negocio no encontrado"
            )
        
        return {"message": "Tipo de negocio eliminado exitosamente"}

