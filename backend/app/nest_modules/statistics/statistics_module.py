"""
Módulo de estadísticas para PyNest
"""
from nest.core import Module
from .statistics_controller import StatisticsController
from .statistics_service import StatisticsService


@Module(
    controllers=[StatisticsController],
    providers=[StatisticsService],
    exports=[StatisticsService]
)
class StatisticsModule:
    """Módulo de estadísticas"""
    pass

