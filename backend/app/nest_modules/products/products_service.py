"""
Servicio de productos usando PyNest - Solo lógica de negocio
"""

from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from .products_repository import ProductRepository, CategoryRepository
from ...models.product import Product, Category
from ...schemas.product import ProductCreate, ProductUpdate, CategoryCreate


@Injectable
class ProductsService:
    """Servicio para lógica de negocio de productos y categorías"""

    def __init__(self):
        pass

    # Métodos de categorías
    def create_category(
        self, category_data: CategoryCreate, business_id: int, db: Session
    ) -> Category:
        """Crear nueva categoría con validaciones"""
        category_repo = CategoryRepository(db)

        # Validar que no exista una categoría con el mismo nombre en el negocio
        existing = category_repo.find_by_name(category_data.name, business_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La categoría ya existe en tu negocio",
            )

        # Crear categoría
        category_dict = category_data.model_dump()
        category_dict["business_id"] = business_id
        return category_repo.create(category_dict)

    def get_categories(
        self, business_id: int, skip: int, limit: int, db: Session
    ) -> List[Category]:
        """Obtener lista de categorías"""
        category_repo = CategoryRepository(db)
        return category_repo.find_all(business_id, skip, limit)

    # Métodos de productos
    def create_product(
        self, product_data: ProductCreate, business_id: int, db: Session
    ) -> Product:
        """Crear nuevo producto con validaciones"""
        product_repo = ProductRepository(db)
        category_repo = CategoryRepository(db)

        # Verificar que la categoría existe y pertenece al negocio
        category = category_repo.find_by_id(product_data.category_id, business_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada en tu negocio",
            )

        # Crear producto
        product_dict = product_data.model_dump()
        product_dict["business_id"] = business_id
        return product_repo.create(product_dict)

    def get_products(
        self, business_id: int, skip: int, limit: int, db: Session
    ) -> List[Product]:
        """Obtener lista de productos"""
        product_repo = ProductRepository(db)
        return product_repo.find_all(business_id, skip, limit)

    def get_product_by_id(
        self, product_id: int, business_id: int, db: Session
    ) -> Product:
        """Obtener producto por ID con validación"""
        product_repo = ProductRepository(db)
        product = product_repo.find_by_id(product_id, business_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )

        return product

    def update_product(
        self,
        product_id: int,
        product_update: ProductUpdate,
        business_id: int,
        db: Session,
    ) -> Product:
        """Actualizar producto con validaciones"""
        product_repo = ProductRepository(db)

        # Validar que el producto existe
        product = product_repo.find_by_id(product_id, business_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )

        # Actualizar
        update_data = product_update.model_dump(exclude_unset=True)
        return product_repo.update(product, update_data)

    def delete_product(self, product_id: int, business_id: int, db: Session) -> None:
        """Eliminar producto (soft delete) con validaciones"""
        product_repo = ProductRepository(db)

        # Validar que el producto existe
        product = product_repo.find_by_id(product_id, business_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )

        # Eliminar
        product_repo.soft_delete(product)
