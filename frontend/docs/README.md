# Frontend - Sistema de Gestión para Restaurante/Kiosko

Aplicación web desarrollada con Angular 19 y Tailwind CSS para la gestión integral de restaurantes, kioskos y locales comerciales.

## 🚀 Tecnologías

- **Framework:** Angular 19 (Standalone Components)
- **Estilos:** Tailwind CSS
- **HTTP:** HttpClient con interceptores
- **Formularios:** Reactive Forms
- **Routing:** Angular Router con lazy loading
- **Estado:** RxJS + BehaviorSubject
- **Autenticación:** JWT

## 📁 Estructura del Proyecto

```
frontend/src/app/
├── core/                    # Lógica principal
│   ├── guards/              # Guards de rutas (authGuard)
│   ├── interceptors/        # HTTP interceptors (auth, loading)
│   ├── models/              # Interfaces TypeScript
│   └── services/            # Servicios de API
├── features/                # Componentes de características
│   ├── auth/                # Login y autenticación
│   ├── dashboard/           # Panel principal
│   ├── inventory/           # Gestión de inventario
│   ├── menu/                # Gestión de menú
│   ├── tables/              # Gestión de mesas
│   ├── orders/              # Gestión de órdenes
│   ├── users/               # Gestión de usuarios
│   ├── configuration/       # Configuración del negocio
│   ├── profile/             # Perfil del usuario
│   └── public-catalog/      # Catálogo público
├── shared/                  # Componentes y directivas compartidas
│   ├── components/          # Componentes reutilizables
│   │   ├── image-upload/    # Subida de imágenes
│   │   ├── global-loading/  # Indicador de carga global
│   │   └── ...
│   └── directives/          # Directivas reutilizables
│       └── tooltip.directive.ts
└── app.routes.ts            # Configuración de rutas
```

## ⚙️ Instalación

### 1. Instalar dependencias

```bash
npm install
```

### 2. Configurar entorno

Edita `src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

### 3. Iniciar servidor de desarrollo

```bash
ng serve
# o
npm start
```

La aplicación estará disponible en: `http://localhost:4200`

## 🎨 Características Principales

### Autenticación y Autorización
- Login con JWT
- Guardado de sesión persistente
- Guards de ruta basados en roles
- Interceptor de autenticación automática

### Sistema de Carga Global
- Loading automático en todas las peticiones HTTP
- Spinner global sin configuración manual
- Botones de carga integrados

### Gestión de Inventario
- CRUD completo de productos
- Categorización
- Control de stock con alertas
- Múltiples tipos de unidad
- Subida de imágenes (URL o archivo)
- Flag "Mostrar en catálogo"

### Gestión de Menú
- CRUD de platillos
- Categorías personalizables
- Ingredientes del inventario
- Platillos destacados
- Tiempo de preparación
- Subida de imágenes

### Gestión de Mesas
- Estados: Disponible, Ocupada, Reservada, Limpieza
- Actualización automática cada 10 segundos
- Cambio de estado en tiempo real

### Gestión de Órdenes
- Selección de items del menú o inventario
- Cálculo automático de totales
- Pagos múltiples/mixtos
- Datos opcionales del cliente
- Edición de órdenes
- Cambio de estados
- Procesamiento de pagos posterior

### Configuración del Negocio
- Información del local
- Gestión de socios
- Métodos de pago configurables
- Slug para catálogo público
- Descarga de código QR

### Perfil de Usuario
- Actualización de datos personales
- Cambio seguro de contraseña
- Validación de contraseña actual

### Catálogo Público
- Acceso sin autenticación
- URL personalizada: `/catalog/{slug}`
- Vista de menú y productos
- Modal de detalle con ingredientes
- Responsive

## 🎯 Componentes Reutilizables

### ImageUploadComponent
Componente para subir imágenes con dos modos:
- URL externa
- Archivo local (sube al servidor)

### TooltipDirective
```html
<input 
  appTooltip="Texto de ayuda"
  tooltipPosition="top"
/>
```

### GlobalLoadingComponent
Loading automático en todas las peticiones HTTP.

## 🛠️ Comandos Útiles

### Desarrollo

```bash
# Iniciar servidor de desarrollo
ng serve

# Iniciar con puerto específico
ng serve --port 4300

# Abrir automáticamente en navegador
ng serve --open
```

### Build

```bash
# Build de producción
ng build --configuration production

# Build de desarrollo
ng build
```

### Testing

```bash
# Ejecutar tests unitarios
ng test

# Ejecutar tests e2e
ng e2e
```

### Linting

```bash
# Verificar código
ng lint

# Aplicar correcciones automáticas
ng lint --fix
```

## 🎨 Tailwind CSS

Configurado con clases personalizadas:

```css
/* Principales clases de utilidad */
.btn-primary      /* Botón primario */
.btn-secondary    /* Botón secundario */
.btn-danger       /* Botón de peligro */
.input-field      /* Campo de entrada */
.card             /* Tarjeta contenedora */
.badge            /* Insignia/etiqueta */
```

Ver `src/styles.scss` para la configuración completa.

## 🔒 Seguridad

- Tokens JWT almacenados en localStorage
- Interceptor automático para agregar Authorization header
- Guards de ruta para proteger páginas
- Validación de roles en el frontend
- Manejo de errores 401/403

## 📱 Responsive Design

La aplicación está completamente optimizada para:
- 📱 Móviles (320px+)
- 📱 Tablets (768px+)
- 💻 Desktop (1024px+)
- 🖥️ Pantallas grandes (1920px+)

## 🌐 Rutas Principales

### Públicas
- `/login` - Página de login
- `/catalog/:slug` - Catálogo público

### Protegidas (requieren autenticación)
- `/dashboard` - Panel principal
- `/inventory` - Inventario
- `/menu` - Menú
- `/tables` - Mesas
- `/orders` - Órdenes
- `/users` - Usuarios (solo admin)
- `/configuration/business` - Configuración (solo admin)
- `/profile` - Perfil del usuario

## 📖 Documentación Adicional

Ver archivos en esta carpeta `docs/`:
- `AUTHENTICATION_FIX.md` - Correcciones de autenticación
- `LOADING_SYSTEM.md` - Sistema de carga global
- `PAYMENT_METHODS_IMPLEMENTATION.md` - Sistema de pagos
- `CHANGELOG.md` - Registro de cambios

## 🐛 Troubleshooting

### Problema: Error al compilar

```bash
# Limpiar caché y reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Problema: CORS error

Verifica que el backend tenga configurado:
```python
allow_origins=["http://localhost:4200"]
```

### Problema: 401 Unauthorized

- Verifica que el token sea válido
- Revisa que el interceptor esté configurado
- Confirma que el backend esté corriendo

## 💡 Tips de Desarrollo

1. **Usa Angular DevTools** para debuggear componentes
2. **Usa Tailwind IntelliSense** en VS Code para autocompletado
3. **Revisa la consola** para errores de compilación
4. **Usa lazy loading** para mejorar performance
5. **Standalone components** para mejor modularidad

## 🚀 Deploy

### Build para producción

```bash
ng build --configuration production
```

Los archivos compilados estarán en `dist/frontend/`

### Variables de entorno

Edita `src/environments/environment.prod.ts`:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://tu-dominio.com/api'
};
```

## 📝 Contribuir

Para agregar nuevas características:

1. Crea el componente en `features/`
2. Crea el servicio en `core/services/`
3. Crea el modelo en `core/models/`
4. Agrega la ruta en `app.routes.ts`
5. Documenta los cambios

## 🎉 Características Especiales

- ✅ **Auto-guardado de sesión** - Persiste login en refresh
- ✅ **Loading global automático** - Sin configuración manual
- ✅ **Tooltips en todos los campos** - Ayuda contextual
- ✅ **Responsive completo** - Funciona en todos los dispositivos
- ✅ **Catálogo público** - Sin autenticación requerida
- ✅ **Código QR** - Para compartir el catálogo
- ✅ **Sistema de pagos flexible** - Pagos parciales y mixtos
- ✅ **Actualización automática** - Mesas se actualizan cada 10s
- ✅ **Edición de órdenes** - Modificar items y estados

---

**Desarrollado con ❤️ usando Angular y Tailwind CSS**
