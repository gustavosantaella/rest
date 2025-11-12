"""
Controlador de autenticación usando PyNest
"""

from nest.core import Controller, Post, Depends
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .auth_service import AuthService
from ...core.database import get_db
from ...schemas.auth import RegisterRequest, RegisterResponse
from ...schemas.user import Token


@Controller("api/auth")
class AuthController:
    """Controlador para rutas de autenticación"""

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    @Post("/register", status_code=status.HTTP_201_CREATED)
    def register(
        self, register_data: RegisterRequest, db: Session = Depends(get_db)
    ) -> RegisterResponse:
        """Registro público de nuevo negocio y usuario administrador"""
        return self.auth_service.register(register_data, db)

    @Post("/login")
    def login(
        self,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
    ) -> Token:
        """Login de usuario"""
        return self.auth_service.login(form_data.username, form_data.password, db)
