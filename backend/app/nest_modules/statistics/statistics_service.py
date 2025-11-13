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
        stats_repo = StatisticsRepository(db)
        start_date = datetime.now() - timedelta(days=days)
        
        # Obtener productos más vendidos
        best_products = stats_repo.get_best_selling_products(business_id, start_date, limit)
        
        # Obtener items de menú más vendidos
        best_menu_items = stats_repo.get_best_selling_menu_items(business_id, start_date, limit)
        
        # Obtener peores productos (menos vendidos)
        worst_products = stats_repo.get_worst_selling_products(business_id, start_date, limit)
        
        return {
            "period_days": days,
            "best_products": best_products,
            "best_menu_items": best_menu_items,
            "worst_products": worst_products
        }
    
    def get_customer_statistics(self, business_id: int, db: Session):
        """Obtener estadísticas de clientes"""
        stats_repo = StatisticsRepository(db)
        
        total_customers = stats_repo.count_customers(business_id)
        start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        new_this_month = stats_repo.count_new_customers(business_id, start_of_month)
        
        # Obtener clientes con deudas
        customers_with_debt = stats_repo.get_customers_with_debt(business_id)
        
        # Calcular total de deuda
        total_debt = sum(customer['total_pending'] for customer in customers_with_debt)
        
        return {
            "total_customers": total_customers,
            "new_customers_last_30_days": new_this_month,
            "customers_with_debt": customers_with_debt,
            "total_debt_from_customers": float(total_debt)
        }
    
    def get_financial_statistics(self, business_id: int, days: int, db: Session):
        """Obtener estadísticas financieras"""
        stats_repo = StatisticsRepository(db)
        start_date = datetime.now() - timedelta(days=days)
        
        # Obtener ventas totales
        total_income = float(stats_repo.sum_sales(business_id, start_date))
        
        # Obtener ingresos por método de pago
        income_by_method = stats_repo.get_sales_by_payment_method(business_id, start_date)
        
        # Placeholder para gastos (puede implementarse más adelante)
        total_expenses = 0.0
        net_profit = total_income - total_expenses
        
        # Calcular margen de ganancia
        profit_margin = (net_profit / total_income * 100) if total_income > 0 else 0.0
        
        # Obtener cuentas por cobrar y por pagar pendientes
        total_pending_income = float(stats_repo.sum_accounts_receivable_pending(business_id))
        total_pending_expenses = float(stats_repo.sum_accounts_payable_pending(business_id))
        
        # Balance proyectado = ganancia actual + por cobrar - por pagar
        projected_balance = net_profit + total_pending_income - total_pending_expenses
        
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_profit": net_profit,
            "income_by_method": income_by_method,
            "profit_margin": float(profit_margin),
            "total_pending_income": total_pending_income,
            "total_pending_expenses": total_pending_expenses,
            "projected_balance": projected_balance,
            "period_days": days
        }

