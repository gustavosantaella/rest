from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..models.order import Order, OrderItem, OrderStatus
from ..models.order_payment import OrderPayment
from ..models.payment_method import PaymentMethod
from ..models.product import Product
from ..models.table import Table, TableStatus
from ..models.user import User
from ..schemas.order import OrderCreate, OrderUpdate, OrderResponse, AddPaymentsToOrder, UpdateOrderItems
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
    
    # Validar y crear pagos (si se especifican)
    total_pagado = 0
    
    if order_data.payments and len(order_data.payments) > 0:
        total_pagado = sum(payment.amount for payment in order_data.payments)
        
        # Solo validar si hay pagos - Validar que la suma de pagos coincida con el total (con margen de error de 0.01)
        if abs(total_pagado - new_order.total) > 0.01:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La suma de los pagos (${total_pagado:.2f}) no coincide con el total de la orden (${new_order.total:.2f})"
            )
    
    # Crear los pagos si existen
    for payment_data in order_data.payments:
        # Verificar que el método de pago existe
        payment_method = db.query(PaymentMethod).filter(
            PaymentMethod.id == payment_data.payment_method_id,
            PaymentMethod.is_active == True
        ).first()
        
        if not payment_method:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Método de pago con ID {payment_data.payment_method_id} no encontrado o inactivo"
            )
        
        order_payment = OrderPayment(
            payment_method_id=payment_data.payment_method_id,
            amount=payment_data.amount,
            reference=payment_data.reference
        )
        new_order.payments.append(order_payment)
    
    # Actualizar payment_status
    if total_pagado >= new_order.total:
        new_order.payment_status = "paid"
        new_order.paid_at = datetime.utcnow()
    elif total_pagado > 0:
        new_order.payment_status = "partial"
    else:
        new_order.payment_status = "pending"
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    # Agregar nombres de métodos de pago a la respuesta
    for payment in new_order.payments:
        payment_method = db.query(PaymentMethod).filter(PaymentMethod.id == payment.payment_method_id).first()
        if payment_method:
            payment.payment_method_name = payment_method.name
    
    return new_order


@router.get("/", response_model=List[OrderResponse])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_chef)  # Chef puede ver órdenes
):
    orders = db.query(Order).offset(skip).limit(limit).all()
    
    # Agregar nombres de métodos de pago
    for order in orders:
        for payment in order.payments:
            payment_method = db.query(PaymentMethod).filter(PaymentMethod.id == payment.payment_method_id).first()
            if payment_method:
                payment.payment_method_name = payment_method.name
    
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
    
    # Agregar nombres de métodos de pago
    for payment in order.payments:
        payment_method = db.query(PaymentMethod).filter(PaymentMethod.id == payment.payment_method_id).first()
        if payment_method:
            payment.payment_method_name = payment_method.name
    
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
    
    # Si se marca como completada y está pagada, liberar la mesa
    if update_data.get("status") == OrderStatus.COMPLETED and order.payment_status == "paid":
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


@router.put("/{order_id}/items", response_model=OrderResponse)
def update_order_items(
    order_id: int,
    items_data: UpdateOrderItems,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar items de una orden existente (agregar/quitar productos)"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada"
        )
    
    # No permitir editar órdenes completadas o canceladas
    if order.status == OrderStatus.COMPLETED or order.status == OrderStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pueden editar órdenes completadas o canceladas"
        )
    
    # Restaurar stock de los items actuales
    for old_item in order.items:
        product = db.query(Product).filter(Product.id == old_item.product_id).first()
        if product:
            product.stock += old_item.quantity
    
    # Eliminar items actuales
    for item in order.items:
        db.delete(item)
    
    # Crear nuevos items
    subtotal = 0
    for item_data in items_data.items:
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
        order.items.append(order_item)
        
        # Reducir stock
        product.stock -= item_data.quantity
    
    # Recalcular totales
    order.subtotal = subtotal
    order.tax = subtotal * 0.16
    order.total = subtotal + order.tax - order.discount
    
    # Recalcular payment_status basado en pagos existentes
    total_pagado = sum(p.amount for p in order.payments)
    if total_pagado >= order.total:
        order.payment_status = "paid"
    elif total_pagado > 0:
        order.payment_status = "partial"
    else:
        order.payment_status = "pending"
    
    db.commit()
    db.refresh(order)
    
    # Agregar nombres de métodos de pago
    for payment in order.payments:
        payment_method = db.query(PaymentMethod).filter(PaymentMethod.id == payment.payment_method_id).first()
        if payment_method:
            payment.payment_method_name = payment_method.name
    
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


@router.post("/{order_id}/payments", response_model=OrderResponse)
def add_payments_to_order(
    order_id: int,
    payment_data: AddPaymentsToOrder,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Agregar pagos a una orden existente"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada"
        )
    
    # Calcular total ya pagado
    existing_payments = sum(p.amount for p in order.payments)
    new_payments_total = sum(p.amount for p in payment_data.payments)
    total_after_payments = existing_payments + new_payments_total
    
    # Validar que no exceda el total
    if total_after_payments > order.total + 0.01:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Los pagos exceden el total de la orden. Ya pagado: ${existing_payments:.2f}, Nuevo: ${new_payments_total:.2f}, Total orden: ${order.total:.2f}"
        )
    
    # Crear los nuevos pagos
    for payment in payment_data.payments:
        # Verificar que el método existe y está activo
        payment_method = db.query(PaymentMethod).filter(
            PaymentMethod.id == payment.payment_method_id,
            PaymentMethod.is_active == True
        ).first()
        
        if not payment_method:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Método de pago con ID {payment.payment_method_id} no encontrado o inactivo"
            )
        
        order_payment = OrderPayment(
            payment_method_id=payment.payment_method_id,
            amount=payment.amount,
            reference=payment.reference
        )
        order.payments.append(order_payment)
    
    # Actualizar payment_status
    if abs(total_after_payments - order.total) <= 0.01:
        order.payment_status = "paid"
        order.paid_at = datetime.utcnow()
        # No cambiar status automáticamente - eso lo maneja el mesero/chef
    elif total_after_payments > 0:
        order.payment_status = "partial"
    
    db.commit()
    db.refresh(order)
    
    # Agregar nombres de métodos de pago
    for payment in order.payments:
        payment_method = db.query(PaymentMethod).filter(PaymentMethod.id == payment.payment_method_id).first()
        if payment_method:
            payment.payment_method_name = payment_method.name
    
    return order

