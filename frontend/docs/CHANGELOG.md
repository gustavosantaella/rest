# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

## [1.3.0] - 2024-11-03

### ⚙️ Módulo de Configuración del Negocio (NUEVO)
- **Información Legal y Administrativa**
  - Nombre comercial del negocio
  - Razón social (nombre legal)
  - RIF/NIT/Tax ID (identificación fiscal)
  - Datos de contacto (teléfono, email, dirección)
  - Configuración fiscal (tasa de impuesto, moneda)
  - Logo del negocio (URL)
  
- **Gestión de Socios**
  - Agregar socios del negocio (solo usuarios Admin)
  - Porcentaje de participación por socio
  - Validación automática (debe sumar 100%)
  - Monto de inversión de cada socio
  - Estado activo/inactivo
  - Fecha de ingreso
  - Notas adicionales
  
- **Características**:
  - Solo Admin puede acceder
  - Validación en tiempo real de porcentajes
  - Barra de progreso visual por socio
  - Cálculo automático de participación total
  - Alerta si no suma 100%
  - Muestra % disponible al agregar socio
  
- **Monedas Soportadas**:
  - USD (Dólar)
  - EUR (Euro)
  - VES (Bolívar Venezolano)
  - COP (Peso Colombiano)
  - MXN (Peso Mexicano)
  - ARS (Peso Argentino)

### 👨‍🍳 Rol Chef Agregado
- Nuevo rol: **Chef** (Cocinero)
- Permisos: Ver y actualizar órdenes de cocina
- Badge color naranja 🟠
- Manager puede gestionar usuarios Chef
- Total de roles: **5**

---

## [1.2.0] - 2024-11-03

### 🔄 Sistema de Loading Global (NUEVO)
- **Loading automático** en todas las peticiones HTTP
  - Interceptor HTTP que detecta peticiones
  - Contador inteligente para peticiones simultáneas
  - Overlay de pantalla completa con spinner
  - Mensaje "Procesando..."
  - Animaciones suaves de entrada/salida
  
- **Componente LoadingSpinner reutilizable**
  - 4 tamaños: sm, md, lg, xl
  - Modo overlay o inline
  - Mensajes personalizables
  - Estilos customizables
  - Fácil de usar en cualquier componente
  
- **LoadingService** para control manual
  - Métodos show() y hide()
  - Observable loading$ para suscripciones
  - Contador de peticiones activas

- **LoadingButton** componente adicional
  - Botones con spinner integrado
  - Previene doble-click automáticamente
  - Texto personalizable durante carga
  
- **Beneficios**:
  - Usuario siempre sabe cuando el sistema está procesando
  - Previene clicks múltiples en botones
  - Mejor percepción de performance
  - UX más profesional
  - Sin código adicional en el 99% de los casos

### 🍽️ Módulo de Menú (NUEVO)
- **Gestión completa de platillos del restaurante**
  - Crear platillos con nombre, descripción y precio
  - Categorías del menú (Entradas, Platos Fuertes, Postres, etc.)
  - Tiempo de preparación por platillo
  - Imágenes de platillos (URL)
  - Platillos destacados ⭐
  - Sistema de disponibilidad (disponible/agotado)
  
- **Sistema de Ingredientes**
  - Asociar ingredientes del inventario a cada platillo
  - Definir cantidades necesarias por porción
  - Visualización de ingredientes en tarjetas
  - Base para reducción automática de stock (futuro)

### 🧾 Órdenes Mejoradas
- **Toggle Menú/Inventario**: Seleccionar entre platillos del menú o productos del inventario
- **Platillos destacados** mostrados primero en órdenes
- **Agrupación por tipo** (Destacados vs Menú Completo)
- Mejor organización de selección de items

### 🔐 Autenticación Mejorada
- **Sesión persistente**: Ya no se pierde sesión al recargar (F5)
- **Manejo inteligente de errores**: Solo logout si token es realmente inválido
- **Return URL**: Redirige a donde estabas después del login
- **Error logging**: Mensajes claros en consola para debugging
- **Interceptor mejorado**: Detecta automáticamente tokens inválidos

### 📚 Documentación
- `FEATURES_COMPLETE.md` - Resumen completo del sistema
- `MENU_DOCUMENTATION.md` - Guía del módulo de menú
- `AUTHENTICATION_FIX.md` - Solución de problemas de sesión
- Actualización de todos los READMEs

---

## [1.1.0] - 2024-11-03

### ✨ Sistema de Tooltips Informativos
- **60+ tooltips** en todos los campos de formularios
- **Directiva reutilizable** `appTooltip`
- Funciona con **hover y focus** (accesible con teclado)
- Diseño moderno con **gradiente púrpura**
- **4 posiciones** configurables (top, bottom, left, right)
- Animaciones suaves de entrada/salida
- Documentación completa en README_TOOLTIP.md

### 📦 Componentes con Tooltips
- **Login**: Credenciales y ayuda para primer acceso
- **Inventario**: Todos los campos de productos y categorías explicados
- **Menú**: Campos de platillos e ingredientes explicados 🆕
- **Mesas**: Configuración de mesas explicada
- **Órdenes**: Guía para crear órdenes paso a paso
- **Usuarios**: Roles y permisos explicados claramente

### 🎨 Mejoras de UX
- Usuarios entienden mejor qué ingresar en cada campo
- Reducción significativa de errores de entrada de datos
- Onboarding más rápido para nuevos usuarios
- Menos necesidad de soporte y documentación externa
- Sistema más profesional y pulido

---

## [1.0.0] - 2024-11-02

### ✨ Lanzamiento Inicial
- **Autenticación JWT** con roles y permisos
- **Dashboard** con estadísticas en tiempo real
- **Gestión completa de inventario**
  - Productos con múltiples unidades de medida
  - Categorías personalizables
  - Control de stock automático
  - Alertas de stock bajo
  - Precios de compra y venta
- **Sistema de mesas** con estados (Disponible, Ocupada, Reservada, Limpieza)
- **Gestión de órdenes y cuentas**
  - Cálculo automático de totales e impuestos
  - Múltiples métodos de pago
  - Estados de orden
  - Reducción automática de stock
- **Administración de usuarios**
  - 4 roles: Admin, Manager, Waiter, Cashier
  - Permisos por rol
  - Activar/Desactivar usuarios
- **Diseño responsive** con Tailwind CSS
- **Backend FastAPI** con PostgreSQL
- **Frontend Angular 17** standalone components

---

## 📊 Métricas del Proyecto

- **Versiones**: 1.2.0 (actual)
- **Líneas de código**: ~5,500+
- **Archivos creados**: 60+
- **Endpoints API**: 40+
- **Componentes**: 9
- **Tooltips**: 60+
- **Documentación**: 10+ archivos

---

## 🙏 Agradecimientos

Gracias por usar este sistema. Esperamos que facilite la gestión de tu negocio.

Para reportar bugs o sugerir mejoras, por favor contacta al equipo de desarrollo.


