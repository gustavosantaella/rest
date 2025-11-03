# 🔄 Componentes Compartidos

## LoadingSpinner

Componente reutilizable para mostrar indicadores de carga.

### 📋 Uso Básico

```typescript
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';

@Component({
  imports: [LoadingSpinnerComponent]
})
```

```html
<app-loading-spinner 
  [show]="loading"
  [isOverlay]="true"
  size="md"
  message="Cargando..."
></app-loading-spinner>
```

### 🎯 Propiedades

#### `show` (boolean) - **Requerido**
Controla la visibilidad del loader.

```html
<app-loading-spinner [show]="isLoading"></app-loading-spinner>
```

#### `isOverlay` (boolean)
Si es `true`, muestra un overlay de pantalla completa.  
Si es `false`, muestra el loader inline.  
**Default:** `true`

```html
<!-- Overlay de pantalla completa -->
<app-loading-spinner [show]="loading" [isOverlay]="true"></app-loading-spinner>

<!-- Inline en un contenedor -->
<app-loading-spinner [show]="loading" [isOverlay]="false"></app-loading-spinner>
```

#### `size` ('sm' | 'md' | 'lg' | 'xl')
Tamaño del spinner.  
**Default:** `'md'`

```html
<app-loading-spinner [show]="loading" size="sm"></app-loading-spinner>
<app-loading-spinner [show]="loading" size="lg"></app-loading-spinner>
```

#### `message` (string)
Mensaje opcional a mostrar debajo del spinner.

```html
<app-loading-spinner 
  [show]="loading" 
  message="Guardando datos..."
></app-loading-spinner>
```

#### `customClass` (string)
Clases CSS adicionales personalizadas.

```html
<app-loading-spinner 
  [show]="loading" 
  customClass="my-custom-class"
></app-loading-spinner>
```

## GlobalLoading

Componente global que se muestra automáticamente en todas las peticiones HTTP.

### 📋 Configuración

Ya está configurado en `app.component.ts`:

```typescript
import { GlobalLoadingComponent } from './shared/components/global-loading/global-loading.component';

@Component({
  imports: [GlobalLoadingComponent],
  template: `
    <router-outlet></router-outlet>
    <app-global-loading></app-global-loading>
  `
})
```

### 🎯 Funcionamiento

- Se activa **automáticamente** en todas las peticiones HTTP
- Se oculta cuando todas las peticiones terminan
- Cuenta múltiples peticiones simultáneas
- No requiere código adicional en componentes

## LoadingService

Servicio para controlar el estado de carga manualmente.

### 📋 Uso Manual

```typescript
import { LoadingService } from '../../core/services/loading.service';

export class MyComponent {
  private loadingService = inject(LoadingService);
  
  async doSomething() {
    this.loadingService.show();
    
    try {
      // Tu código aquí
      await someAsyncOperation();
    } finally {
      this.loadingService.hide();
    }
  }
}
```

### 🎯 Métodos

#### `show()`
Muestra el loader global.

#### `hide()`
Oculta el loader global.

#### `isLoading()`
Retorna `true` si hay alguna petición en curso.

#### `loading$`
Observable para subscribirse a cambios de estado.

```typescript
this.loadingService.loading$.subscribe(isLoading => {
  console.log('Loading:', isLoading);
});
```

## 📱 Ejemplos Completos

### Ejemplo 1: Loader Automático (Global)
```typescript
// NO requiere código adicional
// El interceptor HTTP maneja todo automáticamente

this.productService.getProducts().subscribe({
  next: (products) => {
    // El loader se muestra automáticamente
    this.products = products;
    // El loader se oculta automáticamente
  }
});
```

### Ejemplo 2: Loader en Componente (Inline)
```typescript
@Component({
  imports: [LoadingSpinnerComponent],
  template: `
    <div class="card">
      <app-loading-spinner 
        [show]="loading"
        [isOverlay]="false"
        size="md"
        message="Cargando productos..."
      ></app-loading-spinner>
      
      <div *ngIf="!loading">
        <!-- Contenido -->
      </div>
    </div>
  `
})
export class MyComponent {
  loading = true;
  
  ngOnInit() {
    this.loadData();
  }
  
  loadData() {
    this.loading = true;
    this.service.getData().subscribe({
      next: (data) => {
        this.data = data;
        this.loading = false;
      }
    });
  }
}
```

### Ejemplo 3: Loader Manual para Operaciones Largas
```typescript
import { LoadingService } from '../../core/services/loading.service';

export class MyComponent {
  private loadingService = inject(LoadingService);
  
  async processLargeFile() {
    this.loadingService.show();
    
    try {
      await this.processStep1();
      await this.processStep2();
      await this.processStep3();
    } catch (error) {
      console.error(error);
    } finally {
      this.loadingService.hide();
    }
  }
}
```

### Ejemplo 4: Loader con Mensaje Personalizado
```html
<app-loading-spinner 
  [show]="saving"
  [isOverlay]="true"
  size="lg"
  message="Guardando cambios, por favor espera..."
></app-loading-spinner>
```

## 🎨 Personalización

### Cambiar Colores

En `loading-spinner.component.ts`, modifica los estilos:

```css
.spinner {
  border: 4px solid rgba(255, 0, 0, 0.3);  /* Color base */
  border-top: 4px solid #ff0000;  /* Color animado */
}
```

### Cambiar Velocidad de Animación

```css
.spinner {
  animation: spin 1.2s linear infinite;  /* Más lento */
}
```

### Cambiar Fondo del Overlay

```css
.loading-overlay {
  background: rgba(0, 0, 0, 0.7);  /* Más oscuro */
  backdrop-filter: blur(8px);  /* Más blur */
}
```

## 🔧 Casos de Uso

### Caso 1: Loading Automático (Recomendado)
El sistema ya maneja automáticamente todas las peticiones HTTP.

### Caso 2: Loading Inline en Tablas
```html
<div class="table-container">
  <app-loading-spinner 
    [show]="loading"
    [isOverlay]="false"
    size="sm"
  ></app-loading-spinner>
  
  <table *ngIf="!loading">
    <!-- Tabla -->
  </table>
</div>
```

### Caso 3: Loading en Modales
```html
<div class="modal">
  <app-loading-spinner 
    [show]="saving"
    [isOverlay]="true"
    message="Guardando..."
  ></app-loading-spinner>
  
  <form>
    <!-- Formulario -->
  </form>
</div>
```

### Caso 4: Múltiples Loaders
```html
<!-- Loader global (automático) -->
<app-global-loading></app-global-loading>

<!-- Loader específico del componente -->
<app-loading-spinner 
  [show]="componentLoading"
  [isOverlay]="false"
></app-loading-spinner>
```

## ⚡ Performance

- **Ligero**: Componente minimalista
- **Eficiente**: Solo renderiza cuando `show=true`
- **Sin memoria**: Se destruye automáticamente
- **CSS puro**: Sin dependencias externas

## 🐛 Solución de Problemas

### El loader no aparece
- Verifica que `show=true`
- Revisa que el componente esté importado
- Checa la consola por errores

### El loader no desaparece
- Verifica que llamas a `hide()` o que la petición termine
- Revisa que no haya errores en la petición HTTP
- Usa `finalize()` en observables para garantizar que se oculte

### Múltiples loaders se superponen
- Usa `isOverlay=false` para loaders inline
- Usa el `LoadingService` para controlar uno global
- El interceptor ya maneja múltiples peticiones automáticamente

## 📊 Ventajas

1. **Automático**: No requiere código en componentes
2. **Reutilizable**: Un componente para todo
3. **Flexible**: Overlay o inline
4. **Personalizable**: Tamaños, mensajes, estilos
5. **Profesional**: Mejora la percepción de UX
6. **Inteligente**: Cuenta peticiones simultáneas

## LoadingButton

Botón con loader integrado para prevenir doble-click.

### 📋 Uso

```typescript
import { LoadingButtonComponent } from '../../shared/components/loading-button/loading-button.component';

@Component({
  imports: [LoadingButtonComponent]
})
```

```html
<app-loading-button
  [loading]="saving"
  [disabled]="form.invalid"
  loadingText="Guardando..."
  buttonClass="btn-primary"
  (clicked)="save()"
>
  Guardar Cambios
</app-loading-button>
```

### 🎯 Propiedades

- `loading` (boolean) - Si está en estado de carga
- `disabled` (boolean) - Si está deshabilitado
- `loadingText` (string) - Texto durante carga
- `buttonClass` (string) - Clases CSS del botón
- `type` ('button' | 'submit' | 'reset') - Tipo de botón
- `(clicked)` - Evento al hacer click

### 📱 Ejemplos

```html
<!-- Botón de guardar -->
<app-loading-button
  type="submit"
  [loading]="saving"
  loadingText="Guardando producto..."
  buttonClass="btn-primary"
>
  Guardar
</app-loading-button>

<!-- Botón de eliminar -->
<app-loading-button
  [loading]="deleting"
  loadingText="Eliminando..."
  buttonClass="btn-danger"
  (clicked)="delete()"
>
  Eliminar
</app-loading-button>

<!-- Botón secundario -->
<app-loading-button
  [loading]="processing"
  buttonClass="btn-secondary"
>
  Procesar
</app-loading-button>
```

---

**Sistema de loading completamente implementado** ✅

