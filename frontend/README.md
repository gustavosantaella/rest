# Frontend - Sistema de Gestión para Restaurante/Kiosko

Aplicación Angular con Tailwind CSS para gestión completa de restaurantes, kioskos y locales comerciales.

## 🚀 Características

- ✅ **Login y Autenticación** con JWT
- 📊 **Dashboard Intuitivo** con estadísticas en tiempo real
- 📦 **Gestión de Inventario**
  - Productos con múltiples unidades de medida
  - Categorías personalizables
  - Alertas de stock bajo
  - Precios de compra y venta
- 🍽️ **Gestión de Mesas**
  - Estados: Disponible, Ocupada, Reservada, Limpieza
  - Asignación dinámica
  - Vista tipo tarjetas
- 🧾 **Gestión de Órdenes**
  - Crear órdenes con múltiples items
  - Cálculo automático de totales e impuestos
  - Múltiples métodos de pago
  - Seguimiento de estados
- 👥 **Gestión de Usuarios**
  - Roles: Admin, Manager, Waiter, Cashier
  - Permisos personalizados
  - Activar/Desactivar usuarios
- 🎨 **Diseño Moderno** con Tailwind CSS
- 📱 **Responsive Design** - Compatible con móviles y tablets

## 📋 Requisitos

- Node.js 18+
- Angular CLI 17+

## 🔧 Instalación

1. **Instalar dependencias:**
```bash
npm install
```

2. **Configurar API URL:**

Editar `src/environments/environment.ts`:
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

## ▶️ Ejecutar en Desarrollo

```bash
npm start
```

La aplicación estará disponible en: `http://localhost:4200`

## 🏗️ Compilar para Producción

```bash
npm run build
```

Los archivos compilados estarán en el directorio `dist/`.

## 📚 Estructura del Proyecto

```
frontend/
├── src/
│   ├── app/
│   │   ├── core/                    # Funcionalidad core
│   │   │   ├── models/             # Interfaces y tipos
│   │   │   ├── services/           # Servicios HTTP
│   │   │   ├── guards/             # Guards de autenticación
│   │   │   └── interceptors/       # HTTP Interceptors
│   │   ├── features/                # Módulos funcionales
│   │   │   ├── auth/               # Login
│   │   │   ├── layout/             # Layout principal
│   │   │   ├── dashboard/          # Dashboard
│   │   │   ├── inventory/          # Gestión de inventario
│   │   │   ├── tables/             # Gestión de mesas
│   │   │   ├── orders/             # Gestión de órdenes
│   │   │   └── users/              # Gestión de usuarios
│   │   ├── app.component.ts
│   │   └── app.routes.ts
│   ├── environments/                # Configuración de entornos
│   ├── styles.scss                  # Estilos globales
│   └── index.html
├── angular.json
├── tailwind.config.js               # Configuración Tailwind
├── package.json
└── README.md
```

## 🎨 Tecnologías

- **Angular 17** - Framework principal
- **Tailwind CSS 3** - Estilos y diseño
- **RxJS** - Programación reactiva
- **TypeScript** - Lenguaje de programación

## 🔐 Roles y Permisos

### Administrador
- Acceso total al sistema
- Gestión de usuarios
- Todas las funcionalidades

### Gerente
- Gestión de inventario
- Gestión de mesas
- Gestión de usuarios (limitada)
- Ver reportes

### Mesero
- Crear y gestionar órdenes
- Actualizar estados de mesas
- Ver inventario

### Cajero
- Procesar pagos
- Ver órdenes
- Cerrar cuentas

## 🚀 Flujo de Usuario

1. **Login** → Usuario ingresa credenciales
2. **Dashboard** → Vista general del sistema
3. **Gestionar Inventario** → Admin/Manager agregan productos
4. **Crear Orden** → Mesero toma pedido
5. **Agregar Items** → Seleccionar productos y cantidades
6. **Procesar Pago** → Cajero cobra la cuenta
7. **Liberar Mesa** → Mesa vuelve a estado disponible

## 📱 Responsive Breakpoints

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

## 🎨 Personalización

### Colores

Editar `tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Personaliza tus colores aquí
      }
    }
  }
}
```

### Estilos Globales

Editar `src/styles.scss` para agregar estilos personalizados.

## 🐛 Solución de Problemas

### Error de CORS
Asegúrate de que el backend esté configurado para aceptar peticiones desde `http://localhost:4200`.

### Token Expirado
El token JWT expira después de 30 minutos. Vuelve a iniciar sesión.

### Datos No Se Cargan
Verifica que el backend esté corriendo y la URL de la API sea correcta.

## 📄 Licencia

MIT

