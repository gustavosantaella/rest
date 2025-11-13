"""
Repositorio de estadísticas - Operaciones de base de datos
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Optional
from ...models.order import Order
from ...models.customer import Customer


class StatisticsRepository:
    """Repositorio para operaciones de BD de estadísticas"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def count_orders(self, business_id: int, start_date: datetime) -> int:
        """Contar órdenes desde una fecha"""
        return self.db.query(Order).filter(
            Order.business_id == business_id,
            Order.created_at >= start_date
        ).count()
    
    def sum_sales(self, business_id: int, start_date: datetime) -> float:
        """Sumar ventas pagadas desde una fecha"""
        total = self.db.query(func.sum(Order.total)).filter(
            Order.business_id == business_id,
            Order.created_at >= start_date,
            Order.payment_status == "paid"
        ).scalar()
        return float(total) if total else 0.0
    
    def count_customers(self, business_id: int) -> int:
        """Contar clientes activos"""
        return self.db.query(Customer).filter(
            Customer.business_id == business_id,
            Customer.deleted_at.is_(None)
        ).count()
    
    def count_new_customers(self, business_id: int, start_date: datetime) -> int:
        """Contar clientes nuevos desde una fecha"""
        return self.db.query(Customer).filter(
            Customer.business_id == business_id,
            Customer.created_at >= start_date,
            Customer.deleted_at.is_(None)
        ).count()
    
    def get_sales_by_payment_method(self, business_id: int, start_date: datetime) -> dict:
        """Obtener ventas agrupadas por método de pago"""
        from ...models.order_payment import OrderPayment
        from ...models.payment_method import PaymentMethod
        
        # Obtener pagos agrupados por método
        results = self.db.query(
            PaymentMethod.name,
            func.sum(OrderPayment.amount).label('total')
        ).join(
            OrderPayment, PaymentMethod.id == OrderPayment.payment_method_id
        ).join(
            Order, OrderPayment.order_id == Order.id
        ).filter(
            Order.business_id == business_id,
            Order.created_at >= start_date
        ).group_by(PaymentMethod.name).all()
        
        # Convertir a diccionario
        sales_by_method = {}
        for method_name, total in results:
            if method_name:
                sales_by_method[method_name] = float(total) if total else 0.0
        
        # Si no hay datos, devolver estructura vacía
        if not sales_by_method:
            sales_by_method = {"Sin pagos registrados": 0.0}
        
        return sales_by_method
    
    def sum_accounts_receivable_pending(self, business_id: int) -> float:
        """Sumar montos pendientes de cuentas por cobrar"""
        from ...models.account_receivable import AccountReceivable
        
        total = self.db.query(func.sum(AccountReceivable.amount_pending)).filter(
            AccountReceivable.business_id == business_id,
            AccountReceivable.status.in_(['pending', 'partial', 'overdue']),
            AccountReceivable.deleted_at.is_(None)
        ).scalar()
        
        return float(total) if total else 0.0
    
    def sum_accounts_payable_pending(self, business_id: int) -> float:
        """Sumar montos pendientes de cuentas por pagar"""
        from ...models.account_payable import AccountPayable
        
        total = self.db.query(func.sum(AccountPayable.amount_pending)).filter(
            AccountPayable.business_id == business_id,
            AccountPayable.status.in_(['pending', 'partial', 'overdue']),
            AccountPayable.deleted_at.is_(None)
        ).scalar()
        
        return float(total) if total else 0.0
    
    def get_customers_with_debt(self, business_id: int) -> list:
        """Obtener clientes con deudas pendientes"""
        from ...models.account_receivable import AccountReceivable
        
        # Agrupar cuentas por cobrar por cliente
        results = self.db.query(
            Customer.id,
            Customer.nombre,
            Customer.apellido,
            func.count(AccountReceivable.id).label('accounts_count'),
            func.sum(AccountReceivable.amount_pending).label('total_pending')
        ).join(
            AccountReceivable, Customer.id == AccountReceivable.customer_id
        ).filter(
            Customer.business_id == business_id,
            AccountReceivable.status.in_(['pending', 'partial', 'overdue']),
            AccountReceivable.deleted_at.is_(None),
            Customer.deleted_at.is_(None)
        ).group_by(
            Customer.id, Customer.nombre, Customer.apellido
        ).order_by(
            func.sum(AccountReceivable.amount_pending).desc()
        ).limit(10).all()
        
        # Formatear resultados
        customers_with_debt = []
        for customer_id, nombre, apellido, accounts_count, total_pending in results:
            customers_with_debt.append({
                "id": customer_id,
                "name": f"{nombre} {apellido}",
                "accounts_count": accounts_count,
                "total_pending": float(total_pending) if total_pending else 0.0
            })
        
        return customers_with_debt
    
    def get_best_selling_products(self, business_id: int, start_date: datetime, limit: int) -> list:
        """Obtener productos más vendidos"""
        from ...models.order import OrderItem
        from ...models.product import Product
        
        results = self.db.query(
            Product.id,
            Product.name,
            func.sum(OrderItem.quantity).label('quantity'),
            func.sum(OrderItem.subtotal).label('total_sales')
        ).join(
            OrderItem, Product.id == OrderItem.product_id
        ).join(
            Order, OrderItem.order_id == Order.id
        ).filter(
            Order.business_id == business_id,
            Order.created_at >= start_date,
            OrderItem.product_id.isnot(None),
            OrderItem.deleted_at.is_(None)
        ).group_by(
            Product.id, Product.name
        ).order_by(
            func.sum(OrderItem.quantity).desc()
        ).limit(limit).all()
        
        return [
            {
                "id": product_id,
                "name": name,
                "quantity": int(quantity) if quantity else 0,
                "total_sales": float(total_sales) if total_sales else 0.0
            }
            for product_id, name, quantity, total_sales in results
        ]
    
    def get_best_selling_menu_items(self, business_id: int, start_date: datetime, limit: int) -> list:
        """Obtener items de menú más vendidos"""
        from ...models.order import OrderItem
        from ...models.menu import MenuItem
        
        results = self.db.query(
            MenuItem.id,
            MenuItem.name,
            func.sum(OrderItem.quantity).label('quantity'),
            func.sum(OrderItem.subtotal).label('total_sales')
        ).join(
            OrderItem, MenuItem.id == OrderItem.menu_item_id
        ).join(
            Order, OrderItem.order_id == Order.id
        ).filter(
            Order.business_id == business_id,
            Order.created_at >= start_date,
            OrderItem.menu_item_id.isnot(None),
            OrderItem.deleted_at.is_(None)
        ).group_by(
            MenuItem.id, MenuItem.name
        ).order_by(
            func.sum(OrderItem.quantity).desc()
        ).limit(limit).all()
        
        return [
            {
                "id": menu_id,
                "name": name,
                "quantity": int(quantity) if quantity else 0,
                "total_sales": float(total_sales) if total_sales else 0.0
            }
            for menu_id, name, quantity, total_sales in results
        ]
    
    def get_worst_selling_products(self, business_id: int, start_date: datetime, limit: int) -> list:
        """Obtener productos menos vendidos"""
        from ...models.order import OrderItem
        from ...models.product import Product
        
        results = self.db.query(
            Product.id,
            Product.name,
            func.coalesce(func.sum(OrderItem.quantity), 0).label('quantity'),
            func.coalesce(func.sum(OrderItem.subtotal), 0).label('total_sales')
        ).outerjoin(
            OrderItem, Product.id == OrderItem.product_id
        ).outerjoin(
            Order, OrderItem.order_id == Order.id
        ).filter(
            Product.business_id == business_id,
            Product.deleted_at.is_(None)
        ).group_by(
            Product.id, Product.name
        ).order_by(
            func.coalesce(func.sum(OrderItem.quantity), 0).asc()
        ).limit(limit).all()
        
        return [
            {
                "id": product_id,
                "name": name,
                "quantity": int(quantity) if quantity else 0,
                "total_sales": float(total_sales) if total_sales else 0.0
            }
            for product_id, name, quantity, total_sales in results
        ]

