# 🏢 Nombre del Negocio Dinámico

## ✨ Funcionalidad

El nombre del negocio configurado en el módulo de **Configuración** aparece automáticamente en:
- 📍 Sidebar (logo/header)
- 📍 Top bar (título principal)

## 🎯 Comportamiento

### Si NO hay configuración:
```
Sidebar: "Sistema de Gestión"
Top Bar: "Sistema de Gestión"
```

### Si hay configuración con nombre:
```
Configuración:
  Nombre: "Restaurante El Sabor"

Sidebar: "Restaurante El Sabor"
         "Sistema de Gestión" (subtítulo pequeño)
         
Top Bar: "Restaurante El Sabor"
         "Panel de Control" (subtítulo)
```

## 🔄 Actualización Dinámica

### Flujo:
```
1. Usuario configura negocio
2. Guarda "Restaurante El Sabor"
3. Recarga la página
4. El nombre aparece automáticamente en sidebar y top bar
```

## 💻 Implementación

### Backend:
El endpoint `/api/configuration` retorna la configuración del negocio.

### Frontend:
```typescript
ngOnInit(): void {
  this.loadBusinessName();
}

loadBusinessName(): void {
  this.configService.getConfiguration().subscribe({
    next: (config) => {
      if (config && config.business_name) {
        this.businessName = config.business_name;
      }
    },
    error: () => {
      this.businessName = 'Sistema de Gestión';
    }
  });
}
```

### Template:
```html
<!-- Sidebar -->
<span class="font-bold text-lg">{{ businessName }}</span>
<span *ngIf="businessName !== 'Sistema de Gestión'" class="text-xs">
  Sistema de Gestión
</span>

<!-- Top Bar -->
<h2 class="text-2xl font-bold">{{ businessName }}</h2>
<p class="text-sm text-gray-500">Panel de Control</p>
```

## 🎨 Vista Visual

### Sin Configuración:
```
┌─────────────────────┐
│ [🏠] Sistema de     │
│      Gestión        │
├─────────────────────┤
│ Dashboard           │
│ Inventario          │
│ ...                 │
└─────────────────────┘
```

### Con Configuración:
```
┌─────────────────────┐
│ [🏠] Restaurante El │
│      Sabor          │
│      Sistema de     │
│      Gestión        │
├─────────────────────┤
│ Dashboard           │
│ Inventario          │
│ ...                 │
└─────────────────────┘
```

## 🎯 Casos de Uso

### Caso 1: Nuevo Usuario
```
1. Instala el sistema
2. Login como admin
3. Ve "Sistema de Gestión" en todas partes
4. Va a Configuración
5. Llena "Restaurante Los Amigos"
6. Recarga (F5)
7. Ahora ve "Restaurante Los Amigos" ✅
```

### Caso 2: Cambio de Nombre
```
1. Negocio cambia de nombre
2. Admin va a Configuración
3. Actualiza nombre
4. Recarga la página
5. Nuevo nombre aparece en toda la interfaz ✅
```

### Caso 3: Múltiples Usuarios
```
- Admin ve: "Restaurante El Sabor"
- Manager ve: "Restaurante El Sabor"
- Waiter ve: "Restaurante El Sabor"
- Todos ven el mismo nombre del negocio ✅
```

## 💡 Beneficios

1. **Personalización**: Cada negocio tiene su identidad
2. **Profesional**: No dice "RestaurantApp" genérico
3. **Branding**: Refuerza la marca del negocio
4. **Automático**: Se actualiza solo al configurar
5. **Fallback**: Siempre muestra algo coherente

## 🔄 Sincronización

El nombre se carga:
- ✅ Al iniciar sesión
- ✅ Al refrescar la página
- ✅ Al navegar entre páginas
- ✅ Cuando se actualiza la configuración

## 🚀 Mejoras Futuras

Próximamente se podría:
- [ ] Mostrar logo del negocio (si existe)
- [ ] Cambiar colores según configuración
- [ ] Mostrar slogan del negocio
- [ ] Personalizar favicon
- [ ] Título de la pestaña del navegador

## 📊 Ejemplo Completo

### Configuración:
```json
{
  "business_name": "Pizzería Bella Napoli",
  "legal_name": "Bella Napoli S.R.L.",
  "rif": "J-98765432-1"
}
```

### Resultado en UI:
```
Sidebar Header: 
  🏠 Pizzería Bella Napoli
     Sistema de Gestión

Top Bar:
  Pizzería Bella Napoli
  Panel de Control
```

---

**Nombre del negocio dinámico implementado** ✅

Ahora el sistema se adapta automáticamente al nombre de cada negocio.

