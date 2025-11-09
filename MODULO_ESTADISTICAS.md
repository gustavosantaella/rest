# Módulo de Estadísticas 📊

## 🎉 IMPLEMENTACIÓN 100% COMPLETA

Sistema profesional de estadísticas y análisis de negocio con 4 secciones especializadas accesibles desde un dropdown en el menú lateral.

---

## 📋 Estructura del Módulo

El módulo de estadísticas está organizado en un **dropdown con 4 secciones**:

```
📊 Estadísticas ▼
   📈 General
   🏆 Más/Menos Vendidos
   👥 Clientes
   💰 Ingresos y Egresos
```

---

## 🎯 Sección 1: Estadísticas Generales

**Ruta:** `/statistics/general`

### Métricas Principales
- **Ingresos Totales** 💚 - Total de ventas del período
- **Total Órdenes** 💙 - Cantidad de órdenes generadas
- **Ticket Promedio** 💜 - Promedio de gasto por orden
- **Balance Neto** 🟠 - Ingresos - Egresos

### Análisis de Rendimiento
- **Tasa de Completación** - Porcentaje de órdenes completadas
- **Barra de progreso visual** con porcentaje
- **Órdenes canceladas** incluidas en el análisis

### Cuentas Pendientes
- **Por Cobrar** 🟠 - Dinero que te deben
- **Por Pagar** 🔴 - Dinero que debes

### Selector de Período
- Últimos 7 días
- Últimos 15 días
- Últimos 30 días (default)
- Últimos 60 días
- Últimos 90 días

**Backend Endpoint:** `GET /api/statistics/general?days=30`

---

## 🏆 Sección 2: Más y Menos Vendidos

**Ruta:** `/statistics/best-sellers`

### Productos Más Vendidos 🥇
- **Top 10** productos del inventario
- Ranking numerado (1º, 2º, 3º...)
- Cantidad de unidades vendidas
- Total de ventas generadas
- Diseño verde con gradiente

### Ítems de Menú Más Vendidos 🍽️
- **Top 10** platos del menú
- Cantidad de órdenes
- Total de ventas
- Diseño azul con gradiente

### Productos Menos Vendidos 📉
- Productos con menor venta
- Identificación de problemas
- Sugerencia para revisar precios/promoción
- Diseño naranja de alerta

### Selector de Período
- Últimos 7 días
- Últimos 30 días (default)
- Últimos 60 días
- Últimos 90 días

**Backend Endpoint:** `GET /api/statistics/best-sellers?days=30&limit=10`

---

## 👥 Sección 3: Estadísticas de Clientes

**Ruta:** `/statistics/customers`

### Métricas de Clientes
- **Total Clientes** 💙 - Base de clientes registrados
- **Nuevos Clientes (30 días)** 💚 - Crecimiento reciente
- **Total Deuda** 🟠 - Cuentas por cobrar pendientes

### Clientes con Deuda Pendiente
- **Tabla detallada** con:
  - Nombre del cliente
  - Cantidad de cuentas pendientes
  - Monto total de deuda
- **Ordenados** de mayor a menor deuda
- **Empty state** cuando no hay deudas (¡Excelente!)

### Casos de Uso
- Identificar clientes con más deudas
- Priorizar gestión de cobros
- Análisis de crecimiento de base de clientes

**Backend Endpoint:** `GET /api/statistics/customers`

---

## 💰 Sección 4: Ingresos y Egresos

**Ruta:** `/statistics/financial`

### Resumen Financiero Principal
- **Ingresos** 💚 - Total de ventas del período
- **Egresos** 🔴 - Total de pagos a proveedores
- **Ganancia Neta** 💙 - Ingresos - Egresos
- **Margen de Ganancia** - Porcentaje de rentabilidad

### Balance Proyectado 💜
- **Cálculo completo**:
  ```
  Ganancia Neta
  + Por Cobrar Pendiente
  - Por Pagar Pendiente
  = Balance Proyectado
  ```
- Muestra el estado financiero real proyectado

### Ingresos por Método de Pago
- **Desglose completo** de cada método
- Efectivo, Transferencia, Tarjeta, etc.
- Monto total por método
- Ordenados de mayor a menor

### Cuentas Pendientes
- **Por Cobrar** 🟠 - Dinero pendiente de clientes
- **Por Pagar** 🔴 - Deudas pendientes con proveedores

### Selector de Período
- Últimos 7 días
- Últimos 30 días (default)
- Últimos 60 días
- Últimos 90 días

**Backend Endpoint:** `GET /api/statistics/financial?days=30`

---

## 🗂️ Estructura de Archivos

```
backend/
└── app/routers/
    └── statistics.py ✅
        ├── GET /statistics/general
        ├── GET /statistics/best-sellers
        ├── GET /statistics/customers
        └── GET /statistics/financial

frontend/
└── src/app/
    ├── core/
    │   ├── models/
    │   │   └── statistics.model.ts ✅
    │   │       ├── GeneralStatistics
    │   │       ├── BestSellersStatistics
    │   │       ├── CustomerStatistics
    │   │       └── FinancialStatistics
    │   └── services/
    │       └── statistics.service.ts ✅
    │
    └── features/statistics/
        ├── general/
        │   ├── statistics-general.component.ts ✅
        │   ├── statistics-general.component.html ✅
        │   └── statistics-general.component.scss ✅
        ├── best-sellers/
        │   ├── statistics-best-sellers.component.ts ✅
        │   ├── statistics-best-sellers.component.html ✅
        │   └── statistics-best-sellers.component.scss ✅
        ├── customers/
        │   ├── statistics-customers.component.ts ✅
        │   ├── statistics-customers.component.html ✅
        │   └── statistics-customers.component.scss ✅
        └── financial/
            ├── statistics-financial.component.ts ✅
            ├── statistics-financial.component.html ✅
            └── statistics-financial.component.scss ✅
```

---

## 📊 Endpoints de la API

### 1. Estadísticas Generales
```http
GET /api/statistics/general?days=30
```

**Respuesta:**
```json
{
  "period_days": 30,
  "total_orders": 150,
  "completed_orders": 140,
  "cancelled_orders": 10,
  "total_revenue": 15000.00,
  "average_ticket": 107.14,
  "orders_by_day": {
    "2025-11-01": 5,
    "2025-11-02": 8,
    ...
  },
  "revenue_by_day": {
    "2025-11-01": 450.00,
    "2025-11-02": 720.00,
    ...
  },
  "total_receivable": 2500.00,
  "total_payable": 1800.00,
  "net_balance": 15700.00
}
```

### 2. Más Vendidos
```http
GET /api/statistics/best-sellers?days=30&limit=10
```

**Respuesta:**
```json
{
  "period_days": 30,
  "best_products": [
    {
      "id": 1,
      "name": "Hamburguesa Clásica",
      "quantity": 120,
      "total_sales": 1800.00
    },
    ...
  ],
  "best_menu_items": [...],
  "worst_products": [...]
}
```

### 3. Clientes
```http
GET /api/statistics/customers
```

**Respuesta:**
```json
{
  "total_customers": 45,
  "new_customers_last_30_days": 12,
  "customers_with_debt": [
    {
      "id": 1,
      "name": "Juan Pérez",
      "accounts_count": 3,
      "total_pending": 500.00
    },
    ...
  ],
  "total_debt_from_customers": 2500.00
}
```

### 4. Financiero
```http
GET /api/statistics/financial?days=30
```

**Respuesta:**
```json
{
  "period_days": 30,
  "total_income": 15000.00,
  "total_expenses": 8000.00,
  "net_profit": 7000.00,
  "income_by_method": {
    "Efectivo": 8000.00,
    "Transferencia": 5000.00,
    "Tarjeta": 2000.00
  },
  "total_pending_income": 2500.00,
  "total_pending_expenses": 1800.00,
  "projected_balance": 7700.00,
  "profit_margin": 46.67
}
```

---

## 🎨 Diseño Visual

### Paleta de Colores

#### Estadísticas Generales
- Verde → Ingresos
- Azul → Órdenes
- Morado → Ticket promedio
- Naranja → Balance

#### Más/Menos Vendidos
- Verde → Productos top
- Azul → Menú top
- Naranja → Menos vendidos

#### Clientes
- Azul → Total clientes
- Verde → Nuevos clientes
- Naranja → Deuda total

#### Financiero
- Verde → Ingresos
- Rojo → Egresos
- Azul → Ganancia neta
- Morado → Balance proyectado

### Tarjetas con Gradientes
```scss
bg-gradient-to-br from-green-50 to-white
border-l-4 border-green-500
```

### Iconos Representativos
- 💰 Dinero
- 💸 Gastos
- 📊 Estadísticas
- 🏆 Ganadores
- 📉 Decrecimiento
- 👥 Clientes
- 📈 Crecimiento

---

## 🚀 Cómo Usar

### Acceder al Módulo

1. En el menú lateral, haz click en **"Estadísticas"** 📊
2. Se despliega un dropdown con 4 opciones
3. Selecciona la sección que deseas ver

### Cambiar Período de Análisis

En **General**, **Más/Menos Vendidos** e **Ingresos/Egresos**:
1. Usa el selector en la esquina superior derecha
2. Elige el período (7, 15, 30, 60 o 90 días)
3. Los datos se actualizan automáticamente

### Interpretar los Datos

#### Balance Neto
- **Positivo (verde)**: Ganancia
- **Negativo (rojo)**: Pérdida

#### Balance Proyectado
```
Ejemplo:
Ganancia Neta: $7,000
+ Por Cobrar: $2,500
- Por Pagar: $1,800
= Balance Proyectado: $7,700
```

#### Margen de Ganancia
```
(Ganancia Neta / Ingresos Totales) × 100
```
- **> 20%**: Excelente
- **10-20%**: Bueno
- **< 10%**: Mejorable

---

## 💡 Casos de Uso

### Caso 1: Análisis de Productos
```
Problema: Ventas bajas

1. Ve a "Más/Menos Vendidos"
2. Revisa productos menos vendidos
3. Identifica: "Producto X - solo 2 unidades"
4. Decisión: 
   - Bajar precio
   - Hacer promoción
   - Remover del menú
```

### Caso 2: Gestión de Cobros
```
Objetivo: Recuperar cartera

1. Ve a "Estadísticas de Clientes"
2. Identifica clientes con más deuda
3. Prioriza gestión de cobro
4. Ve a "Cuentas por Cobrar" para acción
```

### Caso 3: Control Financiero
```
Pregunta: ¿Es rentable el negocio?

1. Ve a "Ingresos y Egresos"
2. Revisa Ganancia Neta
3. Verifica Margen de Ganancia
4. Compara con meses anteriores
5. Toma decisiones estratégicas
```

### Caso 4: Planificación de Inventario
```
Objetivo: Optimizar stock

1. Ve a "Más/Menos Vendidos"
2. Productos top → Comprar más stock
3. Productos bajos → Reducir pedidos
4. Optimiza inversión en inventario
```

---

## 🔧 Lógica de Negocio

### Cálculo de Estadísticas Generales

```python
# Total de órdenes
total_orders = count(orders del período)

# Tasa de completación
completion_rate = (completed / total) * 100

# Ticket promedio
average_ticket = total_revenue / paid_orders

# Balance neto
net_balance = revenue + receivable - payable
```

### Productos Más Vendidos

```sql
SELECT 
  product.name,
  SUM(order_item.quantity) as total_quantity,
  SUM(order_item.subtotal) as total_sales
FROM order_items
WHERE order_id IN (orders del período)
GROUP BY product.id
ORDER BY total_quantity DESC
LIMIT 10
```

### Análisis Financiero

```python
# Ingresos
total_income = SUM(orders pagadas del período)

# Egresos
total_expenses = SUM(pagos a proveedores del período)

# Ganancia
net_profit = total_income - total_expenses

# Margen
profit_margin = (net_profit / total_income) * 100
```

---

## 📈 Interpretación de Datos

### Indicadores Clave (KPIs)

#### 1. Ticket Promedio
- **Aumenta**: Clientes gastan más
- **Disminuye**: Revisar precios o estrategia

#### 2. Tasa de Completación
- **> 90%**: Excelente servicio
- **< 80%**: Problemas operativos

#### 3. Margen de Ganancia
- **Saludable**: 15-25% para restaurantes
- **< 10%**: Revisar costos urgente

#### 4. Balance Proyectado
- Incluye deudas y créditos
- Visión realista del flujo de caja
- Planificación financiera

---

## 🎨 Características de Diseño

### Tarjetas con Gradientes
```html
<!-- Ingresos -->
<div class="card bg-gradient-to-br from-green-50 to-white border-l-4 border-green-500">
```

### Barras de Progreso Animadas
```html
<div class="h-4 bg-gray-200 rounded-full">
  <div class="h-full bg-green-500 transition-all" 
       [style.width.%]="percentage">
  </div>
</div>
```

### Rankings con Números
```html
<div class="w-8 h-8 bg-green-600 text-white rounded-full">
  {{ position }}
</div>
```

### Colores Semánticos
- Verde: Positivo, ingresos, ganancias
- Rojo: Negativo, egresos, pérdidas
- Azul: Neutral, información
- Naranja: Advertencia, pendiente
- Morado: Especial, proyecciones

---

## 🔐 Seguridad y Aislamiento

- ✅ **Autenticación requerida** (JWT)
- ✅ **Filtrado por business_id** automático
- ✅ **Solo datos del negocio** del usuario actual
- ✅ **Sin acceso cruzado** entre negocios
- ✅ **Queries optimizadas** con índices

---

## 📱 Responsive Design

### Desktop
- 4 tarjetas por fila en métricas principales
- 2 columnas en análisis detallado
- Tablas completas visibles

### Tablet
- 2-3 tarjetas por fila
- Scroll horizontal en tablas si necesario

### Mobile
- 1 tarjeta por fila
- Tablas optimizadas
- Ranking compacto

---

## 🎯 Beneficios del Módulo

### Para el Dueño
- 👁️ Visión completa del negocio
- 💰 Control financiero total
- 📊 Decisiones basadas en datos
- 🎯 Identificación de oportunidades

### Para Gerentes
- 📈 Seguimiento de rendimiento
- 🏆 Productos exitosos identificados
- 📉 Problemas detectados temprano
- 👥 Gestión eficiente de clientes

### Para el Negocio
- 💡 Insights valiosos
- 📊 Reportes profesionales
- 🚀 Optimización continua
- 💼 Planificación estratégica

---

## 🔮 Mejoras Futuras (Opcional)

### Gráficos Visuales
- 📈 Chart.js o ApexCharts
- 📊 Gráficos de línea para tendencias
- 🥧 Gráficos de pastel para distribución
- 📉 Gráficos de barras comparativos

### Exportación
- 📄 Exportar a PDF
- 📊 Exportar a Excel
- 📧 Envío automático por email
- 📅 Reportes programados

### Comparaciones
- 📅 Comparar períodos
- 📊 Año actual vs año anterior
- 📈 Tendencias históricas
- 🎯 Metas vs realidad

### Análisis Avanzado
- 🤖 Predicciones con IA
- 📊 Análisis de estacionalidad
- 👥 Segmentación de clientes
- 💡 Recomendaciones automáticas

---

## ✅ Checklist de Implementación

### Backend
- [x] Router de estadísticas
- [x] Endpoint de estadísticas generales
- [x] Endpoint de más/menos vendidos
- [x] Endpoint de estadísticas de clientes
- [x] Endpoint financiero
- [x] Queries optimizadas
- [x] Filtrado por business_id
- [x] Integrado en main.py

### Frontend
- [x] Modelos TypeScript
- [x] Servicio de estadísticas
- [x] Componente General (TS + HTML + SCSS)
- [x] Componente Más/Menos Vendidos (TS + HTML + SCSS)
- [x] Componente Clientes (TS + HTML + SCSS)
- [x] Componente Financiero (TS + HTML + SCSS)
- [x] Rutas configuradas
- [x] Dropdown en menú lateral
- [x] Selectores de período
- [x] Diseño responsive

---

## 🎉 Conclusión

**MÓDULO DE ESTADÍSTICAS 100% FUNCIONAL**

El sistema ahora incluye un análisis completo y profesional del negocio con:
- ✅ 4 secciones especializadas
- ✅ 3 endpoints optimizados
- ✅ Diseño moderno y responsive
- ✅ Métricas en tiempo real
- ✅ Análisis financiero completo
- ✅ Identificación de productos
- ✅ Seguimiento de clientes

**Perfecto para toma de decisiones estratégicas** 🎯

---

**Fecha de implementación:** 9 de noviembre de 2025  
**Estado:** ✅ COMPLETADO  
**Versión:** 1.0.0

