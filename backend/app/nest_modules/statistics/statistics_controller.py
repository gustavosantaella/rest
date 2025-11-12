"""
Controlador de estadísticas usando PyNest
"""
from nest.core import Controller, Get, Depends
from sqlalchemy.orm import Session
from .statistics_service import StatisticsService
from ...core.database import get_db
from ...models.user import User
from ...utils.dependencies import get_current_user


@Controller("api/statistics")
class StatisticsController:
    """Controlador para rutas de estadísticas"""
    
    def __init__(self, statistics_service: StatisticsService):
        self.statistics_service = statistics_service
    
    @Get("/general")
    def get_general_statistics(
        self,
        days: int = 30,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Obtener estadísticas generales"""
        return self.statistics_service.get_general_statistics(
            current_user.business_id,
            days,
            db
        )
    
    @Get("/best-sellers")
    def get_best_sellers(
        self,
        days: int = 30,
        limit: int = 10,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Obtener productos más vendidos"""
        return self.statistics_service.get_best_sellers(
            current_user.business_id,
            days,
            limit,
            db
        )
    
    @Get("/customers")
    def get_customer_statistics(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Obtener estadísticas de clientes"""
        return self.statistics_service.get_customer_statistics(
            current_user.business_id,
            db
        )
    
    @Get("/financial")
    def get_financial_statistics(
        self,
        days: int = 30,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Obtener estadísticas financieras"""
        return self.statistics_service.get_financial_statistics(
            current_user.business_id,
            days,
            db
        )

