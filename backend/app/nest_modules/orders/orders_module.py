"""
Módulo de órdenes para PyNest
"""
from nest.core import Module
from .orders_controller import OrdersController
from .orders_service import OrdersService


@Module(
    controllers=[OrdersController],
    providers=[OrdersService],
    exports=[OrdersService]
)
class OrdersModule:
    """Módulo de órdenes"""
    pass

