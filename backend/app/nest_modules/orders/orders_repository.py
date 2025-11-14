"""
Repositorio de órdenes - Operaciones de base de datos
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime
from ...models.order import Order, OrderItem, OrderStatus
from ...models.order_payment import OrderPayment
from ...models.payment_method import PaymentMethod
from ...models.product import Product
from ...models.menu import MenuItem, menu_item_ingredients
from ...models.table import Table, TableStatus
from ...models.customer import Customer


class OrderRepository:
    """Repositorio para operaciones de BD de órdenes"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, order_id: int, business_id: int) -> Optional[Order]:
        """Buscar orden por ID en un negocio"""
        from sqlalchemy.orm import joinedload
        return self.db.query(Order).options(
            joinedload(Order.customer)
        ).filter(
            Order.id == order_id,
            Order.business_id == business_id
        ).first()
    
    def find_by_table_id(self, table_id: int, business_id: int) -> Optional[Order]:
        """Buscar orden activa por ID de mesa"""
        from sqlalchemy.orm import joinedload
        return self.db.query(Order).options(
            joinedload(Order.customer)
        ).filter(
            Order.table_id == table_id,
            Order.business_id == business_id,
            Order.status.in_([OrderStatus.PENDING.value, OrderStatus.PREPARING.value])
        ).first()
    
    def find_all(self, business_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtener todas las órdenes de un negocio"""
        from sqlalchemy.orm import joinedload
        return self.db.query(Order).options(
            joinedload(Order.customer)
        ).filter(
            Order.business_id == business_id
        ).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    
    def create(self, order_data: dict) -> Order:
        """Crear nueva orden"""
        order = Order(**order_data)
        self.db.add(order)
        self.db.flush()
        return order
    
    def update(self, order: Order, update_data: dict) -> Order:
        """Actualizar orden existente"""
        for field, value in update_data.items():
            setattr(order, field, value)
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def delete(self, order: Order) -> None:
        """Eliminar orden"""
        self.db.delete(order)
        self.db.commit()
    
    def commit(self):
        """Commit de transacción"""
        self.db.commit()
    
    def refresh(self, obj):
        """Refresh de objeto"""
        self.db.refresh(obj)


class OrderItemRepository:
    """Repositorio para items de órdenes"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, item_data: dict) -> OrderItem:
        """Crear item de orden"""
        item = OrderItem(**item_data)
        self.db.add(item)
        return item
    
    def delete_all_by_order(self, order_id: int):
        """Eliminar todos los items de una orden"""
        items = self.db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        for item in items:
            self.db.delete(item)


class PaymentRepository:
    """Repositorio para pagos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_payment_method_by_id(self, payment_method_id: int, business_id: int) -> Optional[PaymentMethod]:
        """Buscar método de pago por ID"""
        return self.db.query(PaymentMethod).filter(
            PaymentMethod.id == payment_method_id,
            PaymentMethod.business_id == business_id,
            PaymentMethod.is_active == True,
            PaymentMethod.deleted_at.is_(None)
        ).first()
    
    def create_order_payment(self, payment_data: dict) -> OrderPayment:
        """Crear pago de orden"""
        payment = OrderPayment(**payment_data)
        self.db.add(payment)
        return payment
    
    def get_payment_method_name(self, payment_method_id: int) -> Optional[str]:
        """Obtener nombre del método de pago"""
        method = self.db.query(PaymentMethod).filter(
            PaymentMethod.id == payment_method_id
        ).first()
        return method.name if method else None


class TableRepository:
    """Repositorio para mesas"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, table_id: int, business_id: int) -> Optional[Table]:
        """Buscar mesa por ID"""
        return self.db.query(Table).filter(
            Table.id == table_id,
            Table.business_id == business_id
        ).first()
    
    def update_status(self, table: Table, status: TableStatus):
        """Actualizar estado de mesa"""
        table.status = status
        self.db.commit()


class ProductRepository:
    """Repositorio para productos (para órdenes)"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, product_id: int, business_id: int) -> Optional[Product]:
        """Buscar producto por ID"""
        return self.db.query(Product).filter(
            Product.id == product_id,
            Product.business_id == business_id,
            Product.deleted_at.is_(None)
        ).first()
    
    def update_stock(self, product: Product, quantity_change: int):
        """Actualizar stock de producto"""
        product.stock += quantity_change


class CustomerRepository:
    """Repositorio para clientes"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, customer_id: int, business_id: int) -> Optional[Customer]:
        """Buscar cliente por ID"""
        return self.db.query(Customer).filter(
            Customer.id == customer_id,
            Customer.business_id == business_id,
            Customer.deleted_at.is_(None)
        ).first()


class MenuItemRepository:
    """Repositorio para items del menú"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, menu_item_id: int, business_id: int) -> Optional[MenuItem]:
        """Buscar item del menú por ID"""
        return self.db.query(MenuItem).filter(
            MenuItem.id == menu_item_id,
            MenuItem.business_id == business_id,
            MenuItem.deleted_at.is_(None)
        ).first()
    
    def get_ingredient_quantity(self, menu_item_id: int, product_id: int) -> float:
        """Obtener cantidad de ingrediente necesario para un item del menú"""
        stmt = select(menu_item_ingredients.c.quantity).where(
            menu_item_ingredients.c.menu_item_id == menu_item_id,
            menu_item_ingredients.c.product_id == product_id
        )
        result = self.db.execute(stmt).first()
        return result[0] if result else 0

