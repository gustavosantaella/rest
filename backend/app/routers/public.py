from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from ..database import get_db
from ..models.configuration import BusinessConfiguration
from ..models.product import Product
from ..models.menu import MenuItem, MenuCategory, menu_item_ingredients
from ..schemas.configuration import BusinessConfigurationResponse
from ..schemas.product import ProductResponse
from ..schemas.menu import MenuItemPublicResponse, MenuCategoryResponse

router = APIRouter(prefix="/public", tags=["Public"])

@router.get("/{slug}/info")
def get_business_info(slug: str, db: Session = Depends(get_db)):
    """
    Obtiene la información pública del negocio por su slug.
    No requiere autenticación.
    """
    business = db.query(BusinessConfiguration).filter(
        BusinessConfiguration.slug == slug
    ).first()
    
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    
    return {
        "business_name": business.business_name,
        "slug": business.slug,
        "phone": business.phone,
        "email": business.email,
        "address": business.address,
        "logo_url": business.logo_url,
        "currency": business.currency
    }

@router.get("/{slug}/products", response_model=List[ProductResponse])
def get_public_products(slug: str, db: Session = Depends(get_db)):
    """
    Obtiene los productos visibles en el catálogo del negocio.
    No requiere autenticación.
    """
    # Verificar que el negocio existe
    business = db.query(BusinessConfiguration).filter(
        BusinessConfiguration.slug == slug
    ).first()
    
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    
    # Obtener productos con show_in_catalog = True y stock > 0
    products = db.query(Product).filter(
        Product.show_in_catalog == True,
        Product.stock > 0
    ).all()
    
    return products

@router.get("/{slug}/menu", response_model=List[MenuItemPublicResponse])
def get_public_menu(slug: str, db: Session = Depends(get_db)):
    """
    Obtiene el menú público del negocio.
    No requiere autenticación.
    """
    # Verificar que el negocio existe
    business = db.query(BusinessConfiguration).filter(
        BusinessConfiguration.slug == slug
    ).first()
    
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    
    # Obtener items de menú disponibles
    menu_items = db.query(MenuItem).filter(
        MenuItem.is_available == True
    ).all()
    
    return menu_items

@router.get("/{slug}/menu/{item_id}")
def get_public_menu_item_detail(slug: str, item_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el detalle completo de un item del menú incluyendo ingredientes.
    No requiere autenticación.
    """
    # Verificar que el negocio existe
    business = db.query(BusinessConfiguration).filter(
        BusinessConfiguration.slug == slug
    ).first()
    
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    
    # Obtener el item del menú
    menu_item = db.query(MenuItem).filter(
        MenuItem.id == item_id,
        MenuItem.is_available == True
    ).first()
    
    if not menu_item:
        raise HTTPException(status_code=404, detail="Platillo no encontrado")
    
    # Obtener ingredientes con detalles
    ingredients_data = []
    for product in menu_item.ingredients:
        # Obtener la cantidad del ingrediente desde la tabla de relación usando SQLAlchemy
        stmt = select(menu_item_ingredients.c.quantity).where(
            menu_item_ingredients.c.menu_item_id == menu_item.id,
            menu_item_ingredients.c.product_id == product.id
        )
        result = db.execute(stmt).fetchone()
        
        quantity = result[0] if result else 0
        
        ingredients_data.append({
            "product_id": product.id,
            "product_name": product.name,
            "quantity": quantity,
            "unit_type": product.unit_type
        })
    
    return {
        "id": menu_item.id,
        "name": menu_item.name,
        "description": menu_item.description,
        "category_id": menu_item.category_id,
        "price": menu_item.price,
        "preparation_time": menu_item.preparation_time,
        "is_available": menu_item.is_available,
        "is_featured": menu_item.is_featured,
        "image_url": menu_item.image_url,
        "ingredients": ingredients_data
    }

@router.get("/{slug}/menu-categories", response_model=List[MenuCategoryResponse])
def get_public_menu_categories(slug: str, db: Session = Depends(get_db)):
    """
    Obtiene las categorías del menú público.
    No requiere autenticación.
    """
    # Verificar que el negocio existe
    business = db.query(BusinessConfiguration).filter(
        BusinessConfiguration.slug == slug
    ).first()
    
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    
    # Obtener categorías activas con items disponibles
    categories = db.query(MenuCategory).filter(
        MenuCategory.is_active == True
    ).order_by(MenuCategory.display_order).all()
    
    return categories

