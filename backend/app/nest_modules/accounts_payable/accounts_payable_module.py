"""
Módulo de cuentas por pagar para PyNest
"""
from nest.core import Module
from .accounts_payable_controller import AccountsPayableController
from .accounts_payable_service import AccountsPayableService
from ..accounting.accounting_module import AccountingModule


@Module(
    controllers=[AccountsPayableController],
    providers=[AccountsPayableService],
    imports=[AccountingModule],  # Importar para inyectar AccountingIntegrationService
    exports=[AccountsPayableService]
)
class AccountsPayableModule:
    """Módulo de cuentas por pagar"""
    pass

