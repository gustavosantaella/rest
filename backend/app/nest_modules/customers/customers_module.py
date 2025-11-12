"""
Módulo de clientes para PyNest
"""
from nest.core import Module
from .customers_controller import CustomersController
from .customers_service import CustomersService


@Module(
    controllers=[CustomersController],
    providers=[CustomersService],
    exports=[CustomersService]
)
class CustomersModule:
    """Módulo de clientes"""
    pass

