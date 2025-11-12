"""
Módulo de configuración para PyNest
"""
from nest.core import Module


@Module(
    controllers=[],
    providers=[]
)
class ConfigurationModule:
    """Módulo de configuración (usar legacy router temporalmente)"""
    pass

