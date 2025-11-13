"""
Módulo público de PyNest
"""
from nest.core import Module
from .public_controller import PublicController
from .public_service import PublicService


@Module(
    controllers=[PublicController],
    providers=[PublicService],
)
class PublicModule:
    """Módulo para endpoints públicos"""
    pass

