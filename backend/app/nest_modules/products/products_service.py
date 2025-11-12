"""
Servicio de productos usando PyNest
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from ...models.product import Product, Category
from ...schemas.product import ProductCreate, ProductUpdate, CategoryCreate


@Injectable
class ProductsService:
    """Servicio para manejo de productos y categorías"""
    
    def __init__(self):
        pass
    
    # Métodos de categorías
    def create_category(self, category_data: CategoryCreate, business_id: int, db: Session) -> Category:
        """Crear nueva categoría"""
        existing = db.query(Category).filter(
            Category.name == category_data.name,
            Category.business_id == business_id,
            Category.deleted_at.is_(None)
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La categoría ya existe en tu negocio"
            )
        
        category_dict = category_data.model_dump()
        category_dict['business_id'] = business_id
        new_category = Category(**category_dict)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    
    def get_categories(self, business_id: int, skip: int, limit: int, db: Session) -> List[Category]:
        """Obtener lista de categorías"""
        return db.query(Category).filter(
            Category.business_id == business_id,
            Category.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    
    # Métodos de productos
    def create_product(self, product_data: ProductCreate, business_id: int, db: Session) -> Product:
        """Crear nuevo producto"""
        # Verificar que la categoría existe y pertenece al negocio
        category = db.query(Category).filter(
            Category.id == product_data.category_id,
            Category.business_id == business_id,
            Category.deleted_at.is_(None)
        ).first()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada en tu negocio"
            )
        
        product_dict = product_data.model_dump()
        product_dict['business_id'] = business_id
        new_product = Product(**product_dict)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    
    def get_products(self, business_id: int, skip: int, limit: int, db: Session) -> List[Product]:
        """Obtener lista de productos"""
        return db.query(Product).filter(
            Product.business_id == business_id,
            Product.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    
    def get_product_by_id(self, product_id: int, business_id: int, db: Session) -> Product:
        """Obtener producto por ID"""
        product = db.query(Product).filter(
            Product.id == product_id,
            Product.business_id == business_id,
            Product.deleted_at.is_(None)
        ).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        
        return product
    
    def update_product(
        self,
        product_id: int,
        product_update: ProductUpdate,
        business_id: int,
        db: Session
    ) -> Product:
        """Actualizar producto"""
        product = self.get_product_by_id(product_id, business_id, db)
        
        update_data = product_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        return product
    
    def delete_product(self, product_id: int, business_id: int, db: Session) -> None:
        """Eliminar producto (soft delete)"""
        from datetime import datetime
        
        product = self.get_product_by_id(product_id, business_id, db)
        product.deleted_at = datetime.now()
        db.commit()

