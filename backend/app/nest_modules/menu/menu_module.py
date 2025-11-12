"""
Módulo de menú para PyNest
"""
from nest.core import Module
from .menu_controller import MenuController
from .menu_service import MenuService


@Module(
    controllers=[MenuController],
    providers=[MenuService],
    exports=[MenuService]
)
class MenuModule:
    """Módulo de menú"""
    pass

