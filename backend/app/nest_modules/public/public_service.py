"""
Servicio público usando PyNest - Lógica de negocio para catálogo público
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .public_repository import PublicRepository


@Injectable
class PublicService:
    """Servicio para lógica de negocio del catálogo público"""
    
    def __init__(self):
        pass
    
    def get_business_info(self, slug: str, db: Session):
        """Obtener información pública del negocio por slug"""
        repo = PublicRepository(db)
        
        business = repo.find_business_by_slug(slug)
        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Negocio no encontrado"
            )
        
        return {
            "id": business.id,
            "business_name": business.business_name,
            "slug": business.slug,
            "phone": business.phone,
            "email": business.email,
            "address": business.address,
            "logo_url": business.logo_url,
            "currency": business.currency,
            "tax_rate": business.tax_rate
        }
    
    def get_catalog(self, slug: str, db: Session):
        """Obtener catálogo completo (menú + productos) de un negocio"""
        repo = PublicRepository(db)
        
        business = repo.find_business_by_slug(slug)
        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Negocio no encontrado"
            )
        
        # Obtener categorías y items del menú
        menu_categories = repo.get_menu_categories(business.id)
        menu_items = repo.get_menu_items(business.id)
        
        # Obtener productos
        products = repo.get_products(business.id)
        
        # Agrupar items de menú por categoría
        menu_by_category = {}
        for category in menu_categories:
            category_items = [
                {
                    "id": item.id,
                    "name": item.name,
                    "description": item.description,
                    "price": float(item.price),
                    "image_url": item.image_url,
                    "category_id": item.category_id
                }
                for item in menu_items if item.category_id == category.id
            ]
            if category_items:  # Solo incluir categorías con items
                menu_by_category[category.name] = category_items
        
        # Formatear productos
        products_list = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.sale_price),
                "image_url": product.image_url,
                "category": product.category.name if product.category else None
            }
            for product in products
        ]
        
        return {
            "business": {
                "id": business.id,
                "name": business.business_name,
                "slug": business.slug,
                "phone": business.phone,
                "address": business.address,
                "logo_url": business.logo_url,
                "currency": business.currency
            },
            "menu": menu_by_category,
            "products": products_list
        }
    
    def get_public_products(self, slug: str, db: Session):
        """Obtener productos del catálogo público"""
        repo = PublicRepository(db)
        
        business = repo.find_business_by_slug(slug)
        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Negocio no encontrado"
            )
        
        products = repo.get_products(business.id)
        
        return [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.sale_price),
                "sale_price": float(product.sale_price),  # Para compatibilidad con frontend
                "image_url": product.image_url,
                "category": product.category.name if product.category else None,
                "stock": product.stock,
                "unit_type": product.unit_type
            }
            for product in products
        ]
    
    def get_public_menu(self, slug: str, db: Session):
        """Obtener menú del catálogo público (array plano de items)"""
        repo = PublicRepository(db)
        
        business = repo.find_business_by_slug(slug)
        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Negocio no encontrado"
            )
        
        menu_items = repo.get_menu_items(business.id)
        
        # Devolver array plano de items
        return [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": float(item.price),
                "image_url": item.image_url,
                "category_id": item.category_id,
                "preparation_time": item.preparation_time,
                "is_featured": item.is_featured,
                "is_available": item.is_available
            }
            for item in menu_items
        ]
    
    def get_menu_categories(self, slug: str, db: Session):
        """Obtener solo las categorías del menú"""
        repo = PublicRepository(db)
        
        business = repo.find_business_by_slug(slug)
        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Negocio no encontrado"
            )
        
        categories = repo.get_menu_categories(business.id)
        
        return [
            {
                "id": category.id,
                "name": category.name,
                "description": category.description
            }
            for category in categories
        ]
    
    def get_menu_item_detail(self, slug: str, item_id: int, db: Session):
        """Obtener detalle completo de un item del menú"""
        repo = PublicRepository(db)
        
        business = repo.find_business_by_slug(slug)
        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Negocio no encontrado"
            )
        
        item = repo.get_menu_item_by_id(item_id, business.id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item de menú no encontrado"
            )
        
        # Obtener ingredientes si existen
        ingredients = []
        if hasattr(item, 'ingredients') and item.ingredients:
            ingredients = [
                {
                    "id": ing.id,
                    "name": ing.name,
                    "quantity": ing.quantity if hasattr(ing, 'quantity') else None
                }
                for ing in item.ingredients
            ]
        
        return {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": float(item.price),
            "image_url": item.image_url,
            "category_id": item.category_id,
            "preparation_time": item.preparation_time,
            "is_featured": item.is_featured,
            "is_available": item.is_available,
            "ingredients": ingredients
        }

