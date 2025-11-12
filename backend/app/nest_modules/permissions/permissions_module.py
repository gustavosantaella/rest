"""
Módulo de permisos para PyNest
"""
from nest.core import Module
from .permissions_controller import PermissionsController, SystemPermissionsController
from .permissions_service import PermissionsService


@Module(
    controllers=[PermissionsController, SystemPermissionsController],
    providers=[PermissionsService],
    exports=[PermissionsService]
)
class PermissionsModule:
    """Módulo de permisos"""
    pass

