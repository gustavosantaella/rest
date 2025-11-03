# Sistema de Gestión para Restaurante/Kiosko

Sistema completo de gestión para restaurantes, kioskos y locales comerciales. Desarrollado con **FastAPI** (backend) y **Angular** (frontend).

## 🌟 Características Principales

### Backend (FastAPI + PostgreSQL)
- ✅ API REST completa
- ✅ Autenticación JWT con roles
- ✅ Base de datos PostgreSQL
- ✅ Gestión de inventario con múltiples unidades de medida
- ✅ **Menú del Restaurante** - Gestión de platillos y categorías
- ✅ Sistema de órdenes con cálculo automático
- ✅ Gestión de mesas y estados
- ✅ Control de usuarios y permisos (5 roles)
- ✅ **Configuración y Socios** - Información legal y gestión de socios (¡NUEVO!)

### Frontend (Angular + Tailwind)
- ✅ Interfaz moderna y responsive
- ✅ Dashboard con estadísticas
- ✅ Gestión completa de inventario
- ✅ **Menú Digital** - Catálogo de platillos con imágenes
- ✅ Sistema de órdenes intuitivo
- ✅ Control de mesas visual
- ✅ Administración de usuarios
- ✅ **Tooltips informativos** en todos los campos
- ✅ **Loaders automáticos** en todas las peticiones (¡NUEVO!)

## 📦 Características del Inventario

- **Múltiples Unidades de Medida:**
  - Por unidad
  - Por gramo / kilogramo
  - Por mililitro / litro
  - A granel

- **Control de Precios:**
  - Precio de compra
  - Precio de venta
  - Margen de ganancia

- **Alertas de Stock:**
  - Stock mínimo configurable
  - Alertas automáticas

## 🔐 Roles y Permisos

- **ADMIN**: Acceso total al sistema + Configuración del negocio
- **MANAGER**: Gestión de inventario, mesas y personal
- **WAITER**: Gestión de órdenes y mesas
- **CASHIER**: Procesamiento de pagos
- **CHEF**: Visualización de órdenes de cocina

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.8+
- Node.js 18+
- PostgreSQL 12+

### 1. Backend Setup

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Crear base de datos PostgreSQL
createdb restaurant_db

# Inicializar base de datos con usuario admin (opcional)
python init_db.py

# Ejecutar servidor
python run.py
```

Backend disponible en: `http://localhost:8000`
Documentación API: `http://localhost:8000/docs`

**Usuario administrador por defecto:**
- Usuario: `admin`
- Email: `admin@admin.admin`
- Password: `123456.Ab!`

### 2. Frontend Setup

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar
npm start
```

Frontend disponible en: `http://localhost:4200`

## 💡 Sistema de Tooltips

Todos los campos de formularios incluyen tooltips informativos que explican:
- **Qué ingresar** en cada campo
- **Formato esperado** y ejemplos
- **Cómo se usa** esa información en el sistema
- **Consejos** y mejores prácticas

**Uso**: Simplemente pasa el mouse (hover) o haz focus en cualquier campo para ver la ayuda contextual.

Ver más detalles en [README_TOOLTIP.md](frontend/README_TOOLTIP.md)

## 📁 Estructura del Proyecto

```
ecommerce/
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── schemas/           # Schemas Pydantic
│   │   ├── routers/           # Endpoints
│   │   ├── utils/             # Utilidades
│   │   ├── database.py
│   │   ├── config.py
│   │   └── main.py
│   ├── requirements.txt
│   └── README.md
│
└── frontend/                   # Aplicación Angular
    ├── src/
    │   ├── app/
    │   │   ├── core/          # Servicios y modelos
    │   │   └── features/      # Componentes
    │   ├── environments/
    │   └── styles.scss
    ├── angular.json
    ├── tailwind.config.js
    └── README.md
```

## 🔑 Credenciales de Acceso

Al iniciar el backend por primera vez, se crea automáticamente un usuario administrador:

- **Usuario:** `admin`
- **Email:** `admin@admin.admin`  
- **Password:** `123456.Ab!`
- **Rol:** Administrador

> ⚠️ **Importante:** Cambia esta contraseña después del primer inicio de sesión en producción.

## 🎯 Flujo de Trabajo

1. **Configuración Inicial:**
   - Iniciar sesión con usuario admin
   - **Configurar negocio y socios** (Configuración) 🆕
   - Crear categorías de productos
   - Agregar productos al inventario
   - Crear categorías del menú
   - Crear platillos del menú
   - Configurar mesas del local
   - Crear usuarios del personal

2. **Operación Diaria:**
   - Mesero toma orden en una mesa
   - Sistema calcula automáticamente totales
   - Stock se reduce automáticamente
   - Cajero procesa el pago
   - Mesa queda disponible

3. **Administración:**
   - Monitorear stock bajo
   - Ver estadísticas de ventas
   - Gestionar personal
   - Actualizar precios

## 🛠️ Tecnologías

### Backend
- FastAPI - Framework web moderno
- SQLAlchemy - ORM
- PostgreSQL - Base de datos
- Pydantic - Validación de datos
- JWT - Autenticación
- Bcrypt - Encriptación

### Frontend
- Angular 17 - Framework
- Tailwind CSS 3 - Estilos
- RxJS - Programación reactiva
- TypeScript - Lenguaje

## 📚 Documentación Adicional

- [Backend README](./backend/README.md) - Documentación detallada del backend
- [Frontend README](./frontend/README.md) - Documentación detallada del frontend
- [Menú Documentation](./MENU_DOCUMENTATION.md) - Guía completa del módulo de menú
- [Configuration Module](./CONFIGURATION_MODULE.md) - Módulo de configuración y socios 🆕
- [Roles Documentation](./ROLES_DOCUMENTATION.md) - Sistema de 5 roles
- [API Docs](http://localhost:8000/docs) - Documentación interactiva de la API

## 🔄 API Endpoints

### Autenticación
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Login

### Productos (Inventario)
- `GET /api/products/` - Listar productos
- `POST /api/products/` - Crear producto
- `PUT /api/products/{id}` - Actualizar producto
- `DELETE /api/products/{id}` - Eliminar producto

### Menú (Platillos) 🆕
- `GET /api/menu/items` - Listar platillos
- `POST /api/menu/items` - Crear platillo
- `GET /api/menu/items/featured` - Platillos destacados
- `PUT /api/menu/items/{id}` - Actualizar platillo
- `DELETE /api/menu/items/{id}` - Eliminar platillo

### Mesas
- `GET /api/tables/` - Listar mesas
- `POST /api/tables/` - Crear mesa
- `PUT /api/tables/{id}` - Actualizar mesa

### Órdenes
- `GET /api/orders/` - Listar órdenes
- `POST /api/orders/` - Crear orden
- `PUT /api/orders/{id}` - Actualizar orden

### Usuarios
- `GET /api/users/` - Listar usuarios (admin)
- `GET /api/users/me` - Usuario actual
- `PUT /api/users/{id}` - Actualizar usuario

### Configuración 🆕
- `GET /api/configuration` - Obtener configuración del negocio
- `POST /api/configuration` - Crear configuración
- `PUT /api/configuration` - Actualizar configuración
- `GET /api/configuration/partners` - Listar socios
- `POST /api/configuration/partners` - Agregar socio
- `PUT /api/configuration/partners/{id}` - Actualizar socio
- `DELETE /api/configuration/partners/{id}` - Eliminar socio

## 🎨 Capturas de Pantalla

*(Las capturas de pantalla irían aquí)*

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Notas

- El sistema calcula automáticamente un IVA del 16% (configurable)
- Las contraseñas se encriptan con Bcrypt
- Los tokens JWT expiran después de 30 minutos
- El sistema soporta múltiples monedas (configuración futura)

## 🐛 Reporte de Bugs

Si encuentras algún bug, por favor abre un issue en GitHub.

## 📄 Licencia

MIT License - Ver archivo LICENSE para más detalles

## 👥 Autores

Sistema desarrollado para la gestión eficiente de locales comerciales.

---

**¡Gracias por usar nuestro sistema!** 🚀

