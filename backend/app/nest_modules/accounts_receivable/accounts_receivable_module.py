"""
Módulo de cuentas por cobrar para PyNest
"""
from nest.core import Module
from .accounts_receivable_controller import AccountsReceivableController
from .accounts_receivable_service import AccountsReceivableService


@Module(
    controllers=[AccountsReceivableController],
    providers=[AccountsReceivableService],
    exports=[AccountsReceivableService]
)
class AccountsReceivableModule:
    """Módulo de cuentas por cobrar"""
    pass

