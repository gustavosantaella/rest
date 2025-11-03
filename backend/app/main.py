from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import engine, Base, SessionLocal
from .routers import auth, users, products, tables, orders, menu, configuration, profile, payment_methods, upload, public
from .models.user import User, UserRole
from .utils.security import get_password_hash
import os

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Crear usuario admin por defecto si no existe
def create_default_admin():
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin = User(
                username="admin",
                email="admin@admin.admin",
                full_name="Administrador",
                hashed_password=get_password_hash("123456.Ab!"),
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("\n✅ Usuario administrador creado:")
            print("   Usuario: admin")
            print("   Email: admin@admin.admin")
            print("   Password: 123456.Ab!\n")
    except Exception as e:
        print(f"Error al crear admin: {e}")
        db.rollback()
    finally:
        db.close()

create_default_admin()

app = FastAPI(
    title="Sistema de Gestión para Restaurante/Kiosko",
    description="API completa para gestión de inventario, mesas, órdenes y usuarios",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(tables.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(menu.router, prefix="/api")
app.include_router(configuration.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(payment_methods.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(public.router, prefix="/api")

# Configurar carpeta de archivos estáticos para imágenes
UPLOAD_DIR = "uploads"
UPLOAD_IMAGES_DIR = os.path.join(UPLOAD_DIR, "images")

# Crear carpetas si no existen
os.makedirs(UPLOAD_IMAGES_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/")
def root():
    return {
        "message": "Sistema de Gestión para Restaurante/Kiosko API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}

