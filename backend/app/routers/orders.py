from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..models.order import Order, OrderItem, OrderStatus
from ..models.product import Product
from ..models.table import Table, TableStatus
from ..models.user import User
from ..schemas.order import OrderCreate, OrderUpdate, OrderResponse
from ..utils.dependencies import get_current_user, get_current_active_chef

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verificar que la mesa existe y está disponible (si se especifica)
    if order_data.table_id:
        table = db.query(Table).filter(Table.id == order_data.table_id).first()
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mesa no encontrada"
            )
        # Actualizar estado de la mesa
        table.status = TableStatus.OCCUPIED
    
    # Crear la orden
    new_order = Order(
        table_id=order_data.table_id,
        user_id=current_user.id,
        notes=order_data.notes,
        status=OrderStatus.PENDING
    )
    
    subtotal = 0
    
    # Crear items de la orden
    for item_data in order_data.items:
        product = db.query(Product).filter(Product.id == item_data.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {item_data.product_id} no encontrado"
            )
        
        # Verificar stock
        if product.stock < item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para {product.name}"
            )
        
        item_subtotal = product.sale_price * item_data.quantity
        subtotal += item_subtotal
        
        order_item = OrderItem(
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            unit_price=product.sale_price,
            subtotal=item_subtotal,
            notes=item_data.notes
        )
        new_order.items.append(order_item)
        
        # Reducir stock
        product.stock -= item_data.quantity
    
    # Calcular totales (IVA del 16% como ejemplo)
    new_order.subtotal = subtotal
    new_order.tax = subtotal * 0.16
    new_order.total = subtotal + new_order.tax
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    return new_order


@router.get("/", response_model=List[OrderResponse])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_chef)  # Chef puede ver órdenes
):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_chef)  # Chef puede ver órdenes
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada"
        )
    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada"
        )
    
    update_data = order_update.model_dump(exclude_unset=True)
    
    # Si se actualiza el descuento, recalcular total
    if "discount" in update_data:
        order.discount = update_data["discount"]
        order.total = order.subtotal + order.tax - order.discount
    
    # Si se marca como pagada
    if update_data.get("status") == OrderStatus.PAID:
        order.paid_at = datetime.utcnow()
        # Liberar la mesa si tiene una asignada
        if order.table_id:
            table = db.query(Table).filter(Table.id == order.table_id).first()
            if table:
                table.status = TableStatus.AVAILABLE
    
    for field, value in update_data.items():
        if field != "discount":  # Ya manejado arriba
            setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada"
        )
    
    # Liberar mesa si está asignada
    if order.table_id:
        table = db.query(Table).filter(Table.id == order.table_id).first()
        if table:
            table.status = TableStatus.AVAILABLE
    
    db.delete(order)
    db.commit()
    return None

