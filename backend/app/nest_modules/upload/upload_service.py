"""
Servicio de upload de imágenes
"""

import os
import uuid
from nest.core import Injectable
from fastapi import UploadFile, HTTPException, status
from pathlib import Path


@Injectable
class UploadService:
    """Servicio para manejar la subida de archivos"""

    def __init__(self):
        # Directorio base para uploads
        self.upload_dir = Path("uploads")
        self.images_dir = self.upload_dir / "images"
        
        # Crear directorios si no existen
        self.images_dir.mkdir(parents=True, exist_ok=True)
    
    def upload_image(self, file: UploadFile) -> dict:
        """
        Subir una imagen
        
        Args:
            file: Archivo de imagen a subir
            
        Returns:
            dict: Diccionario con image_url y filename
        """
        # Validar tipo de archivo
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de archivo no permitido. Tipos permitidos: {', '.join(allowed_types)}"
            )
        
        # Leer contenido del archivo
        file_content = file.file.read()
        
        # Validar tamaño (máximo 5MB)
        file_size = len(file_content)
        max_size = 5 * 1024 * 1024  # 5MB
        
        if file_size > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo es demasiado grande. Tamaño máximo: 5MB"
            )
        
        # Validar que el archivo no esté vacío
        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo está vacío"
            )
        
        # Generar nombre único para el archivo
        file_extension = Path(file.filename).suffix or ".jpg"
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = self.images_dir / unique_filename
        
        # Guardar archivo
        try:
            # Resetear el puntero del archivo antes de escribir
            file.file.seek(0)
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            # Generar URL relativa
            image_url = f"/uploads/images/{unique_filename}"
            
            return {
                "image_url": image_url,
                "filename": unique_filename
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al guardar el archivo: {str(e)}"
            )
    
    def delete_image(self, image_url: str) -> dict:
        """
        Eliminar una imagen
        
        Args:
            image_url: URL de la imagen a eliminar
            
        Returns:
            dict: Mensaje de confirmación
        """
        try:
            # Extraer el nombre del archivo de la URL
            if image_url.startswith("/uploads/images/"):
                filename = image_url.replace("/uploads/images/", "")
            elif image_url.startswith("uploads/images/"):
                filename = image_url.replace("uploads/images/", "")
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="URL de imagen inválida"
                )
            
            file_path = self.images_dir / filename
            
            # Verificar que el archivo existe
            if not file_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Imagen no encontrada"
                )
            
            # Eliminar archivo
            file_path.unlink()
            
            return {"message": "Imagen eliminada exitosamente"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar la imagen: {str(e)}"
            )

