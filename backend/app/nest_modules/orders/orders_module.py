"""
Módulo de órdenes para PyNest
"""
from nest.core import Module
from .orders_controller import OrdersController
from .orders_service import OrdersService
from ..accounting.accounting_module import AccountingModule


@Module(
    controllers=[OrdersController],
    providers=[OrdersService],
    imports=[AccountingModule],  # Importar para inyectar AccountingIntegrationService
    exports=[OrdersService]
)
class OrdersModule:
    """Módulo de órdenes"""
    pass

