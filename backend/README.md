# Backend - Sistema de Gestión para Restaurante/Kiosko

API REST desarrollada con FastAPI y PostgreSQL para gestión completa de restaurantes, kioskos y locales comerciales.

## 🚀 Características

- ✅ **Autenticación JWT** con roles y permisos
- 📦 **Gestión de Inventario** (productos, categorías, unidades de medida)
- 🍽️ **Gestión de Mesas** con estados (disponible, ocupada, reservada)
- 🧾 **Gestión de Órdenes/Cuentas** con items y cálculo automático
- 👥 **Gestión de Usuarios** con diferentes roles (admin, manager, waiter, cashier)
- 💰 **Precios de compra y venta**
- ⚖️ **Múltiples unidades de medida** (unidad, gramo, kilo, litro, etc.)

## 📋 Requisitos

- Python 3.8+
- PostgreSQL 12+

## 🔧 Instalación

1. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

> **Nota sobre bcrypt:** Si tienes problemas con bcrypt, ejecuta:
> ```bash
> # Windows
> update_dependencies.bat
> 
> # Linux/Mac
> chmod +x update_dependencies.sh
> ./update_dependencies.sh
> ```

3. **Configurar variables de entorno:**
```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:
```
DATABASE_URL=postgresql://user:password@localhost:5432/restaurant_db
SECRET_KEY=tu-clave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. **Crear la base de datos PostgreSQL:**
```bash
# Conectarse a PostgreSQL
psql -U postgres

# Crear la base de datos
CREATE DATABASE restaurant_db;
```

5. **Inicializar la base de datos (opcional):**
```bash
python init_db.py
```

Este script creará las tablas y el usuario administrador por defecto:
- **Usuario:** admin
- **Email:** admin@admin.admin
- **Password:** 123456.Ab!
- **Rol:** Administrador

## ▶️ Ejecutar

```bash
python run.py
# O alternativamente:
uvicorn app.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

> **Nota:** El usuario administrador se crea automáticamente al iniciar la aplicación si no existe.

## 📚 Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación principal FastAPI
│   ├── config.py            # Configuración y variables de entorno
│   ├── database.py          # Conexión a base de datos
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── table.py
│   │   └── order.py
│   ├── schemas/             # Schemas Pydantic
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── table.py
│   │   └── order.py
│   ├── routers/             # Endpoints de la API
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── tables.py
│   │   └── orders.py
│   └── utils/               # Utilidades
│       ├── security.py      # JWT y passwords
│       └── dependencies.py  # Dependencias de FastAPI
├── requirements.txt
├── .env.example
└── README.md
```

## 🔐 Roles y Permisos

- **ADMIN**: Acceso total al sistema
- **MANAGER**: Gestión de inventario, mesas y usuarios
- **WAITER**: Gestión de órdenes y mesas
- **CASHIER**: Gestión de pagos y cierre de cuentas
- **CHEF**: Visualización de órdenes de cocina

## 📝 Endpoints Principales

### Autenticación
- `POST /api/auth/register` - Registrar nuevo usuario
- `POST /api/auth/login` - Login y obtener token JWT

### Usuarios
- `GET /api/users/me` - Obtener usuario actual
- `GET /api/users/` - Listar usuarios (admin)
- `PUT /api/users/{id}` - Actualizar usuario (admin)

### Productos
- `POST /api/products/categories` - Crear categoría
- `GET /api/products/categories` - Listar categorías
- `POST /api/products/` - Crear producto
- `GET /api/products/` - Listar productos
- `PUT /api/products/{id}` - Actualizar producto
- `DELETE /api/products/{id}` - Eliminar producto

### Mesas
- `POST /api/tables/` - Crear mesa
- `GET /api/tables/` - Listar mesas
- `PUT /api/tables/{id}` - Actualizar mesa
- `DELETE /api/tables/{id}` - Eliminar mesa

### Órdenes
- `POST /api/orders/` - Crear orden
- `GET /api/orders/` - Listar órdenes
- `GET /api/orders/{id}` - Obtener orden
- `PUT /api/orders/{id}` - Actualizar orden (pagar, cancelar)
- `DELETE /api/orders/{id}` - Eliminar orden

## 🔄 Flujo de Trabajo

1. **Login**: Usuario se autentica y obtiene token JWT
2. **Crear Orden**: Mesero crea orden para una mesa
3. **Agregar Items**: Se agregan productos a la orden
4. **Calcular Total**: Sistema calcula subtotal, impuestos y total
5. **Actualizar Stock**: Stock de productos se reduce automáticamente
6. **Pagar**: Orden se marca como pagada
7. **Liberar Mesa**: Mesa queda disponible nuevamente

## 🛠️ Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **PostgreSQL** - Base de datos relacional
- **Pydantic** - Validación de datos
- **JWT** - Autenticación basada en tokens
- **Bcrypt** - Hash de contraseñas

## 📄 Licencia

MIT

