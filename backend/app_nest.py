"""
Aplicación principal usando PyNest
"""

from nest.core import PyNestFactory, Module
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Importar módulos PyNest migrados
from app.nest_modules.auth.auth_module import AuthModule
from app.nest_modules.products.products_module import ProductsModule
from app.nest_modules.customers.customers_module import CustomersModule
from app.nest_modules.users.users_module import UsersModule
from app.nest_modules.tables.tables_module import TablesModule
from app.nest_modules.profile.profile_module import ProfileModule
from app.nest_modules.orders.orders_module import OrdersModule
from app.nest_modules.menu.menu_module import MenuModule
from app.nest_modules.configuration.configuration_module import ConfigurationModule
from app.nest_modules.payment_methods.payment_methods_module import PaymentMethodsModule
from app.nest_modules.accounts_receivable.accounts_receivable_module import (
    AccountsReceivableModule,
)
from app.nest_modules.accounts_payable.accounts_payable_module import (
    AccountsPayableModule,
)
from app.nest_modules.permissions.permissions_module import PermissionsModule
from app.nest_modules.roles.roles_module import RolesModule
from app.nest_modules.statistics.statistics_module import StatisticsModule

# Importar routers legacy (temporal - hasta completar migración)
from app.routers import (
    orders,
    menu,
    configuration,
    payment_methods,
    upload,
    public,
    permissions,
    roles,
    system_permissions,
    accounts_receivable,
    accounts_payable,
    statistics,
)


@Module(
    imports=[
        AuthModule,
        ProductsModule,
        CustomersModule,
        UsersModule,
        TablesModule,
        ProfileModule,
        OrdersModule,
        MenuModule,
        ConfigurationModule,
        PaymentMethodsModule,
        AccountsReceivableModule,
        AccountsPayableModule,
        PermissionsModule,
        RolesModule,
        StatisticsModule,
    ]
)
class AppModule:
    """Módulo principal de la aplicación"""

    pass


# Crear la aplicación PyNest con prefijo /api
http_server = PyNestFactory.create(
    AppModule,
    description="Sistema de Gestión para Restaurante/Kiosko",
    title="Restaurant Management API",
    version="2.0.0",
    debug=True,
)

# En PyNest 0.4.0, el objeto devuelto ES la aplicación FastAPI
app = http_server.get_server()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers legacy temporalmente (hasta completar migración)
app.include_router(orders.router, prefix="/api")
app.include_router(menu.router, prefix="/api")
app.include_router(configuration.router, prefix="/api")
app.include_router(payment_methods.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(permissions.router, prefix="/api")
app.include_router(roles.router, prefix="/api")
app.include_router(system_permissions.router, prefix="/api")
app.include_router(public.router, prefix="/api")
app.include_router(accounts_receivable.router, prefix="/api")
app.include_router(accounts_payable.router, prefix="/api")
app.include_router(statistics.router, prefix="/api")

# Configurar archivos estáticos
UPLOAD_DIR = "uploads"
UPLOAD_IMAGES_DIR = os.path.join(UPLOAD_DIR, "images")
os.makedirs(UPLOAD_IMAGES_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/")
def root():
    return {
        "message": "Sistema de Gestión para Restaurante/Kiosko API - PyNest",
        "version": "2.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "framework": "PyNest"}
