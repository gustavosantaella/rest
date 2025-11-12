"""
Repositorio de productos - Operaciones de base de datos
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ...models.product import Product, Category


class CategoryRepository:
    """Repositorio para operaciones de BD de categorías"""

    def __init__(self, db: Session):
        self.db = db

    def find_by_name(self, name: str, business_id: int) -> Optional[Category]:
        """Buscar categoría por nombre en un negocio"""
        return (
            self.db.query(Category)
            .filter(
                Category.name == name,
                Category.business_id == business_id,
                Category.deleted_at.is_(None),
            )
            .first()
        )

    def find_by_id(self, category_id: int, business_id: int) -> Optional[Category]:
        """Buscar categoría por ID en un negocio"""
        return (
            self.db.query(Category)
            .filter(
                Category.id == category_id,
                Category.business_id == business_id,
                Category.deleted_at.is_(None),
            )
            .first()
        )

    def find_all(
        self, business_id: int, skip: int = 0, limit: int = 100
    ) -> List[Category]:
        """Obtener todas las categorías de un negocio"""
        return (
            self.db.query(Category)
            .filter(Category.business_id == business_id, Category.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, category_data: dict) -> Category:
        """Crear nueva categoría"""
        category = Category(**category_data)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category


class ProductRepository:
    """Repositorio para operaciones de BD de productos"""

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, product_id: int, business_id: int) -> Optional[Product]:
        """Buscar producto por ID en un negocio"""
        return (
            self.db.query(Product)
            .filter(
                Product.id == product_id,
                Product.business_id == business_id,
                Product.deleted_at.is_(None),
            )
            .first()
        )

    def find_all(
        self, business_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """Obtener todos los productos de un negocio"""
        return (
            self.db.query(Product)
            .filter(Product.business_id == business_id, Product.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, product_data: dict) -> Product:
        """Crear nuevo producto"""
        product = Product(**product_data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product, update_data: dict) -> Product:
        """Actualizar producto existente"""
        for field, value in update_data.items():
            setattr(product, field, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def soft_delete(self, product: Product) -> None:
        """Eliminar producto (soft delete)"""
        product.deleted_at = datetime.now()
        self.db.commit()
