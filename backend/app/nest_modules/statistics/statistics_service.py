"""
Servicio de estadísticas usando PyNest - Lógica de negocio
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .statistics_repository import StatisticsRepository


@Injectable
class StatisticsService:
    """Servicio para lógica de negocio de estadísticas"""
    
    def __init__(self):
        pass
    
    def get_general_statistics(self, business_id: int, days: int, db: Session):
        """Obtener estadísticas generales"""
        stats_repo = StatisticsRepository(db)
        start_date = datetime.now() - timedelta(days=days)
        
        total_orders = stats_repo.count_orders(business_id, start_date)
        total_sales = stats_repo.sum_sales(business_id, start_date)
        total_customers = stats_repo.count_customers(business_id)
        
        return {
            "total_orders": total_orders,
            "total_sales": total_sales,
            "total_customers": total_customers,
            "period_days": days
        }
    
    def get_best_sellers(self, business_id: int, days: int, limit: int, db: Session):
        """Obtener productos más vendidos"""
        # Placeholder por ahora
        return []
    
    def get_customer_statistics(self, business_id: int, db: Session):
        """Obtener estadísticas de clientes"""
        stats_repo = StatisticsRepository(db)
        
        total_customers = stats_repo.count_customers(business_id)
        start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        new_this_month = stats_repo.count_new_customers(business_id, start_of_month)
        
        return {
            "total_customers": total_customers,
            "new_this_month": new_this_month,
            "active": total_customers
        }
    
    def get_financial_statistics(self, business_id: int, days: int, db: Session):
        """Obtener estadísticas financieras"""
        stats_repo = StatisticsRepository(db)
        start_date = datetime.now() - timedelta(days=days)
        
        total_sales = stats_repo.sum_sales(business_id, start_date)
        
        return {
            "total_sales": total_sales,
            "total_expenses": 0,  # Placeholder
            "profit": total_sales,
            "period_days": days
        }

