"""
Controlador de menú usando PyNest
"""
from nest.core import Controller, Get, Post, Put, Delete, Depends
from fastapi import status
from sqlalchemy.orm import Session
from typing import List, Optional
from .menu_service import MenuService
from ...core.database import get_db
from ...models.user import User
from ...schemas.menu import (
    MenuCategoryCreate, MenuCategoryUpdate, MenuCategoryResponse,
    MenuItemCreate, MenuItemUpdate, MenuItemResponse
)
from ...utils.dependencies import get_current_user, get_current_active_manager


@Controller("api/menu")
class MenuController:
    """Controlador para rutas del menú"""
    
    def __init__(self, service: MenuService):
        self.service = service
    
    # Endpoints de categorías
    @Get("/categories")
    def get_menu_categories(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[MenuCategoryResponse]:
        """Obtener categorías del menú"""
        return self.service.get_menu_categories(
            current_user.business_id,
            db
        )
    
    @Post("/categories", status_code=status.HTTP_201_CREATED)
    def create_menu_category(
        self,
        category: MenuCategoryCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_manager)
    ) -> MenuCategoryResponse:
        """Crear nueva categoría del menú"""
        return self.service.create_menu_category(
            category,
            current_user.business_id,
            db
        )
    
    @Put("/categories/{category_id}")
    def update_menu_category(
        self,
        category_id: int,
        category_update: MenuCategoryUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_manager)
    ) -> MenuCategoryResponse:
        """Actualizar categoría del menú"""
        return self.service.update_menu_category(
            category_id,
            category_update,
            current_user.business_id,
            db
        )
    
    @Delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_menu_category(
        self,
        category_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_manager)
    ):
        """Eliminar categoría del menú"""
        self.service.delete_menu_category(
            category_id,
            current_user.business_id,
            db
        )
        return None
    
    # Endpoints de items
    @Get("/items")
    def get_menu_items(
        self,
        available_only: bool = False,
        category_id: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[MenuItemResponse]:
        """Obtener items del menú"""
        return self.service.get_menu_items(
            current_user.business_id,
            available_only,
            category_id,
            db
        )
    
    @Post("/items", status_code=status.HTTP_201_CREATED)
    def create_menu_item(
        self,
        item: MenuItemCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_manager)
    ) -> MenuItemResponse:
        """Crear nuevo item del menú"""
        return self.service.create_menu_item(
            item,
            current_user.business_id,
            db
        )
    
    @Put("/items/{item_id}")
    def update_menu_item(
        self,
        item_id: int,
        item_update: MenuItemUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_manager)
    ) -> MenuItemResponse:
        """Actualizar item del menú"""
        return self.service.update_menu_item(
            item_id,
            item_update,
            current_user.business_id,
            db
        )
    
    @Delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_menu_item(
        self,
        item_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_manager)
    ):
        """Eliminar item del menú"""
        self.service.delete_menu_item(
            item_id,
            current_user.business_id,
            db
        )
        return None

