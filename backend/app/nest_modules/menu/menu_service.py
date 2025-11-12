"""
Servicio de menú usando PyNest - Lógica de negocio
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List, Optional
from .menu_repository import MenuItemRepository, MenuCategoryRepository


@Injectable
class MenuService:
    """Servicio para lógica de negocio del menú"""
    
    def __init__(self):
        pass
    
    def get_menu_categories(self, business_id: int, db: Session):
        """Obtener categorías del menú"""
        repo = MenuCategoryRepository(db)
        return repo.find_all(business_id)
    
    def get_menu_items(
        self,
        business_id: int,
        available_only: bool,
        category_id: Optional[int],
        db: Session
    ):
        """Obtener items del menú"""
        repo = MenuItemRepository(db)
        return repo.find_all(business_id, available_only, category_id)

