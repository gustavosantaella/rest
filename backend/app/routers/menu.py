from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import delete
from typing import List
from ..database import get_db
from ..models.menu import MenuItem, MenuCategory, menu_item_ingredients
from ..models.product import Product
from ..models.user import User
from ..schemas.menu import (
    MenuItemCreate, MenuItemUpdate, MenuItemResponse, IngredientItem,
    MenuCategoryCreate, MenuCategoryUpdate, MenuCategoryResponse
)
from ..utils.dependencies import get_current_user, get_current_active_manager

router = APIRouter(prefix="/menu", tags=["menu"])


# CATEGORÍAS DEL MENÚ
@router.post("/categories", response_model=MenuCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_menu_category(
    category: MenuCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_manager),
):
    db_category = db.query(MenuCategory).filter(MenuCategory.name == category.name).first()
    if db_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría del menú ya existe",
        )
    
    new_category = MenuCategory(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/categories", response_model=List[MenuCategoryResponse])
def read_menu_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    categories = db.query(MenuCategory).order_by(MenuCategory.display_order).offset(skip).limit(limit).all()
    return categories


@router.put("/categories/{category_id}", response_model=MenuCategoryResponse)
def update_menu_category(
    category_id: int,
    category_update: MenuCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_manager),
):
    category = db.query(MenuCategory).filter(MenuCategory.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )
    
    update_data = category_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    return category


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_manager),
):
    category = db.query(MenuCategory).filter(MenuCategory.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )
    
    db.delete(category)
    db.commit()
    return None


# ITEMS DEL MENÚ (PLATILLOS)
@router.post("/items", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
def create_menu_item(
    menu_item: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_manager),
):
    # Verificar que la categoría existe
    category = db.query(MenuCategory).filter(MenuCategory.id == menu_item.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )
    
    # Crear el item sin ingredientes
    item_data = menu_item.model_dump(exclude={'ingredients'})
    new_item = MenuItem(**item_data)
    db.add(new_item)
    db.flush()  # Para obtener el ID
    
    # Agregar ingredientes
    if menu_item.ingredients:
        for ingredient in menu_item.ingredients:
            # Verificar que el producto existe
            product = db.query(Product).filter(Product.id == ingredient.product_id).first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto con ID {ingredient.product_id} no encontrado",
                )
            
            # Insertar en la tabla de relación
            stmt = menu_item_ingredients.insert().values(
                menu_item_id=new_item.id,
                product_id=ingredient.product_id,
                quantity=ingredient.quantity
            )
            db.execute(stmt)
    
    db.commit()
    db.refresh(new_item)
    
    # Obtener ingredientes con nombres
    return _build_menu_item_response(new_item, db)


@router.get("/items", response_model=List[MenuItemResponse])
def read_menu_items(
    skip: int = 0,
    limit: int = 100,
    category_id: int = None,
    available_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(MenuItem)
    
    if category_id:
        query = query.filter(MenuItem.category_id == category_id)
    
    if available_only:
        query = query.filter(MenuItem.is_available == True)
    
    items = query.offset(skip).limit(limit).all()
    return [_build_menu_item_response(item, db) for item in items]


@router.get("/items/featured", response_model=List[MenuItemResponse])
def read_featured_menu_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = db.query(MenuItem).filter(
        MenuItem.is_featured == True,
        MenuItem.is_available == True
    ).all()
    return [_build_menu_item_response(item, db) for item in items]


@router.get("/items/{item_id}", response_model=MenuItemResponse)
def read_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item del menú no encontrado",
        )
    return _build_menu_item_response(item, db)


@router.put("/items/{item_id}", response_model=MenuItemResponse)
def update_menu_item(
    item_id: int,
    item_update: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_manager),
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item del menú no encontrado",
        )
    
    update_data = item_update.model_dump(exclude_unset=True, exclude={'ingredients'})
    
    for field, value in update_data.items():
        setattr(item, field, value)
    
    # Actualizar ingredientes si se proporcionan
    if item_update.ingredients is not None:
        # Eliminar ingredientes existentes
        db.execute(delete(menu_item_ingredients).where(menu_item_ingredients.c.menu_item_id == item_id))
        
        # Agregar nuevos ingredientes
        for ingredient in item_update.ingredients:
            stmt = menu_item_ingredients.insert().values(
                menu_item_id=item_id,
                product_id=ingredient.product_id,
                quantity=ingredient.quantity
            )
            db.execute(stmt)
    
    db.commit()
    db.refresh(item)
    return _build_menu_item_response(item, db)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_manager),
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item del menú no encontrado",
        )
    
    db.delete(item)
    db.commit()
    return None


# Helper function para construir respuesta con ingredientes
def _build_menu_item_response(item: MenuItem, db: Session) -> MenuItemResponse:
    # Obtener ingredientes con sus cantidades
    ingredients_data = db.execute(
        menu_item_ingredients.select().where(menu_item_ingredients.c.menu_item_id == item.id)
    ).fetchall()
    
    ingredients = []
    for ing_data in ingredients_data:
        product = db.query(Product).filter(Product.id == ing_data.product_id).first()
        if product:
            ingredients.append(IngredientItem(
                product_id=ing_data.product_id,
                quantity=ing_data.quantity,
                product_name=product.name
            ))
    
    return MenuItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        category_id=item.category_id,
        price=item.price,
        preparation_time=item.preparation_time,
        is_available=item.is_available,
        is_featured=item.is_featured,
        image_url=item.image_url,
        created_at=item.created_at,
        updated_at=item.updated_at,
        ingredients=ingredients
    )

