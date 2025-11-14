"""
Módulo de cuentas por cobrar para PyNest
"""
from nest.core import Module
from .accounts_receivable_controller import AccountsReceivableController
from .accounts_receivable_service import AccountsReceivableService
from ..accounting.accounting_module import AccountingModule


@Module(
    controllers=[AccountsReceivableController],
    providers=[AccountsReceivableService],
    imports=[AccountingModule],  # Importar para inyectar AccountingIntegrationService
    exports=[AccountsReceivableService]
)
class AccountsReceivableModule:
    """Módulo de cuentas por cobrar"""
    pass

