"""
Módulo de tipos de negocios para PyNest
"""

from nest.core import Module
from .business_types_controller import BusinessTypesController
from .business_types_service import BusinessTypesService


@Module(
    controllers=[BusinessTypesController],
    providers=[BusinessTypesService],
    exports=[BusinessTypesService]
)
class BusinessTypesModule:
    """Módulo de tipos de negocios"""
    pass

