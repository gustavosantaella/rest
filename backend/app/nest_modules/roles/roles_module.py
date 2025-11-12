"""
Módulo de roles para PyNest
"""
from nest.core import Module
from .roles_controller import RolesController
from .roles_service import RolesService


@Module(
    controllers=[RolesController],
    providers=[RolesService],
    exports=[RolesService]
)
class RolesModule:
    """Módulo de roles"""
    pass

