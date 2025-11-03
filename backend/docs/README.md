# Backend - Sistema de Gestión para Restaurante/Kiosko

API completa desarrollada con FastAPI y PostgreSQL para gestión integral de restaurantes, kioskos y locales comerciales.

## 🚀 Tecnologías

- **Framework:** FastAPI 0.104.1
- **Base de Datos:** PostgreSQL (con SQLAlchemy 2.0)
- **Autenticación:** JWT (python-jose)
- **Seguridad:** Bcrypt, Passlib
- **Validación:** Pydantic 2.5
- **Generación de QR:** qrcode + Pillow
- **Servidor:** Uvicorn

## 📁 Estructura del Proyecto

```
backend/
├── app/
│   ├── models/          # Modelos de base de datos (SQLAlchemy)
│   ├── schemas/         # Schemas de validación (Pydantic)
│   ├── routers/         # Endpoints de la API
│   ├── utils/           # Utilidades (auth, security)
│   ├── config.py        # Configuración de la app
│   ├── database.py      # Conexión a PostgreSQL
│   └── main.py          # Aplicación principal
├── db/
│   └── migrations/      # Scripts de migración de BD
├── docs/                # Documentación
├── uploads/             # Archivos subidos (imágenes)
├── requirements.txt     # Dependencias Python
└── run.py              # Script de ejecución
```

## ⚙️ Instalación

### 1. Crear entorno virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar base de datos

Crea un archivo `.env` en la raíz del backend:

```env
DATABASE_URL=postgresql://usuario:password@localhost/nombre_bd
SECRET_KEY=tu_clave_secreta_muy_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Ejecutar migraciones

```bash
# Ver orden de ejecución en db/migrations/README.md
.venv\Scripts\python.exe db/migrations/migrate_add_profile_fields.py
.venv\Scripts\python.exe db/migrations/migrate_add_payment_methods.py
# ... etc
```

### 5. Iniciar servidor

```bash
python run.py
```

El servidor estará disponible en: `http://localhost:8000`

## 📚 Documentación de la API

Una vez iniciado el servidor, visita:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## 🔐 Usuario por Defecto

Al iniciar por primera vez, se crea automáticamente un usuario administrador:

```
Email: admin@admin.admin
Password: 123456.Ab!
```

**⚠️ Importante:** Cambia estas credenciales en producción.

## 🗂️ Módulos Principales

### Autenticación
- `/api/auth/login` - Login con JWT
- `/api/auth/me` - Usuario actual

### Usuarios
- CRUD completo de usuarios
- Roles: Admin, Manager, Waiter, Cashier, Chef
- Permisos basados en roles

### Inventario
- Gestión de productos y categorías
- Tipos de unidad: unidad, gramo, kg, ml, litro, granel
- Control de stock con alertas
- Precios de compra y venta
- Imágenes de productos

### Menú
- Gestión de platillos y categorías
- Ingredientes vinculados al inventario
- Platillos destacados
- Tiempo de preparación
- Imágenes de platillos

### Mesas
- Estados: Disponible, Ocupada, Reservada, Limpieza
- Capacidad y ubicación
- Actualización en tiempo real

### Órdenes
- Items del menú o inventario
- Pagos múltiples/mixtos
- Estados: Pendiente, Preparando, Completado, Cancelado
- Datos del cliente
- Historial de pagos

### Configuración
- Información del negocio
- Socios y participaciones
- Métodos de pago
- Slug para catálogo público
- Generación de código QR

### Catálogo Público
- `/api/public/{slug}/info` - Info del negocio
- `/api/public/{slug}/menu` - Menú público
- `/api/public/{slug}/products` - Productos públicos
- ❌ **Sin autenticación requerida**

## 🛠️ Comandos Útiles

### Desarrollo

```bash
# Iniciar servidor en modo desarrollo (con auto-reload)
python run.py

# O directamente con uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Ejecutar tests (si existen)
pytest
```

### Base de Datos

```bash
# Inicializar base de datos
python init_db.py

# Ejecutar migración específica
.venv\Scripts\python.exe db/migrations/nombre_migracion.py
```

## 📖 Documentación Adicional

Ver carpeta `docs/` para:
- `MIGRATION_GUIDE.md` - Guía de migraciones
- `PAYMENT_METHODS_COMPLETE.md` - Sistema de pagos
- `TROUBLESHOOTING.md` - Solución de problemas

## 🔒 Seguridad

- Contraseñas hasheadas con bcrypt
- Tokens JWT con expiración
- Validación de permisos por rol
- CORS configurado
- SQL injection protection (SQLAlchemy ORM)

## 📦 Dependencias Principales

Ver `requirements.txt` completo. Principales:
- `fastapi` - Framework web
- `sqlalchemy` - ORM
- `psycopg2-binary` - Driver PostgreSQL
- `pydantic` - Validación de datos
- `python-jose` - JWT
- `passlib` + `bcrypt` - Hashing de passwords
- `qrcode` + `pillow` - Generación de QR

## 🌐 CORS

Por defecto configurado para:
- `http://localhost:4200` (Angular)

Modifica en `app/main.py` según tu configuración.

## 📝 Licencia

Proyecto desarrollado para gestión de restaurantes y locales comerciales.
