"""
Servicio de órdenes usando PyNest - Lógica de negocio
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from .orders_repository import (
    OrderRepository, OrderItemRepository, PaymentRepository,
    TableRepository, ProductRepository, MenuItemRepository
)
from ...models.order import OrderStatus
from ...models.table import TableStatus
from ...schemas.order import OrderCreate, OrderUpdate, AddPaymentsToOrder, UpdateOrderItems


@Injectable
class OrdersService:
    """Servicio para lógica de negocio de órdenes"""
    
    def __init__(self):
        pass
    
    def create_order(self, order_data: OrderCreate, user_id: int, business_id: int, db: Session):
        """Crear nueva orden con validaciones"""
        order_repo = OrderRepository(db)
        item_repo = OrderItemRepository(db)
        table_repo = TableRepository(db)
        
        # Verificar y actualizar mesa si se especifica
        if order_data.table_id:
            table = table_repo.find_by_id(order_data.table_id, business_id)
            if not table:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Mesa no encontrada"
                )
            table_repo.update_status(table, TableStatus.OCCUPIED)
        
        # Procesar items y calcular subtotal
        subtotal = 0
        items_to_create = []
        
        for item_data in order_data.items:
            item_subtotal, item_dict = self._process_order_item(item_data, business_id, db)
            subtotal += item_subtotal
            items_to_create.append(item_dict)
        
        # Calcular totales
        tax = subtotal * 0.16
        total = subtotal + tax
        
        # Crear la orden
        order = order_repo.create({
            'business_id': business_id,
            'table_id': order_data.table_id,
            'user_id': user_id,
            'notes': order_data.notes,
            'status': OrderStatus.PENDING.value,
            'subtotal': subtotal,
            'tax': tax,
            'total': total,
            'discount': 0,
            'payment_status': 'pending'
        })
        
        # Crear items
        for item_dict in items_to_create:
            item_dict['order_id'] = order.id
            item_repo.create(item_dict)
        
        # Procesar pagos si existen
        total_pagado = 0
        if order_data.payments and len(order_data.payments) > 0:
            total_pagado = self._add_payments(order, order_data.payments, business_id, db)
        
        # Actualizar estado de pago
        self._update_payment_status(order, total_pagado)
        
        order_repo.commit()
        order_repo.refresh(order)
        
        # Agregar nombres de métodos de pago
        self._enrich_with_payment_names(order, db)
        
        return order
    
    def _process_order_item(self, item_data, business_id: int, db: Session):
        """Procesar un item de orden (producto o menu item)"""
        if item_data.source_type == "menu" and item_data.menu_item_id:
            return self._process_menu_item(item_data, business_id, db)
        else:
            return self._process_product_item(item_data, business_id, db)
    
    def _process_menu_item(self, item_data, business_id: int, db: Session):
        """Procesar item del menú"""
        menu_item_repo = MenuItemRepository(db)
        product_repo = ProductRepository(db)
        
        menu_item = menu_item_repo.find_by_id(item_data.menu_item_id, business_id)
        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item de menú con ID {item_data.menu_item_id} no encontrado"
            )
        
        if not menu_item.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El item '{menu_item.name}' no está disponible"
            )
        
        # Verificar y reducir stock de ingredientes
        for ingredient in menu_item.ingredients:
            ingredient_qty = menu_item_repo.get_ingredient_quantity(menu_item.id, ingredient.id)
            required_qty = ingredient_qty * item_data.quantity
            
            if ingredient.stock < required_qty:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente del ingrediente '{ingredient.name}'"
                )
        
        # Reducir stock
        for ingredient in menu_item.ingredients:
            ingredient_qty = menu_item_repo.get_ingredient_quantity(menu_item.id, ingredient.id)
            product_repo.update_stock(ingredient, -ingredient_qty * item_data.quantity)
        
        item_subtotal = menu_item.price * item_data.quantity
        
        return item_subtotal, {
            'menu_item_id': item_data.menu_item_id,
            'source_type': 'menu',
            'quantity': item_data.quantity,
            'unit_price': menu_item.price,
            'subtotal': item_subtotal,
            'notes': item_data.notes
        }
    
    def _process_product_item(self, item_data, business_id: int, db: Session):
        """Procesar producto directo"""
        product_repo = ProductRepository(db)
        
        if not item_data.product_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe proporcionar product_id o menu_item_id"
            )
        
        product = product_repo.find_by_id(item_data.product_id, business_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {item_data.product_id} no encontrado"
            )
        
        if product.stock < item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para {product.name}"
            )
        
        # Reducir stock
        product_repo.update_stock(product, -item_data.quantity)
        
        item_subtotal = product.sale_price * item_data.quantity
        
        return item_subtotal, {
            'product_id': item_data.product_id,
            'source_type': 'product',
            'quantity': item_data.quantity,
            'unit_price': product.sale_price,
            'subtotal': item_subtotal,
            'notes': item_data.notes
        }
    
    def _add_payments(self, order, payments, business_id: int, db: Session):
        """Agregar pagos a la orden"""
        payment_repo = PaymentRepository(db)
        total_pagado = sum(payment.amount for payment in payments)
        
        # Validar que coincida con el total (con margen de error)
        if abs(total_pagado - order.total) > 0.01:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La suma de los pagos (${total_pagado:.2f}) no coincide con el total (${order.total:.2f})"
            )
        
        for payment_data in payments:
            payment_method = payment_repo.find_payment_method_by_id(
                payment_data.payment_method_id, business_id
            )
            if not payment_method:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Método de pago con ID {payment_data.payment_method_id} no encontrado"
                )
            
            payment = payment_repo.create_order_payment({
                'order_id': order.id,
                'payment_method_id': payment_data.payment_method_id,
                'amount': payment_data.amount,
                'reference': payment_data.reference
            })
            order.payments.append(payment)
        
        return total_pagado
    
    def _update_payment_status(self, order, total_pagado):
        """Actualizar estado de pago"""
        if total_pagado >= order.total:
            order.payment_status = 'paid'
            order.paid_at = datetime.utcnow()
        elif total_pagado > 0:
            order.payment_status = 'partial'
        else:
            order.payment_status = 'pending'
    
    def _enrich_with_payment_names(self, order, db: Session):
        """Agregar nombres de métodos de pago"""
        payment_repo = PaymentRepository(db)
        for payment in order.payments:
            payment.payment_method_name = payment_repo.get_payment_method_name(
                payment.payment_method_id
            )
    
    def get_orders(self, business_id: int, skip: int, limit: int, db: Session):
        """Obtener lista de órdenes"""
        order_repo = OrderRepository(db)
        orders = order_repo.find_all(business_id, skip, limit)
        
        for order in orders:
            self._enrich_with_payment_names(order, db)
        
        return orders
    
    def get_order_by_id(self, order_id: int, business_id: int, db: Session):
        """Obtener orden por ID"""
        order_repo = OrderRepository(db)
        order = order_repo.find_by_id(order_id, business_id)
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orden no encontrada"
            )
        
        self._enrich_with_payment_names(order, db)
        return order
    
    def get_order_by_table(self, table_id: int, business_id: int, db: Session):
        """Obtener orden activa de una mesa"""
        order_repo = OrderRepository(db)
        order = order_repo.find_by_table_id(table_id, business_id)
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay orden activa para esta mesa"
            )
        
        self._enrich_with_payment_names(order, db)
        return order
    
    def update_order(self, order_id: int, order_update: OrderUpdate, business_id: int, db: Session):
        """Actualizar orden"""
        order_repo = OrderRepository(db)
        table_repo = TableRepository(db)
        
        order = order_repo.find_by_id(order_id, business_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orden no encontrada"
            )
        
        update_data = order_update.model_dump(exclude_unset=True)
        
        # Manejar descuento
        if 'discount' in update_data:
            order.discount = update_data['discount']
            order.total = order.subtotal + order.tax - order.discount
        
        # Liberar mesa si se completa
        if (update_data.get('status') == OrderStatus.COMPLETED.value 
            and order.payment_status == 'paid' and order.table_id):
            table = table_repo.find_by_id(order.table_id, business_id)
            if table:
                table_repo.update_status(table, TableStatus.AVAILABLE)
            order.paid_at = datetime.utcnow()
        
        for field, value in update_data.items():
            if field != 'discount':
                setattr(order, field, value)
        
        order_repo.commit()
        order_repo.refresh(order)
        return order
    
    def add_payments_to_order(
        self,
        order_id: int,
        payment_data: AddPaymentsToOrder,
        business_id: int,
        db: Session
    ):
        """Agregar pagos a una orden existente"""
        order_repo = OrderRepository(db)
        payment_repo = PaymentRepository(db)
        
        order = order_repo.find_by_id(order_id, business_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orden no encontrada"
            )
        
        existing_payments = sum(p.amount for p in order.payments)
        new_payments_total = sum(p.amount for p in payment_data.payments)
        total_after_payments = existing_payments + new_payments_total
        
        if total_after_payments > order.total + 0.01:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Los pagos exceden el total. Ya pagado: ${existing_payments:.2f}, Nuevo: ${new_payments_total:.2f}, Total: ${order.total:.2f}"
            )
        
        # Crear nuevos pagos
        for payment in payment_data.payments:
            payment_method = payment_repo.find_payment_method_by_id(
                payment.payment_method_id, business_id
            )
            if not payment_method:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Método de pago con ID {payment.payment_method_id} no encontrado"
                )
            
            order_payment = payment_repo.create_order_payment({
                'order_id': order.id,
                'payment_method_id': payment.payment_method_id,
                'amount': payment.amount,
                'reference': payment.reference
            })
            order.payments.append(order_payment)
        
        # Actualizar estado de pago
        if abs(total_after_payments - order.total) <= 0.01:
            order.payment_status = 'paid'
            order.paid_at = datetime.utcnow()
        elif total_after_payments > 0:
            order.payment_status = 'partial'
        
        order_repo.commit()
        order_repo.refresh(order)
        self._enrich_with_payment_names(order, db)
        
        return order
    
    def delete_order(self, order_id: int, business_id: int, db: Session):
        """Eliminar orden"""
        order_repo = OrderRepository(db)
        table_repo = TableRepository(db)
        
        order = order_repo.find_by_id(order_id, business_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orden no encontrada"
            )
        
        # Liberar mesa si está asignada
        if order.table_id:
            table = table_repo.find_by_id(order.table_id, business_id)
            if table:
                table_repo.update_status(table, TableStatus.AVAILABLE)
        
        order_repo.delete(order)

