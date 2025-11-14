"""
Módulo de contabilidad usando PyNest
"""
from nest.core import Module
from .accounting_controller import AccountingController
from .accounting_service import AccountingService


@Module(
    controllers=[AccountingController],
    providers=[AccountingService],
    exports=[AccountingService]
)
class AccountingModule:
    """Módulo de contabilidad"""
    pass

