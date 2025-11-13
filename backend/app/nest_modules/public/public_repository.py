"""
Repositorio público - Operaciones de base de datos para catálogo público
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from ...models.configuration import BusinessConfiguration
from ...models.menu import MenuItem, MenuCategory
from ...models.product import Product


class PublicRepository:
    """Repositorio para operaciones de BD públicas (sin autenticación)"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_business_by_slug(self, slug: str) -> Optional[BusinessConfiguration]:
        """Buscar negocio por slug"""
        return self.db.query(BusinessConfiguration).filter(
            BusinessConfiguration.slug == slug
        ).first()
    
    def get_menu_categories(self, business_id: int) -> List[MenuCategory]:
        """Obtener categorías del menú de un negocio"""
        return self.db.query(MenuCategory).filter(
            MenuCategory.business_id == business_id,
            MenuCategory.deleted_at.is_(None)
        ).order_by(MenuCategory.name).all()
    
    def get_menu_items(self, business_id: int) -> List[MenuItem]:
        """Obtener items del menú de un negocio"""
        return self.db.query(MenuItem).filter(
            MenuItem.business_id == business_id,
            MenuItem.is_available == True,
            MenuItem.deleted_at.is_(None)
        ).order_by(MenuItem.name).all()
    
    def get_products(self, business_id: int) -> List[Product]:
        """Obtener productos de un negocio (para catálogo)"""
        return self.db.query(Product).filter(
            Product.business_id == business_id,
            Product.show_in_catalog == True,
            Product.deleted_at.is_(None)
        ).order_by(Product.name).all()
    
    def get_menu_item_by_id(self, item_id: int, business_id: int) -> Optional[MenuItem]:
        """Obtener detalle de un item del menú"""
        return self.db.query(MenuItem).filter(
            MenuItem.id == item_id,
            MenuItem.business_id == business_id,
            MenuItem.deleted_at.is_(None)
        ).first()

