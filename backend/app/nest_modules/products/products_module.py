"""
Módulo de productos para PyNest
"""
from nest.core import Module
from .products_controller import ProductsController
from .products_service import ProductsService


@Module(
    controllers=[ProductsController],
    providers=[ProductsService],
    exports=[ProductsService]
)
class ProductsModule:
    """Módulo de productos"""
    pass

