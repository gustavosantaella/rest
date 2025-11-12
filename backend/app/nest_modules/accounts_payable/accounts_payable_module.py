"""
Módulo de cuentas por pagar para PyNest
"""
from nest.core import Module
from .accounts_payable_controller import AccountsPayableController
from .accounts_payable_service import AccountsPayableService


@Module(
    controllers=[AccountsPayableController],
    providers=[AccountsPayableService],
    exports=[AccountsPayableService]
)
class AccountsPayableModule:
    """Módulo de cuentas por pagar"""
    pass

