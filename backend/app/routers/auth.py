from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import re
from ..database import get_db
from ..models.user import User, UserRole
from ..models.configuration import BusinessConfiguration
from ..schemas.user import Token, LoginRequest, UserCreate, UserResponse
from ..schemas.auth import RegisterRequest, RegisterResponse
from ..utils.security import verify_password, get_password_hash, create_access_token
from ..config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


def generate_slug(business_name: str, db: Session) -> str:
    """Genera un slug único a partir del nombre del negocio"""
    slug = business_name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.strip('-')
    slug = slug or 'mi-negocio'
    
    # Asegurar que el slug es único
    counter = 1
    original_slug = slug
    while True:
        existing = db.query(BusinessConfiguration).filter(BusinessConfiguration.slug == slug).first()
        if not existing:
            break
        slug = f"{original_slug}-{counter}"
        counter += 1
    
    return slug


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(register_data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Registro público: Crea un nuevo negocio con su usuario administrador.
    No requiere autenticación.
    """
    
    # Verificar si el email ya está registrado en algún negocio (solo usuarios no eliminados)
    existing_user = db.query(User).filter(
        User.email == register_data.email,
        User.deleted_at.is_(None)  # Solo usuarios no eliminados
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado en el sistema",
        )
    
    # Verificar longitud de contraseña
    if len(register_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 8 caracteres",
        )
    
    try:
        # 1. Crear configuración del negocio
        slug = generate_slug(register_data.business_name, db)
        
        new_business = BusinessConfiguration(
            business_name=register_data.business_name,
            slug=slug,
            legal_name=register_data.legal_name,
            phone=register_data.phone,
            tax_rate=0.16,
            currency="USD"
        )
        db.add(new_business)
        db.flush()  # Para obtener el ID sin hacer commit completo
        
        # 2. Crear usuario administrador del negocio
        username = register_data.email.split('@')[0]  # Usar parte del email como username
        hashed_password = get_password_hash(register_data.password)
        
        new_user = User(
            business_id=new_business.id,
            username=username,
            email=register_data.email,
            full_name=register_data.full_name,
            hashed_password=hashed_password,
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(new_user)
        
        # 3. Commit de ambos
        db.commit()
        db.refresh(new_business)
        db.refresh(new_user)
        
        return RegisterResponse(
            message="Negocio y usuario creados exitosamente",
            business_slug=new_business.slug,
            user_email=new_user.email
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el negocio: {str(e)}"
        )


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # Buscar usuario (solo usuarios no eliminados)
    user = db.query(User).filter(
        User.username == form_data.username,
        User.deleted_at.is_(None)  # Solo usuarios no eliminados
    ).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo"
        )

    # Crear token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
