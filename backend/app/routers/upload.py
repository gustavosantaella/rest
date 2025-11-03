from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Optional
import os
import shutil
from datetime import datetime
import uuid

router = APIRouter(prefix="/upload", tags=["Upload"])

# Directorio para guardar las imágenes
UPLOAD_DIR = "uploads/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Extensiones permitidas
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def get_file_extension(filename: str) -> str:
    """Obtiene la extensión del archivo"""
    return os.path.splitext(filename)[1].lower()

def is_allowed_file(filename: str) -> bool:
    """Verifica si la extensión del archivo es permitida"""
    return get_file_extension(filename) in ALLOWED_EXTENSIONS

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    """
    Sube una imagen al servidor.
    Retorna la URL de la imagen subida.
    """
    
    # Validar extensión
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido. Extensiones permitidas: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Validar tamaño (máximo 5MB)
    file.file.seek(0, 2)  # Ir al final del archivo
    file_size = file.file.tell()  # Obtener posición (tamaño)
    file.file.seek(0)  # Volver al inicio
    
    MAX_SIZE = 5 * 1024 * 1024  # 5MB
    if file_size > MAX_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"El archivo es demasiado grande. Tamaño máximo: 5MB"
        )
    
    # Generar nombre único
    file_extension = get_file_extension(file.filename)
    unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    try:
        # Guardar archivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Retornar URL relativa
        image_url = f"/uploads/images/{unique_filename}"
        return {"image_url": image_url, "filename": unique_filename}
    
    except Exception as e:
        # Limpiar archivo si hubo error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {str(e)}")

@router.delete("/image")
async def delete_image(image_url: str):
    """
    Elimina una imagen del servidor.
    """
    try:
        # Extraer el nombre del archivo de la URL
        filename = os.path.basename(image_url)
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"message": "Imagen eliminada correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la imagen: {str(e)}")

