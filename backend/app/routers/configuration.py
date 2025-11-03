from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import re
import qrcode
from io import BytesIO
from ..database import get_db
from ..models.configuration import BusinessConfiguration, Partner
from ..models.user import User, UserRole
from ..schemas.configuration import (
    BusinessConfigurationCreate, BusinessConfigurationUpdate, BusinessConfigurationResponse,
    PartnerCreate, PartnerUpdate, PartnerResponse
)
from ..utils.dependencies import get_current_active_admin

router = APIRouter(prefix="/configuration", tags=["configuration"])


def generate_slug(business_name: str, db: Session, exclude_id: int = None) -> str:
    """Genera un slug único a partir del nombre del negocio"""
    # Convertir a minúsculas y eliminar caracteres especiales
    slug = business_name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.strip('-')
    slug = slug or 'mi-negocio'
    
    # Asegurar que el slug es único
    counter = 1
    original_slug = slug
    while True:
        query = db.query(BusinessConfiguration).filter(BusinessConfiguration.slug == slug)
        if exclude_id:
            query = query.filter(BusinessConfiguration.id != exclude_id)
        
        if query.first() is None:
            break
        
        slug = f"{original_slug}-{counter}"
        counter += 1
    
    return slug


# CONFIGURACIÓN DEL NEGOCIO
@router.post("/", response_model=BusinessConfigurationResponse, status_code=status.HTTP_201_CREATED)
def create_business_configuration(
    config: BusinessConfigurationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    # Verificar si ya existe configuración
    existing = db.query(BusinessConfiguration).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La configuración del negocio ya existe. Usa PUT para actualizar.",
        )
    
    config_data = config.model_dump()
    
    # Generar slug si no se proporcionó
    if not config_data.get('slug'):
        config_data['slug'] = generate_slug(config_data['business_name'], db)
    
    new_config = BusinessConfiguration(**config_data)
    db.add(new_config)
    db.commit()
    db.refresh(new_config)
    return _build_config_response(new_config, db)


@router.get("/", response_model=BusinessConfigurationResponse)
def get_business_configuration(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    config = db.query(BusinessConfiguration).first()
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se ha configurado el negocio aún",
        )
    return _build_config_response(config, db)


@router.put("/", response_model=BusinessConfigurationResponse)
def update_business_configuration(
    config_update: BusinessConfigurationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    config = db.query(BusinessConfiguration).first()
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se ha configurado el negocio aún. Usa POST para crear.",
        )
    
    update_data = config_update.model_dump(exclude_unset=True)
    
    # Si se actualiza el nombre y no hay slug, generar uno nuevo
    if 'business_name' in update_data and not config.slug:
        update_data['slug'] = generate_slug(update_data['business_name'], db, config.id)
    
    for field, value in update_data.items():
        setattr(config, field, value)
    
    db.commit()
    db.refresh(config)
    return _build_config_response(config, db)


@router.get("/qr-code")
def get_catalog_qr_code(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    """
    Genera un código QR para el catálogo público del negocio.
    Requiere autenticación de administrador.
    """
    config = db.query(BusinessConfiguration).first()
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se ha configurado el negocio aún.",
        )
    
    if not config.slug:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El negocio no tiene un slug configurado. Actualiza la configuración primero.",
        )
    
    # URL del catálogo público (usar la URL del frontend)
    # En producción, esto debería ser configurable
    frontend_url = "http://localhost:4200"
    catalog_url = f"{frontend_url}/catalog/{config.slug}"
    
    # Generar código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(catalog_url)
    qr.make(fit=True)
    
    # Crear imagen
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar en BytesIO
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    # Retornar como imagen
    return StreamingResponse(
        buf,
        media_type="image/png",
        headers={
            "Content-Disposition": f'attachment; filename="qr-{config.slug}.png"'
        }
    )


# SOCIOS
@router.post("/partners", response_model=PartnerResponse, status_code=status.HTTP_201_CREATED)
def add_partner(
    partner: PartnerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    # Verificar que existe la configuración
    config = db.query(BusinessConfiguration).first()
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Primero debes crear la configuración del negocio",
        )
    
    # Verificar que el usuario existe y es admin
    user = db.query(User).filter(User.id == partner.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los socios deben ser usuarios administradores",
        )
    
    # Verificar que el porcentaje total no exceda 100%
    total_percentage = sum([p.participation_percentage for p in config.partners if p.is_active])
    if total_percentage + partner.participation_percentage > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El porcentaje total de participación excedería 100% (actual: {total_percentage}%)",
        )
    
    new_partner = Partner(
        business_config_id=config.id,
        **partner.model_dump()
    )
    
    db.add(new_partner)
    db.commit()
    db.refresh(new_partner)
    return _build_partner_response(new_partner, db)


@router.get("/partners", response_model=List[PartnerResponse])
def get_partners(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    config = db.query(BusinessConfiguration).first()
    if not config:
        return []
    
    return [_build_partner_response(p, db) for p in config.partners]


@router.put("/partners/{partner_id}", response_model=PartnerResponse)
def update_partner(
    partner_id: int,
    partner_update: PartnerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Socio no encontrado",
        )
    
    # Si se actualiza el porcentaje, verificar que no exceda 100%
    if partner_update.participation_percentage is not None:
        config = db.query(BusinessConfiguration).filter(BusinessConfiguration.id == partner.business_config_id).first()
        total_percentage = sum([
            p.participation_percentage 
            for p in config.partners 
            if p.is_active and p.id != partner_id
        ])
        
        if total_percentage + partner_update.participation_percentage > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El porcentaje total excedería 100% (actual sin este socio: {total_percentage}%)",
            )
    
    update_data = partner_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(partner, field, value)
    
    db.commit()
    db.refresh(partner)
    return _build_partner_response(partner, db)


@router.delete("/partners/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_partner(
    partner_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Socio no encontrado",
        )
    
    db.delete(partner)
    db.commit()
    return None


# Helper functions
def _build_config_response(config: BusinessConfiguration, db: Session) -> BusinessConfigurationResponse:
    partners = [_build_partner_response(p, db) for p in config.partners]
    
    return BusinessConfigurationResponse(
        id=config.id,
        business_name=config.business_name,
        slug=config.slug,
        legal_name=config.legal_name,
        rif=config.rif,
        phone=config.phone,
        email=config.email,
        address=config.address,
        tax_rate=config.tax_rate,
        currency=config.currency,
        logo_url=config.logo_url,
        created_at=config.created_at,
        updated_at=config.updated_at,
        partners=partners
    )


def _build_partner_response(partner: Partner, db: Session) -> PartnerResponse:
    user = db.query(User).filter(User.id == partner.user_id).first()
    
    return PartnerResponse(
        id=partner.id,
        business_config_id=partner.business_config_id,
        user_id=partner.user_id,
        participation_percentage=partner.participation_percentage,
        investment_amount=partner.investment_amount,
        join_date=partner.join_date,
        is_active=partner.is_active,
        notes=partner.notes,
        created_at=partner.created_at,
        updated_at=partner.updated_at,
        user_name=user.full_name if user else None,
        user_email=user.email if user else None
    )

