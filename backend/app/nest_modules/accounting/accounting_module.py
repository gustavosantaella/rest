"""
Módulo de contabilidad usando PyNest
"""
from nest.core import Module
from .accounting_controller import AccountingController
from .accounting_service import AccountingService
from .accounting_integration_service import AccountingIntegrationService


@Module(
    controllers=[AccountingController],
    providers=[AccountingService, AccountingIntegrationService],
    exports=[AccountingService, AccountingIntegrationService]
)
class AccountingModule:
    """Módulo de contabilidad"""
    pass

