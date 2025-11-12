"""
Módulo de métodos de pago para PyNest
"""
from nest.core import Module
from .payment_methods_controller import PaymentMethodsController
from .payment_methods_service import PaymentMethodsService


@Module(
    controllers=[PaymentMethodsController],
    providers=[PaymentMethodsService],
    exports=[PaymentMethodsService]
)
class PaymentMethodsModule:
    """Módulo de métodos de pago"""
    pass

