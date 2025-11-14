"""
Módulo de upload usando PyNest
"""

from nest.core import Module
from .upload_controller import UploadController
from .upload_service import UploadService


@Module(
    controllers=[UploadController],
    providers=[UploadService],
    exports=[UploadService]
)
class UploadModule:
    """Módulo de upload de imágenes"""
    pass

