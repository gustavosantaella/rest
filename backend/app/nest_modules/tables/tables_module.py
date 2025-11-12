"""
Módulo de mesas para PyNest
"""
from nest.core import Module
from .tables_controller import TablesController
from .tables_service import TablesService


@Module(
    controllers=[TablesController],
    providers=[TablesService],
    exports=[TablesService]
)
class TablesModule:
    """Módulo de mesas"""
    pass

