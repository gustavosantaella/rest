"""
Servicio de menú usando PyNest - Lógica de negocio
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from .menu_repository import MenuItemRepository, MenuCategoryRepository
from ...schemas.menu import MenuCategoryCreate, MenuCategoryUpdate, MenuItemCreate, MenuItemUpdate


@Injectable
class MenuService:
    """Servicio para lógica de negocio del menú"""
    
    def __init__(self):
        pass
    
    # Categorías del menú
    def get_menu_categories(self, business_id: int, db: Session):
        """Obtener categorías del menú"""
        repo = MenuCategoryRepository(db)
        return repo.find_all(business_id)
    
    def create_menu_category(self, category_data: MenuCategoryCreate, business_id: int, db: Session):
        """Crear nueva categoría del menú"""
        repo = MenuCategoryRepository(db)
        
        # Validar que no exista una categoría con el mismo nombre
        existing = repo.find_by_name(category_data.name, business_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una categoría con ese nombre"
            )
        
        category_dict = category_data.model_dump()
        category_dict['business_id'] = business_id
        return repo.create(category_dict)
    
    def update_menu_category(
        self,
        category_id: int,
        category_update: MenuCategoryUpdate,
        business_id: int,
        db: Session
    ):
        """Actualizar categoría del menú"""
        repo = MenuCategoryRepository(db)
        
        category = repo.find_by_id(category_id, business_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )
        
        update_data = category_update.model_dump(exclude_unset=True)
        return repo.update(category, update_data)
    
    def delete_menu_category(self, category_id: int, business_id: int, db: Session):
        """Eliminar categoría del menú"""
        repo = MenuCategoryRepository(db)
        
        category = repo.find_by_id(category_id, business_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )
        
        repo.soft_delete(category)
    
    # Items del menú
    def get_menu_items(
        self,
        business_id: int,
        available_only: bool,
        category_id: Optional[int],
        db: Session
    ):
        """Obtener items del menú"""
        repo = MenuItemRepository(db)
        items = repo.find_all(business_id, available_only, category_id)
        
        # Formatear cada item para incluir ingredientes correctamente
        return [self._format_menu_item_response(item, db) for item in items]
    
    def create_menu_item(self, item_data: MenuItemCreate, business_id: int, db: Session):
        """Crear nuevo item del menú"""
        repo = MenuItemRepository(db)
        
        # Separar ingredientes del resto de datos
        item_dict = item_data.model_dump(exclude={'ingredients'})
        item_dict['business_id'] = business_id
        ingredients_data = item_data.ingredients
        
        # Crear el item sin ingredientes primero
        menu_item = repo.create(item_dict)
        
        # Agregar ingredientes si existen
        if ingredients_data:
            repo.add_ingredients(menu_item.id, ingredients_data)
        
        # Recargar el item con los ingredientes
        db.refresh(menu_item)
        
        # Formatear la respuesta para incluir ingredientes correctamente
        return self._format_menu_item_response(menu_item, db)
    
    def update_menu_item(
        self,
        item_id: int,
        item_update: MenuItemUpdate,
        business_id: int,
        db: Session
    ):
        """Actualizar item del menú"""
        repo = MenuItemRepository(db)
        
        item = repo.find_by_id(item_id, business_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item del menú no encontrado"
            )
        
        # Separar ingredientes del resto de datos
        update_data = item_update.model_dump(exclude_unset=True, exclude={'ingredients'})
        
        # Actualizar ingredientes si se proporcionan
        if item_update.ingredients is not None:
            repo.update_ingredients(item_id, item_update.ingredients)
        
        updated_item = repo.update(item, update_data)
        
        # Formatear la respuesta
        return self._format_menu_item_response(updated_item, db)
    
    def _format_menu_item_response(self, menu_item, db: Session):
        """Formatear respuesta del menu item con ingredientes correctos"""
        from sqlalchemy import select
        from ...models.menu import menu_item_ingredients
        
        # Obtener ingredientes con sus cantidades desde la tabla intermedia
        stmt = select(
            menu_item_ingredients.c.product_id,
            menu_item_ingredients.c.quantity
        ).where(menu_item_ingredients.c.menu_item_id == menu_item.id)
        
        ingredients_result = db.execute(stmt).all()
        
        # Formatear ingredientes
        formatted_ingredients = [
            {
                'product_id': ing[0],
                'quantity': ing[1],
                'product_name': None  # Se podría cargar si es necesario
            }
            for ing in ingredients_result
        ]
        
        # Crear diccionario de respuesta
        response_dict = {
            'id': menu_item.id,
            'business_id': menu_item.business_id,
            'name': menu_item.name,
            'description': menu_item.description,
            'category_id': menu_item.category_id,
            'price': menu_item.price,
            'preparation_time': menu_item.preparation_time,
            'is_available': menu_item.is_available,
            'is_featured': menu_item.is_featured,
            'image_url': menu_item.image_url,
            'created_at': menu_item.created_at,
            'updated_at': menu_item.updated_at,
            'ingredients': formatted_ingredients
        }
        
        return response_dict
    
    def delete_menu_item(self, item_id: int, business_id: int, db: Session):
        """Eliminar item del menú"""
        repo = MenuItemRepository(db)
        
        item = repo.find_by_id(item_id, business_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item del menú no encontrado"
            )
        
        repo.soft_delete(item)

