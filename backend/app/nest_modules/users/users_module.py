"""
Módulo de usuarios para PyNest
"""
from nest.core import Module
from .users_controller import UsersController
from .users_service import UsersService


@Module(
    controllers=[UsersController],
    providers=[UsersService],
    exports=[UsersService]
)
class UsersModule:
    """Módulo de usuarios"""
    pass

