"""
Controlador de productos usando PyNest
"""

from nest.core import Controller, Get, Post, Put, Delete, Depends
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
from .products_service import ProductsService
from ...core.database import get_db
from ...models.user import User
from ...schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    CategoryCreate,
    CategoryResponse,
)
from ...utils.dependencies import get_current_user, get_current_active_manager


@Controller("api/products")
class ProductsController:
    """Controlador para rutas de productos"""

    def __init__(self, products_service: ProductsService):
        self.products_service = products_service

    # Endpoints de categorías
    @Post("/categories", status_code=status.HTTP_201_CREATED)
    def create_category(
        self,
        category: CategoryCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_manager),
    ) -> CategoryResponse:
        """Crear nueva categoría"""
        return self.products_service.create_category(category, current_user.business_id, db)

    @Get("/categories")
    def read_categories(
        self,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> List[CategoryResponse]:
        """Obtener lista de categorías"""
        return self.products_service.get_categories(current_user.business_id, skip, limit, db)

    # Endpoints de productos
    @Post("/", status_code=status.HTTP_201_CREATED)
    def create_product(
        self,
        product: ProductCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_manager),
    ) -> ProductResponse:
        """Crear nuevo producto"""
        return self.products_service.create_product(product, current_user.business_id, db)

    @Get("/")
    def read_products(
        self,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> List[ProductResponse]:
        """Obtener lista de productos"""
        return self.products_service.get_products(current_user.business_id, skip, limit, db)

    @Get("/{product_id}")
    def read_product(
        self,
        product_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> ProductResponse:
        """Obtener producto por ID"""
        return self.products_service.get_product_by_id(product_id, current_user.business_id, db)

    @Put("/{product_id}")
    def update_product(
        self,
        product_id: int,
        product_update: ProductUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_manager),
    ) -> ProductResponse:
        """Actualizar producto"""
        return self.products_service.update_product(product_id, product_update, current_user.business_id, db)

    @Delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_product(
        self,
        product_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_manager),
    ):
        """Eliminar producto (soft delete)"""
        self.products_service.delete_product(product_id, current_user.business_id, db)
        return None
