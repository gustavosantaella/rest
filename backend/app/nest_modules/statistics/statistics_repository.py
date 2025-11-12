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

