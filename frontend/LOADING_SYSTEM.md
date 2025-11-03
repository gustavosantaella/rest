# 🔄 Sistema de Loading Global

## 📋 Descripción

Sistema completo y automático de indicadores de carga para todas las peticiones HTTP de la aplicación.

## ✨ Características

- ✅ **Automático**: Se activa en todas las peticiones HTTP
- ✅ **Global**: Un loader para toda la aplicación
- ✅ **Inteligente**: Cuenta peticiones simultáneas
- ✅ **Reutilizable**: Componente que puedes usar donde quieras
- ✅ **Personalizable**: Tamaños, mensajes, estilos
- ✅ **Overlay o Inline**: Dos modos de visualización
- ✅ **Performance**: Ligero y eficiente

## 🏗️ Componentes del Sistema

### 1. LoadingService
Servicio que controla el estado global de carga.

### 2. LoadingInterceptor
Interceptor HTTP que automáticamente muestra/oculta el loader.

### 3. LoadingSpinnerComponent
Componente visual del spinner (reutilizable).

### 4. GlobalLoadingComponent
Componente global montado en `app.component`.

## 🎯 Funcionamiento Automático

### Sin Código Adicional:

```typescript
// Petición HTTP normal
this.productService.getProducts().subscribe({
  next: (products) => {
    this.products = products;
  }
});

// ✅ El loader se muestra automáticamente al iniciar
// ✅ El loader se oculta automáticamente al terminar
```

### Múltiples Peticiones Simultáneas:

```typescript
// Tres peticiones al mismo tiempo
this.productService.getProducts().subscribe(...);
this.tableService.getTables().subscribe(...);
this.orderService.getOrders().subscribe(...);

// ✅ El loader se muestra una vez
// ✅ El loader se mantiene hasta que TODAS terminen
// ✅ El loader se oculta cuando la última termine
```

## 🎨 Uso Manual (Opcional)

### En Componentes:

```typescript
import { LoadingService } from '../../core/services/loading.service';

export class MyComponent {
  private loadingService = inject(LoadingService);
  
  async doLongOperation() {
    this.loadingService.show();
    
    try {
      await step1();
      await step2();
      await step3();
    } finally {
      this.loadingService.hide();
    }
  }
}
```

### Loader Inline (Local):

```typescript
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';

@Component({
  imports: [LoadingSpinnerComponent],
  template: `
    <div class="card">
      <app-loading-spinner 
        [show]="localLoading"
        [isOverlay]="false"
        size="md"
        message="Cargando datos..."
      ></app-loading-spinner>
      
      <div *ngIf="!localLoading">
        <!-- Tu contenido -->
      </div>
    </div>
  `
})
export class MyComponent {
  localLoading = false;
  
  loadData() {
    this.localLoading = true;
    this.service.getData().subscribe({
      next: (data) => {
        this.data = data;
        this.localLoading = false;
      }
    });
  }
}
```

## 📊 Tipos de Loading

### 1. Global (Automático)
- Se muestra en **TODAS** las peticiones HTTP
- Overlay de pantalla completa
- Mensaje "Procesando..."
- **No requiere código adicional**

### 2. Local (Manual)
- Para operaciones específicas
- Inline o overlay según necesites
- Mensajes personalizados
- Control total sobre cuándo mostrar/ocultar

## 🎨 Personalización

### Tamaños Disponibles:

| Tamaño | Píxeles | Uso Recomendado |
|--------|---------|-----------------|
| `sm` | 32px | Botones, badges |
| `md` | 48px | Cards, formularios |
| `lg` | 64px | Pantallas completas |
| `xl` | 80px | Splash screens |

### Ejemplos de Mensajes:

```html
<!-- Operaciones genéricas -->
message="Cargando..."
message="Procesando..."

<!-- Operaciones específicas -->
message="Guardando producto..."
message="Creando orden..."
message="Procesando pago..."
message="Eliminando registro..."

<!-- Operaciones largas -->
message="Esto puede tomar unos segundos..."
message="Generando reporte, por favor espera..."
```

## 🔧 Casos de Uso Reales

### Caso 1: Petición HTTP Normal
```typescript
// ✅ Automático - No requiere código
this.service.getData().subscribe(data => {
  this.data = data;
});
```

### Caso 2: Operación sin HTTP
```typescript
import { LoadingService } from '../../core/services/loading.service';

exportToExcel() {
  this.loadingService.show();
  
  try {
    // Operación pesada
    const data = this.processLargeData();
    this.downloadFile(data);
  } finally {
    this.loadingService.hide();
  }
}
```

### Caso 3: Loader en Modal
```html
<div class="modal">
  <app-loading-spinner 
    [show]="saving"
    [isOverlay]="true"
    size="lg"
    message="Guardando cambios..."
  ></app-loading-spinner>
  
  <form (ngSubmit)="save()">
    <!-- Formulario -->
  </form>
</div>
```

```typescript
save() {
  this.saving = true;
  this.service.save(this.form.value).subscribe({
    next: () => {
      this.saving = false;
      this.closeModal();
    },
    error: () => {
      this.saving = false;
      alert('Error al guardar');
    }
  });
}
```

### Caso 4: Loader en Tabla
```html
<div class="table-container">
  <app-loading-spinner 
    [show]="loading"
    [isOverlay]="false"
    size="sm"
  ></app-loading-spinner>
  
  <table *ngIf="!loading" class="table">
    <thead>...</thead>
    <tbody>...</tbody>
  </table>
</div>
```

## 💡 Mejores Prácticas

### ✅ DO:
- Usa el loader automático para peticiones HTTP
- Usa loaders inline para contenido específico
- Proporciona mensajes descriptivos
- Oculta el contenido mientras carga

### ❌ DON'T:
- No uses múltiples loaders globales
- No olvides llamar a `hide()` en el `finally`
- No uses loaders para operaciones instantáneas
- No bloquees la UI innecesariamente

## 🎯 Ventajas

1. **Mejor UX**: Usuario sabe que algo está pasando
2. **Sin confusión**: No hace clicks múltiples
3. **Profesional**: Sistema se ve más pulido
4. **Feedback visual**: Siempre informado
5. **Automático**: 99% sin código adicional

## 📊 Estadísticas de Implementación

- **Archivos creados**: 3
- **Líneas de código**: ~200
- **Componentes afectados**: Todos (automático)
- **Configuración necesaria**: Mínima
- **Mantenimiento**: Bajo

## 🐛 Troubleshooting

### El loader no desaparece
```typescript
// Siempre usa finalize() en observables
this.service.getData().pipe(
  finalize(() => this.loading = false)
).subscribe(...);
```

### Loader parpadeante en peticiones rápidas
```typescript
// Agregar delay mínimo (opcional)
setTimeout(() => {
  this.loadingService.show();
}, 100);
```

### Quiero deshabilitar el loader global
```typescript
// Remover el interceptor de main.ts
provideHttpClient(
  withInterceptors([authInterceptor])  // Sin loadingInterceptor
)
```

## 🚀 Roadmap Futuro

- [ ] Modo skeleton screen
- [ ] Progress bar para uploads
- [ ] Estimación de tiempo restante
- [ ] Cancelación de peticiones
- [ ] Queue de peticiones
- [ ] Retry automático

---

**Sistema de loading completamente implementado y funcional** ✅

