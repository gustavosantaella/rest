# 📁 Estructura del Proyecto

Documentación completa de la organización del sistema de gestión.

## 🏗️ Arquitectura General

```
ecommerce/
├── backend/              # API REST con FastAPI
├── frontend/             # SPA con Angular 19
└── README.md             # Documentación principal
```

---

## 🔧 Backend - FastAPI

```
backend/
│
├── app/                              # Aplicación principal
│   ├── __init__.py
│   ├── main.py                       # ⭐ Punto de entrada de FastAPI
│   ├── config.py                     # Configuración (DATABASE_URL, SECRET_KEY)
│   ├── database.py                   # Conexión a PostgreSQL
│   │
│   ├── models/                       # 💾 Modelos SQLAlchemy (DB)
│   │   ├── __init__.py
│   │   ├── user.py                   # Usuarios y roles
│   │   ├── product.py                # Productos y categorías
│   │   ├── menu.py                   # Menú y categorías
│   │   ├── menu_ingredient.py        # Ingredientes de platillos
│   │   ├── table.py                  # Mesas del restaurante
│   │   ├── order.py                  # Órdenes y items
│   │   ├── order_payment.py          # Pagos de órdenes
│   │   ├── payment_method.py         # Métodos de pago
│   │   └── configuration.py          # Configuración del negocio
│   │
│   ├── schemas/                      # 📋 Schemas Pydantic (Validación)
│   │   ├── __init__.py
│   │   ├── user.py                   # UserCreate, UserResponse, Token
│   │   ├── product.py                # ProductCreate, ProductResponse
│   │   ├── menu.py                   # MenuItemCreate, MenuItemResponse
│   │   ├── table.py                  # TableCreate, TableResponse
│   │   ├── order.py                  # OrderCreate, OrderResponse
│   │   ├── order_payment.py          # OrderPaymentCreate
│   │   ├── payment_method.py         # PaymentMethodCreate
│   │   ├── configuration.py          # BusinessConfigurationCreate
│   │   ├── profile.py                # ProfileUpdate
│   │   └── menu_ingredient.py        # IngredientItem
│   │
│   ├── routers/                      # 🛣️ Endpoints de la API
│   │   ├── __init__.py
│   │   ├── auth.py                   # POST /login, GET /me
│   │   ├── users.py                  # CRUD de usuarios
│   │   ├── products.py               # CRUD de inventario
│   │   ├── menu.py                   # CRUD de menú
│   │   ├── tables.py                 # CRUD de mesas
│   │   ├── orders.py                 # CRUD de órdenes + pagos
│   │   ├── payment_methods.py        # CRUD de métodos de pago
│   │   ├── configuration.py          # Config del negocio + QR
│   │   ├── profile.py                # Perfil del usuario
│   │   ├── upload.py                 # Subida de imágenes
│   │   └── public.py                 # Catálogo público (sin auth)
│   │
│   └── utils/                        # 🔧 Utilidades
│       ├── __init__.py
│       ├── security.py               # Hashing, JWT, passwords
│       └── dependencies.py           # Dependencias de FastAPI
│
├── db/                               # 💽 Base de Datos
│   └── migrations/                   # Scripts de migración SQL
│       ├── README.md                 # Guía de migraciones
│       ├── migrate_add_profile_fields.py
│       ├── migrate_add_payment_methods.py
│       ├── migrate_add_customer_fields.py
│       ├── migrate_add_order_payments.py
│       ├── migrate_add_show_in_catalog.py
│       ├── migrate_fix_show_in_catalog_type.py
│       ├── migrate_add_image_url_to_products.py
│       └── migrate_add_slug_to_business.py
│
├── docs/                             # 📚 Documentación
│   ├── README.md                     # Guía del backend
│   ├── MIGRATION_GUIDE.md            # Guía de migraciones
│   ├── PAYMENT_METHODS_COMPLETE.md   # Sistema de pagos
│   ├── TROUBLESHOOTING.md            # Solución de problemas
│   ├── update_dependencies.bat       # Script de actualización
│   ├── update_dependencies.sh        # Script de actualización
│   ├── migrate_add_profile_fields.bat
│   └── migrate_add_profile_fields.sh
│
├── uploads/                          # 📁 Archivos subidos
│   └── images/                       # Imágenes de productos/menú
│
├── .env                              # 🔐 Variables de entorno (NO en git)
├── .gitignore
├── init_db.py                        # Script de inicialización de BD
├── requirements.txt                  # Dependencias Python
└── run.py                            # Script para iniciar servidor
```

---

## 🎨 Frontend - Angular

```
frontend/
│
├── src/
│   ├── app/
│   │   ├── app.component.ts          # ⭐ Componente raíz
│   │   ├── app.routes.ts             # ⭐ Configuración de rutas
│   │   │
│   │   ├── core/                     # 🎯 Lógica principal
│   │   │   ├── guards/
│   │   │   │   └── auth.guard.ts     # Protección de rutas
│   │   │   │
│   │   │   ├── interceptors/
│   │   │   │   ├── auth.interceptor.ts      # Agrega JWT automático
│   │   │   │   └── loading.interceptor.ts   # Loading automático
│   │   │   │
│   │   │   ├── models/               # 📋 Interfaces TypeScript
│   │   │   │   ├── user.model.ts
│   │   │   │   ├── product.model.ts
│   │   │   │   ├── menu.model.ts
│   │   │   │   ├── table.model.ts
│   │   │   │   ├── order.model.ts
│   │   │   │   ├── payment-method.model.ts
│   │   │   │   └── configuration.model.ts
│   │   │   │
│   │   │   └── services/             # 🔌 Servicios de API
│   │   │       ├── auth.service.ts          # Autenticación
│   │   │       ├── user.service.ts          # Usuarios
│   │   │       ├── product.service.ts       # Inventario
│   │   │       ├── menu.service.ts          # Menú
│   │   │       ├── table.service.ts         # Mesas
│   │   │       ├── order.service.ts         # Órdenes
│   │   │       ├── payment-method.service.ts
│   │   │       ├── configuration.service.ts
│   │   │       ├── profile.service.ts
│   │   │       ├── upload.service.ts        # Subida de imágenes
│   │   │       ├── public.service.ts        # Catálogo público
│   │   │       ├── loading.service.ts       # Estado de carga
│   │   │       └── notification.service.ts
│   │   │
│   │   ├── features/                 # 📄 Páginas/Componentes
│   │   │   ├── auth/
│   │   │   │   └── login/            # Página de login
│   │   │   ├── layout/               # Layout principal con sidebar
│   │   │   ├── dashboard/            # Panel de control
│   │   │   ├── inventory/            # Gestión de inventario
│   │   │   ├── menu/                 # Gestión de menú
│   │   │   ├── tables/               # Gestión de mesas
│   │   │   ├── orders/               # Gestión de órdenes
│   │   │   ├── users/                # Gestión de usuarios
│   │   │   ├── configuration/        # Configuración del negocio
│   │   │   ├── profile/              # Perfil del usuario
│   │   │   └── public-catalog/       # Catálogo público
│   │   │
│   │   └── shared/                   # 🔄 Compartido
│   │       ├── components/
│   │       │   ├── image-upload/     # Subida de imágenes
│   │       │   ├── global-loading/   # Loading global
│   │       │   ├── loading-spinner/  # Spinner
│   │       │   ├── loading-button/   # Botón con loading
│   │       │   └── debug-loading/    # Debug del loading
│   │       │
│   │       └── directives/
│   │           └── tooltip.directive.ts  # Tooltips de ayuda
│   │
│   ├── environments/                 # 🌍 Configuración por entorno
│   │   ├── environment.ts            # Desarrollo
│   │   └── environment.prod.ts       # Producción
│   │
│   ├── index.html                    # HTML principal
│   ├── main.ts                       # Bootstrap de Angular
│   └── styles.scss                   # Estilos globales + Tailwind
│
├── docs/                             # 📚 Documentación
│   ├── README.md                     # Guía del frontend
│   ├── AUTHENTICATION_FIX.md
│   ├── LOADING_SYSTEM.md
│   ├── PAYMENT_METHODS_IMPLEMENTATION.md
│   ├── CHANGELOG.md
│   └── ... otros archivos .md
│
├── angular.json                      # Configuración de Angular
├── package.json                      # Dependencias npm
├── tailwind.config.js                # Configuración de Tailwind
└── tsconfig.json                     # Configuración de TypeScript
```

---

## 🗄️ Modelos de Base de Datos

### Users (Usuarios)
```
- id, username, email, full_name
- hashed_password
- role (admin, manager, waiter, cashier, chef)
- dni, country (perfil)
- is_active
```

### Categories (Categorías de Inventario)
```
- id, name, description
```

### Products (Inventario)
```
- id, name, description, category_id
- unit_type (unit, weight_gram, weight_kg, volume_ml, volume_l, bulk)
- purchase_price, sale_price
- stock, min_stock
- show_in_catalog (boolean)
- image_url
```

### MenuCategories (Categorías de Menú)
```
- id, name, description
- display_order, is_active
```

### MenuItem (Platillos del Menú)
```
- id, name, description, category_id
- price, preparation_time
- is_available, is_featured
- image_url
- ingredients (relación con Products)
```

### Tables (Mesas)
```
- id, number, capacity, location
- status (available, occupied, reserved, cleaning)
```

### Orders (Órdenes)
```
- id, table_id (opcional)
- notes
- status (pending, preparing, completed, cancelled)
- payment_status (pending, partial, paid)
- customer_name, customer_email, customer_phone
- subtotal, tax, discount, total
- paid_at, created_at
```

### OrderItem (Items de Orden)
```
- id, order_id, product_id
- quantity, unit_price, notes
- subtotal
```

### PaymentMethod (Métodos de Pago)
```
- id, type, name, is_active
- phone, dni, bank, account_holder, account_number
  (campos opcionales según el tipo)
```

### OrderPayment (Pagos de Órdenes)
```
- id, order_id, payment_method_id
- amount, reference
- created_at
```

### BusinessConfiguration (Configuración)
```
- id, business_name, slug
- legal_name, rif
- phone, email, address
- tax_rate, currency
- logo_url
```

### Partner (Socios)
```
- id, business_config_id, user_id
- participation_percentage, investment_amount
- join_date, is_active, notes
```

---

## 🎯 Flujo de Datos

### Autenticación
```
Login → JWT Token → localStorage → authInterceptor → Backend
```

### Órdenes
```
1. Seleccionar mesa (opcional)
2. Agregar items del menú/inventario
3. Calcular total automático
4. Registrar pagos (opcional)
5. Crear orden
6. Backend:
   - Reduce stock de productos
   - Cambia estado de mesa a OCCUPIED
   - Calcula totales
   - Registra pagos
```

### Catálogo Público
```
Usuario → /catalog/{slug} → Backend público → Menú/Productos → Modal detalle
```

---

## 📦 Principales Dependencias

### Backend
```python
fastapi==0.104.1          # Framework web
sqlalchemy==2.0.23        # ORM
psycopg2-binary==2.9.9    # Driver PostgreSQL
pydantic==2.5.0           # Validación
python-jose==3.3.0        # JWT
passlib==1.7.4            # Hashing
bcrypt==4.0.1             # Passwords
qrcode==8.2               # Generación de QR
pillow==12.0.0            # Procesamiento de imágenes
```

### Frontend
```json
@angular/core: ^19.0.0
@angular/common: ^19.0.0
@angular/router: ^19.0.0
@angular/forms: ^19.0.0
tailwindcss: ^3.4.0
rxjs: ~7.8.0
typescript: ~5.6.0
```

---

## 🔐 Seguridad

### Backend
- ✅ Passwords hasheadas con bcrypt
- ✅ JWT con expiración (30 min por defecto)
- ✅ Dependencias de roles (get_current_active_admin, etc.)
- ✅ CORS configurado
- ✅ SQLAlchemy previene SQL injection

### Frontend
- ✅ Guards de ruta por rol
- ✅ Token en localStorage
- ✅ Interceptor automático para JWT
- ✅ Validación en formularios
- ✅ Manejo de errores 401/403

---

## 🚀 Scripts Disponibles

### Backend
```bash
python run.py                     # Iniciar servidor
python init_db.py                 # Inicializar BD
.venv/Scripts/python db/migrations/migrate_*.py  # Ejecutar migración
```

### Frontend
```bash
ng serve                          # Servidor desarrollo
ng build                          # Build producción
ng test                           # Tests unitarios
ng lint                           # Verificar código
```

---

## 📝 Convenciones de Código

### Backend (Python)
- **Nombres de archivos:** snake_case
- **Clases:** PascalCase
- **Funciones:** snake_case
- **Constantes:** UPPER_CASE

### Frontend (TypeScript)
- **Nombres de archivos:** kebab-case
- **Clases:** PascalCase
- **Funciones/Variables:** camelCase
- **Constantes:** UPPER_CASE
- **Interfaces:** PascalCase con `I` opcional

---

## 🔄 Ciclo de Vida de Componentes

### Angular Components
```typescript
1. constructor()         // Inyección de dependencias
2. ngOnInit()           // Inicialización, cargar datos
3. ngOnDestroy()        // Limpieza (intervals, subscriptions)
```

### FastAPI Endpoints
```python
1. Recibir request
2. Validar con schema (Pydantic)
3. Verificar autenticación/permisos
4. Procesar lógica de negocio
5. Retornar response (schema)
```

---

## 📊 Diagramas de Relaciones

### Órdenes
```
Order (1) ──── (N) OrderItem ──── (1) Product/MenuItem
Order (1) ──── (N) OrderPayment ──── (1) PaymentMethod
Order (N) ──── (1) Table
```

### Menú
```
MenuItem (N) ──── (1) MenuCategory
MenuItem (N) ──── (N) Product (ingredients)
```

### Configuración
```
BusinessConfiguration (1) ──── (N) Partner ──── (1) User
```

---

## 🌐 Endpoints Principales

### Públicos (sin autenticación)
```
POST /api/auth/login
GET  /api/public/{slug}/info
GET  /api/public/{slug}/menu
GET  /api/public/{slug}/products
GET  /api/public/{slug}/menu/{item_id}
```

### Privados (requieren JWT)
```
GET    /api/users/me
GET    /api/products
POST   /api/products
GET    /api/menu
POST   /api/menu
GET    /api/orders
POST   /api/orders
POST   /api/orders/{id}/payments
PUT    /api/orders/{id}/items
GET    /api/configuration
GET    /api/configuration/qr-code
POST   /api/upload/image
```

---

## 📱 Responsive Breakpoints

```scss
// Tailwind breakpoints
sm:  640px   // Tablets pequeñas
md:  768px   // Tablets
lg:  1024px  // Laptops
xl:  1280px  // Desktops
2xl: 1536px  // Pantallas grandes
```

---

## 🎨 Paleta de Colores

```css
Primary:   #3B82F6 (blue-500)
Success:   #10B981 (green-500)
Warning:   #F59E0B (yellow-500)
Danger:    #EF4444 (red-500)
Info:      #06B6D4 (cyan-500)
```

---

**📖 Ver READMEs individuales en `backend/docs/` y `frontend/docs/` para más detalles.**

