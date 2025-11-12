"""
Controlador de menú usando PyNest
"""
from nest.core import Controller, Get, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from .menu_service import MenuService
from ...core.database import get_db
from ...models.user import User
from ...utils.dependencies import get_current_user


@Controller("api/menu")
class MenuController:
    """Controlador para rutas del menú"""
    
    def __init__(self, service: MenuService):
        self.service = service
    
    @Get("/categories")
    def get_menu_categories(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Obtener categorías del menú"""
        return self.service.get_menu_categories(
            current_user.business_id,
            db
        )
    
    @Get("/items")
    def get_menu_items(
        self,
        available_only: bool = False,
        category_id: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Obtener items del menú"""
        return self.service.get_menu_items(
            current_user.business_id,
            available_only,
            category_id,
            db
        )

