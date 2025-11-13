"""
Repositorio de menú - Operaciones de base de datos
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ...models.menu import MenuItem, MenuCategory


class MenuCategoryRepository:
    """Repositorio para operaciones de BD de categorías del menú"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self, business_id: int) -> List[MenuCategory]:
        """Obtener todas las categorías del menú de un negocio"""
        return self.db.query(MenuCategory).filter(
            MenuCategory.business_id == business_id,
            MenuCategory.deleted_at.is_(None),
            MenuCategory.is_active == True
        ).order_by(MenuCategory.display_order).all()
    
    def find_by_id(self, category_id: int, business_id: int) -> Optional[MenuCategory]:
        """Buscar categoría del menú por ID"""
        return self.db.query(MenuCategory).filter(
            MenuCategory.id == category_id,
            MenuCategory.business_id == business_id,
            MenuCategory.deleted_at.is_(None)
        ).first()
    
    def find_by_name(self, name: str, business_id: int) -> Optional[MenuCategory]:
        """Buscar categoría por nombre"""
        return self.db.query(MenuCategory).filter(
            MenuCategory.name == name,
            MenuCategory.business_id == business_id,
            MenuCategory.deleted_at.is_(None)
        ).first()
    
    def create(self, category_data: dict) -> MenuCategory:
        """Crear nueva categoría del menú"""
        category = MenuCategory(**category_data)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def update(self, category: MenuCategory, update_data: dict) -> MenuCategory:
        """Actualizar categoría del menú"""
        for field, value in update_data.items():
            setattr(category, field, value)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def soft_delete(self, category: MenuCategory) -> None:
        """Eliminar categoría del menú (soft delete)"""
        category.deleted_at = datetime.now()
        self.db.commit()


class MenuItemRepository:
    """Repositorio para operaciones de BD de items del menú"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(
        self,
        business_id: int,
        available_only: bool = False,
        category_id: Optional[int] = None
    ) -> List[MenuItem]:
        """Obtener items del menú de un negocio"""
        query = self.db.query(MenuItem).filter(
            MenuItem.business_id == business_id,
            MenuItem.deleted_at.is_(None)
        )
        
        if available_only:
            query = query.filter(MenuItem.is_available == True)
        
        if category_id:
            query = query.filter(MenuItem.category_id == category_id)
        
        return query.all()
    
    def find_by_id(self, item_id: int, business_id: int) -> Optional[MenuItem]:
        """Buscar item del menú por ID"""
        return self.db.query(MenuItem).filter(
            MenuItem.id == item_id,
            MenuItem.business_id == business_id,
            MenuItem.deleted_at.is_(None)
        ).first()
    
    def create(self, item_data: dict) -> MenuItem:
        """Crear nuevo item del menú (sin ingredientes)"""
        item = MenuItem(**item_data)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def add_ingredients(self, menu_item_id: int, ingredients: List):
        """Agregar ingredientes a un item del menú"""
        from sqlalchemy import insert
        from ...models.menu import menu_item_ingredients
        
        # Eliminar ingredientes existentes
        self.db.execute(
            menu_item_ingredients.delete().where(
                menu_item_ingredients.c.menu_item_id == menu_item_id
            )
        )
        
        # Insertar nuevos ingredientes
        for ingredient in ingredients:
            self.db.execute(
                insert(menu_item_ingredients).values(
                    menu_item_id=menu_item_id,
                    product_id=ingredient.product_id if hasattr(ingredient, 'product_id') else ingredient['product_id'],
                    quantity=ingredient.quantity if hasattr(ingredient, 'quantity') else ingredient['quantity']
                )
            )
        
        self.db.commit()
    
    def update_ingredients(self, menu_item_id: int, ingredients: List):
        """Actualizar ingredientes de un item del menú"""
        self.add_ingredients(menu_item_id, ingredients)
    
    def update(self, item: MenuItem, update_data: dict) -> MenuItem:
        """Actualizar item del menú"""
        for field, value in update_data.items():
            setattr(item, field, value)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def soft_delete(self, item: MenuItem) -> None:
        """Eliminar item del menú (soft delete)"""
        item.deleted_at = datetime.now()
        self.db.commit()

