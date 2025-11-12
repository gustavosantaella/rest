"""
Configuración de base de datos para PyNest
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import settings

# Crear engine
engine = create_engine(settings.DATABASE_URL)

# SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()


def get_db():
    """Dependency para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializar base de datos - crear tablas"""
    Base.metadata.create_all(bind=engine)

