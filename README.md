# 🍽️ Sistema de Gestión para Restaurante/Kiosko

Sistema completo de gestión para restaurantes, kioskos y locales comerciales. Desarrollado con **FastAPI** (backend) y **Angular 19** (frontend).

## ✨ Características Principales

### 📦 Gestión de Inventario
- Control de productos con categorías
- Múltiples unidades de medida (unidad, gramo, kg, ml, litro)
- Precios de compra y venta
- Alertas de stock bajo
- Imágenes de productos
- Control de visibilidad en catálogo

### 📖 Gestión de Menú
- Platillos con ingredientes del inventario
- Categorías personalizables
- Platillos destacados
- Tiempo de preparación
- Imágenes de platillos
- Disponibilidad en tiempo real

### 🪑 Gestión de Mesas
- Estados: Disponible, Ocupada, Reservada, Limpieza
- Capacidad y ubicación
- Actualización automática cada 10 segundos
- Cambio rápido de estado

### 🧾 Gestión de Órdenes
- Items del menú o inventario en la misma orden
- Sistema de pagos flexible:
  - Pagos parciales
  - Pagos mixtos (múltiples métodos)
  - Pago posterior (orden sin pago)
- Datos del cliente opcionales
- Estados: Pendiente, Preparando, Completado, Cancelado
- Edición de órdenes activas
- Historial completo de pagos

### 👥 Gestión de Usuarios
- Roles: Admin, Manager, Waiter, Cashier, Chef
- Permisos basados en roles
- Autenticación con JWT
- Sesión persistente

### ⚙️ Configuración del Negocio
- Información del local (nombre, RIF, contacto)
- Gestión de socios con % de participación
- Métodos de pago personalizables:
  - Pago Móvil (teléfono, DNI, banco)
  - Transferencia Bancaria (cuenta, titular, banco)
  - Efectivo, Bolívares, Dólares, Euros
- Slug personalizado para catálogo público
- **Código QR descargable** para compartir catálogo

### 🌐 Catálogo Público
- Acceso sin autenticación
- URL personalizada: `/catalog/{slug-negocio}`
- Vista de menú organizado por categorías
- Vista de productos disponibles
- Modal de detalle con ingredientes
- Responsive (móvil, tablet, desktop)
- Ideal para QR en mesas o redes sociales

### 📸 Gestión de Imágenes
- Subida de archivos (JPG, PNG, GIF, WEBP)
- URLs externas
- Máximo 5MB por archivo
- Almacenamiento en servidor
- Preview en tiempo real

## 🏗️ Estructura del Proyecto

```
ecommerce/
├── backend/                 # API con FastAPI
│   ├── app/                 # Código fuente
│   │   ├── models/          # Modelos SQLAlchemy
│   │   ├── schemas/         # Schemas Pydantic
│   │   ├── routers/         # Endpoints API
│   │   └── utils/           # Utilidades
│   ├── db/
│   │   └── migrations/      # ✨ Scripts de migración
│   ├── docs/                # ✨ Documentación backend
│   ├── uploads/             # Archivos subidos
│   └── requirements.txt     # Dependencias Python
│
└── frontend/                # App con Angular
    ├── src/app/
    │   ├── core/            # Servicios, guards, models
    │   ├── features/        # Componentes de páginas
    │   └── shared/          # Componentes reutilizables
    └── docs/                # ✨ Documentación frontend
```

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

### Backend

```bash
cd backend

# Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
# DATABASE_URL=postgresql://user:pass@localhost/dbname
# SECRET_KEY=tu_clave_secreta

# Ejecutar migraciones (ver backend/db/migrations/README.md)
.venv\Scripts\python.exe db/migrations/migrate_add_profile_fields.py
# ... ejecutar todas en orden

# Iniciar servidor
python run.py
```

Backend disponible en: http://localhost:8000

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
ng serve
```

Frontend disponible en: http://localhost:4200

### Credenciales por Defecto

```
Email: admin@admin.admin
Password: 123456.Ab!
```

⚠️ **Cambia estas credenciales en producción**

## 📚 Documentación

### Backend
- [README Backend](backend/docs/README.md) - Guía completa del backend
- [Guía de Migraciones](backend/db/migrations/README.md) - Cómo ejecutar migraciones
- [Sistema de Pagos](backend/docs/PAYMENT_METHODS_COMPLETE.md) - Documentación de pagos
- [Troubleshooting](backend/docs/TROUBLESHOOTING.md) - Solución de problemas

### Frontend
- [README Frontend](frontend/docs/README.md) - Guía completa del frontend
- [Sistema de Loading](frontend/docs/LOADING_SYSTEM.md) - Loading global
- [Tooltips](frontend/docs/README_TOOLTIP.md) - Sistema de tooltips
- [Changelog](frontend/docs/CHANGELOG.md) - Historial de cambios

## 🎯 Roles y Permisos

| Rol      | Dashboard | Inventario | Menú | Mesas | Órdenes | Usuarios | Config | Perfil |
|----------|-----------|------------|------|-------|---------|----------|--------|--------|
| Admin    | ✅        | ✅         | ✅   | ✅    | ✅      | ✅       | ✅     | ✅     |
| Manager  | ✅        | ✅         | ✅   | ✅    | ✅      | ✅       | ✅     | ✅     |
| Waiter   | ✅        | ❌         | ❌   | ✅    | ✅      | ❌       | ❌     | ✅     |
| Cashier  | ✅        | ❌         | ❌   | ❌    | ✅      | ❌       | ❌     | ✅     |
| Chef     | ✅        | ❌         | ❌   | ❌    | ✅(ver) | ❌       | ❌     | ✅     |

## 🔄 Flujo de Trabajo Típico

### 1. Configuración Inicial (Admin)
```
1. Login → Dashboard
2. Configuración → Negocio
   - Nombre del local
   - Información de contacto
   - Slug para catálogo público
   - Descargar QR
3. Configuración → Métodos de Pago
   - Configurar Pago Móvil, Transferencias, etc.
```

### 2. Preparación del Inventario
```
1. Inventario → Categorías
   - Crear categorías (Bebidas, Comidas, etc.)
2. Inventario → Productos
   - Agregar productos
   - Subir imágenes
   - Configurar stock y precios
   - Marcar "Mostrar en catálogo" si aplica
```

### 3. Configuración del Menú
```
1. Menú → Categorías
   - Crear categorías (Entradas, Platos Fuertes, Postres)
2. Menú → Platillos
   - Crear platillos
   - Asignar ingredientes del inventario
   - Subir imágenes
   - Marcar como destacados
   - Configurar tiempo de preparación
```

### 4. Operación Diaria
```
1. Mesas → Verificar disponibilidad
2. Órdenes → Nueva Orden
   - Seleccionar mesa
   - Agregar items (menú o inventario)
   - Registrar pagos (opcional)
3. Ver estado en Dashboard
4. Actualizar estado de órdenes
5. Procesar pagos pendientes
```

## 🌐 URLs del Sistema

### Administración
- Dashboard: http://localhost:4200/dashboard
- Login: http://localhost:4200/login

### Catálogo Público
- Formato: http://localhost:4200/catalog/{slug-negocio}
- Ejemplo: http://localhost:4200/catalog/tasca-el-abuelo

### API
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## 🐛 Reportar Problemas

Si encuentras algún bug o tienes sugerencias:
1. Verifica `backend/docs/TROUBLESHOOTING.md`
2. Revisa `frontend/docs/` para fixes conocidos
3. Revisa los logs del servidor

## 📦 Dependencias Principales

### Backend
- FastAPI - Framework web
- SQLAlchemy - ORM
- PostgreSQL - Base de datos
- JWT - Autenticación
- QRCode - Generación de códigos QR

### Frontend
- Angular 19 - Framework SPA
- Tailwind CSS - Estilos
- RxJS - Programación reactiva
- TypeScript - Tipado estático

## 📄 Licencia

Este proyecto es un sistema de gestión privado para uso interno.

---

**🎉 ¡Listo para gestionar tu negocio de forma profesional!**
