"""
Módulo de configuración para PyNest
"""
from nest.core import Module
from .configuration_controller import ConfigurationController
from .configuration_service import ConfigurationService


@Module(
    controllers=[ConfigurationController],
    providers=[ConfigurationService],
    exports=[ConfigurationService]
)
class ConfigurationModule:
    """Módulo de configuración"""
    pass

