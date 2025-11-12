"""
Módulo de perfil para PyNest
"""
from nest.core import Module
from .profile_controller import ProfileController
from .profile_service import ProfileService


@Module(
    controllers=[ProfileController],
    providers=[ProfileService],
    exports=[ProfileService]
)
class ProfileModule:
    """Módulo de perfil de usuario"""
    pass

