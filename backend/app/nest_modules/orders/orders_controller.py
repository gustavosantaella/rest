"""
Controlador de órdenes usando PyNest
"""
from nest.core import Controller, Get, Post, Put, Delete, Depends
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
from .orders_service import OrdersService
from ...core.database import get_db
from ...models.user import User
from ...schemas.order import (
    OrderCreate, OrderUpdate, OrderResponse,
    AddPaymentsToOrder, UpdateOrderItems
)
from ...utils.dependencies import get_current_user, get_current_active_chef


@Controller("api/orders")
class OrdersController:
    """Controlador para rutas de órdenes"""
    
    def __init__(self, orders_service: OrdersService):
        self.orders_service = orders_service
    
    @Post("/", status_code=status.HTTP_201_CREATED)
    def create_order(
        self,
        order_data: OrderCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> OrderResponse:
        """Crear nueva orden"""
        return self.orders_service.create_order(
            order_data,
            current_user.id,
            current_user.business_id,
            db
        )
    
    @Get("/")
    def read_orders(
        self,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_chef)
    ) -> List[OrderResponse]:
        """Obtener lista de órdenes"""
        return self.orders_service.get_orders(
            current_user.business_id,
            skip,
            limit,
            db
        )
    
    @Get("/table/{table_id}")
    def get_order_by_table(
        self,
        table_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> OrderResponse:
        """Obtener la orden activa de una mesa específica"""
        return self.orders_service.get_order_by_table(
            table_id,
            current_user.business_id,
            db
        )
    
    @Get("/{order_id}")
    def read_order(
        self,
        order_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_chef)
    ) -> OrderResponse:
        """Obtener orden por ID"""
        return self.orders_service.get_order_by_id(
            order_id,
            current_user.business_id,
            db
        )
    
    @Put("/{order_id}")
    def update_order(
        self,
        order_id: int,
        order_update: OrderUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> OrderResponse:
        """Actualizar orden"""
        return self.orders_service.update_order(
            order_id,
            order_update,
            current_user.business_id,
            db
        )
    
    @Post("/{order_id}/payments")
    def add_payments_to_order(
        self,
        order_id: int,
        payment_data: AddPaymentsToOrder,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> OrderResponse:
        """Agregar pagos a una orden existente"""
        return self.orders_service.add_payments_to_order(
            order_id,
            payment_data,
            current_user.business_id,
            db
        )
    
    @Delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_order(
        self,
        order_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Eliminar orden"""
        self.orders_service.delete_order(
            order_id,
            current_user.business_id,
            db
        )
        return None

