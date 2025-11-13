"""
Controlador público usando PyNest - Endpoints sin autenticación
"""
from nest.core import Controller, Get, Depends
from sqlalchemy.orm import Session
from .public_service import PublicService
from ...core.database import get_db


@Controller("api/public")
class PublicController:
    """Controlador para rutas públicas (sin autenticación)"""
    
    def __init__(self, service: PublicService):
        self.service = service
    
    @Get("/{slug}/info")
    def get_business_info(
        self,
        slug: str,
        db: Session = Depends(get_db)
    ):
        """Obtener información pública del negocio"""
        return self.service.get_business_info(slug, db)
    
    @Get("/{slug}/catalog")
    def get_catalog(
        self,
        slug: str,
        db: Session = Depends(get_db)
    ):
        """Obtener catálogo completo del negocio (menú + productos)"""
        return self.service.get_catalog(slug, db)
    
    @Get("/{slug}/products")
    def get_products(
        self,
        slug: str,
        db: Session = Depends(get_db)
    ):
        """Obtener productos del catálogo público"""
        return self.service.get_public_products(slug, db)
    
    @Get("/{slug}/menu")
    def get_menu(
        self,
        slug: str,
        db: Session = Depends(get_db)
    ):
        """Obtener menú del catálogo público"""
        return self.service.get_public_menu(slug, db)
    
    @Get("/{slug}/menu-categories")
    def get_menu_categories(
        self,
        slug: str,
        db: Session = Depends(get_db)
    ):
        """Obtener categorías del menú"""
        return self.service.get_menu_categories(slug, db)
    
    @Get("/{slug}/menu/{item_id}")
    def get_menu_item_detail(
        self,
        slug: str,
        item_id: int,
        db: Session = Depends(get_db)
    ):
        """Obtener detalle de un item del menú"""
        return self.service.get_menu_item_detail(slug, item_id, db)

