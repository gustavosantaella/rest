"""
Controlador de upload de imágenes usando PyNest
"""

from nest.core import Controller, Post, Delete, Depends
from fastapi import UploadFile, File, Query, status, HTTPException
from typing import Optional
from .upload_service import UploadService
from ...utils.dependencies import get_current_user
from ...models.user import User


@Controller("api/upload")
class UploadController:
    """Controlador para rutas de upload"""

    def __init__(self, upload_service: UploadService):
        self.upload_service = upload_service

    @Post("/image", status_code=status.HTTP_201_CREATED)
    def upload_image(
        self,
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user)
    ) -> dict:
        """
        Subir una imagen
        
        Args:
            file: Archivo de imagen a subir
            current_user: Usuario autenticado
            
        Returns:
            dict: Diccionario con image_url y filename
        """
        return self.upload_service.upload_image(file)

    @Delete("/image", status_code=status.HTTP_200_OK)
    def delete_image(
        self,
        image_url: str = Query(..., description="URL de la imagen a eliminar"),
        current_user: User = Depends(get_current_user)
    ) -> dict:
        """
        Eliminar una imagen
        
        Args:
            image_url: URL de la imagen a eliminar
            current_user: Usuario autenticado
            
        Returns:
            dict: Mensaje de confirmación
        """
        return self.upload_service.delete_image(image_url)

