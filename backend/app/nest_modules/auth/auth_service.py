"""
Servicio de autenticación usando PyNest - Solo lógica de negocio
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
import re
from .auth_repository import AuthRepository
from ...models.user import UserRole
from ...schemas.auth import RegisterRequest, RegisterResponse
from ...schemas.user import Token
from ...utils.security import verify_password, get_password_hash, create_access_token
from ...config import settings


@Injectable
class AuthService:
    """Servicio para lógica de negocio de autenticación"""
    
    def __init__(self):
        pass
    
    def generate_slug(self, business_name: str, auth_repo: AuthRepository) -> str:
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
            existing = auth_repo.find_business_by_slug(slug)
            if not existing:
                break
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        return slug
    
    def register(self, register_data: RegisterRequest, db: Session) -> RegisterResponse:
        """
        Registro público: Crea un nuevo negocio con su usuario administrador.
        No requiere autenticación.
        """
        auth_repo = AuthRepository(db)
        
        # Validar si el email ya está registrado
        if auth_repo.find_user_by_email(register_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado en el sistema",
            )
        
        # Validar longitud de contraseña
        if len(register_data.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña debe tener al menos 8 caracteres",
            )
        
        try:
            # 1. Crear configuración del negocio
            slug = self.generate_slug(register_data.business_name, auth_repo)
            
            new_business = auth_repo.create_business({
                'business_name': register_data.business_name,
                'slug': slug,
                'legal_name': register_data.legal_name,
                'phone': register_data.phone,
                'tax_rate': 0.16,
                'currency': 'USD'
            })
            
            # 2. Crear usuario administrador del negocio
            username = register_data.email.split('@')[0]
            
            new_user = auth_repo.create_user({
                'business_id': new_business.id,
                'username': username,
                'email': register_data.email,
                'full_name': register_data.full_name,
                'hashed_password': get_password_hash(register_data.password),
                'role': UserRole.ADMIN,
                'is_active': True
            })
            
            # 3. Commit de ambos
            auth_repo.commit()
            auth_repo.refresh(new_business)
            auth_repo.refresh(new_user)
            
            return RegisterResponse(
                message="Negocio y usuario creados exitosamente",
                business_slug=new_business.slug,
                user_email=new_user.email
            )
            
        except Exception as e:
            auth_repo.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear el negocio: {str(e)}"
            )
    
    def login(self, username: str, password: str, db: Session) -> Token:
        """Autenticar usuario y generar token"""
        auth_repo = AuthRepository(db)
        
        # Buscar usuario
        user = auth_repo.find_user_by_username(username)
        
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo"
            )
        
        # Crear token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")

