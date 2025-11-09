# Módulo de Cierre de Caja

## 📋 Descripción

El módulo de **Cierre de Caja** proporciona un resumen completo y detallado de todas las ventas y transacciones del día. Es una herramienta esencial para el control diario de las operaciones del negocio.

## 🎯 Características Principales

### 📊 Resumen Financiero
- **Total Ventas del Día**: Suma de todas las órdenes pagadas
- **Total Órdenes**: Cantidad total de órdenes generadas
- **Ticket Promedio**: Monto promedio por orden
- **Órdenes Completadas**: Cantidad de órdenes finalizadas exitosamente
- **Órdenes Canceladas**: Cantidad de órdenes canceladas

### 💳 Desglose por Métodos de Pago
- Vista detallada de cada método de pago utilizado
- Cantidad de transacciones por método
- Monto total recaudado por cada método
- Ordenados de mayor a menor por monto

### 📦 Productos Más Vendidos (Top 10)
- Listado de los 10 productos con mayor venta del día
- Cantidad vendida de cada producto
- Total generado por producto
- Ideal para análisis de inventario y demanda

### 📋 Listado Completo de Órdenes
- Todas las órdenes del día con detalle
- Hora de creación
- Estado de la orden
- Estado del pago
- Monto total

### 🖨️ Funcionalidades de Exportación
- **Imprimir Reporte**: Formato optimizado para impresión
- **Exportar CSV**: Descarga de datos en formato CSV para Excel
- **Selector de Fecha**: Consultar cierres de días anteriores

## 📱 Interfaz de Usuario

### Tarjetas de Resumen (4 Principales)
1. **Total Ventas** 💚 (Verde) - Ingresos totales del día
2. **Total Órdenes** 💙 (Azul) - Cantidad de órdenes
3. **Ticket Promedio** 💜 (Morado) - Promedio de gasto
4. **Órdenes Completadas** 💚 (Esmeralda) - Órdenes finalizadas

### Secciones Adicionales
- **Desglose por Métodos de Pago**: Tarjetas con iconos y montos
- **Productos Más Vendidos**: Tabla ordenada por cantidad
- **Listado de Órdenes**: Tabla completa con todos los detalles

## 🚀 Cómo Usar

### Acceder al Módulo

1. Inicia sesión en el sistema
2. En el menú lateral, haz clic en **"Cierre de Caja"** 🧮
3. Por defecto se muestra el día actual

### Consultar un Día Específico

1. Usa el selector de fecha en la parte superior
2. Selecciona la fecha deseada
3. Haz clic en el botón de actualizar (🔄)
4. El sistema mostrará los datos de ese día

### Imprimir el Reporte

1. Haz clic en el botón **"Imprimir"** 
2. Se abrirá la vista previa de impresión
3. El formato está optimizado para papel
4. Incluye encabezado con fecha y pie de página con timestamp

### Exportar a CSV

1. Haz clic en el botón **"Exportar CSV"**
2. Se descargará un archivo: `cierre-caja-YYYY-MM-DD.csv`
3. El archivo incluye:
   - Resumen general
   - Desglose de métodos de pago
   - Productos más vendidos
4. Puede abrirse en Excel, Google Sheets, etc.

## 💡 Detalles Técnicos

### Filtrado de Datos

El sistema filtra las órdenes por:
- **Fecha de creación** (`created_at`)
- Solo órdenes del día seleccionado
- Comparación normalizada (00:00:00) para precisión

### Cálculo de Ventas

Solo se cuentan para ventas:
- Órdenes con `payment_status === 'paid'`
- Del día específico seleccionado
- Con al menos un pago registrado

### Métodos de Pago

Se obtienen de:
- Tabla `order_payments` (pagos registrados)
- Relación con tabla `payment_methods`
- Suma total por cada método
- Cuenta de transacciones

### Productos Vendidos

Se procesan de:
- `order_items` de cada orden
- Agrupados por producto/ítem de menú
- Suma de cantidades y totales
- Top 10 más vendidos

## 🎨 Formato de Impresión

El reporte impreso incluye:

### Encabezado
```
CIERRE DE CAJA
Fecha: [Fecha seleccionada]
```

### Secciones
1. Resumen en tarjetas (4 métricas principales)
2. Desglose por métodos de pago
3. Productos más vendidos
4. Listado de órdenes

### Pie de Página
```
Reporte generado el: [Fecha y hora actual]
Sistema de Gestión para Restaurante/Kiosko
```

### Optimizaciones
- Sin botones ni elementos de navegación
- Bordes simplificados
- Tamaño de fuente ajustado
- `break-inside: avoid` para no cortar secciones

## 📊 Formato CSV

El archivo CSV exportado contiene:

```csv
CIERRE DE CAJA - 2025-11-09

RESUMEN GENERAL
Total Ventas,$487.20
Total Órdenes,15
Órdenes Completadas,13
Órdenes Canceladas,2
Ticket Promedio,$37.48

MÉTODOS DE PAGO
Método,Cantidad,Monto
Efectivo,8,$320.50
Tarjeta de Crédito,5,$166.70

PRODUCTOS MÁS VENDIDOS
Producto,Cantidad,Total
Hamburguesa Clásica,12,$180.00
Papas Fritas,15,$75.00
...
```

## 🔐 Permisos y Acceso

- Requiere autenticación
- Accesible para usuarios con permisos apropiados
- Los datos son filtrados por `business_id` automáticamente
- Solo se muestran datos del negocio del usuario actual

## 📝 Casos de Uso

### 1. Cierre Diario
- Al final del día, revisa el total de ventas
- Compara con el efectivo en caja
- Verifica los métodos de pago

### 2. Análisis de Productos
- Identifica los productos más vendidos
- Planifica compras de inventario
- Ajusta el menú según demanda

### 3. Auditoría
- Exporta CSV para contabilidad
- Imprime reporte para archivo físico
- Revisa órdenes canceladas

### 4. Comparación Histórica
- Consulta días anteriores
- Compara ventas entre fechas
- Identifica tendencias

## 🎯 Métricas Calculadas

### Total Ventas
```typescript
orders
  .filter(o => o.payment_status === 'paid')
  .reduce((sum, o) => sum + o.total, 0)
```

### Ticket Promedio
```typescript
totalVentas / cantidadOrdenesPagadas
```

### Por Método de Pago
```typescript
// Suma de todos los payments de cada método
order.payments
  .filter(p => p.payment_method_id === methodId)
  .reduce((sum, p) => sum + p.amount, 0)
```

### Productos Vendidos
```typescript
// Suma de quantities por producto
order.items
  .filter(i => i.product_id === productId)
  .reduce((sum, i) => sum + i.quantity, 0)
```

## 🔮 Mejoras Futuras (Opcional)

Posibles extensiones:
- 📈 Gráficos de ventas por hora
- 📅 Comparación con días anteriores
- 💰 Apertura de caja (monto inicial)
- 📤 Gastos y retiros del día
- 👥 Ventas por cajero/mesero
- 🏆 Metas de ventas diarias
- 📧 Envío automático por email
- 📱 Notificaciones al finalizar el día
- 🔒 Bloqueo de caja después de cerrar
- 💾 Guardar cierres en base de datos
- 📊 Dashboard de cierres mensuales

## 📂 Archivos del Módulo

### Frontend
```
frontend/src/app/features/cash-closing/
├── cash-closing.component.ts    # Lógica del componente
├── cash-closing.component.html  # Template visual
└── cash-closing.component.scss  # Estilos (impresión)
```

### Rutas
- **URL**: `/cash-closing`
- **Menú**: "Cierre de Caja" 🧮
- **Lazy Loading**: Carga solo cuando se accede

### Servicios Utilizados
- `OrderService` - Obtención de órdenes
- `PaymentMethodService` - Métodos de pago

## 🎨 Diseño Responsive

### Desktop
- 4 tarjetas en una fila
- Tablas completas visibles
- Botones de acción en header

### Tablet
- 2-3 tarjetas por fila
- Tablas con scroll horizontal si necesario
- Layout ajustado

### Mobile
- 1 tarjeta por fila
- Tablas optimizadas
- Botones apilados verticalmente

## ⚡ Rendimiento

- **Carga inicial**: Rápida (solo datos del día)
- **Filtrado**: En cliente (JavaScript)
- **Exportación**: Instantánea
- **Impresión**: Optimizada para papel

## 🐛 Solución de Problemas

### No aparecen datos
- Verifica que haya órdenes en la fecha seleccionada
- Asegúrate de que las órdenes tengan estado `paid`
- Revisa la consola del navegador por errores

### La impresión no se ve bien
- Usa Chrome o Edge para mejores resultados
- Verifica la configuración de impresión (orientación, márgenes)
- Algunos navegadores tienen mejor soporte CSS de impresión

### El CSV no se descarga
- Verifica permisos del navegador para descargas
- Revisa que no haya bloqueadores de pop-ups
- Intenta con otro navegador

---

**Fecha de implementación:** 9 de noviembre de 2025  
**Estado:** ✅ Completado y listo para producción  
**Versión:** 1.0.0

