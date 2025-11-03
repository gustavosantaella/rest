# Directiva Tooltip

Directiva reutilizable para agregar tooltips/popovers informativos a cualquier elemento HTML.

## 📋 Uso Básico

```typescript
import { TooltipDirective } from '../../shared/directives/tooltip.directive';

@Component({
  imports: [TooltipDirective, ...]
})
```

```html
<input 
  type="text" 
  appTooltip="Este es el texto del tooltip"
  tooltipPosition="top"
/>
```

## 🎯 Propiedades

### `appTooltip` (string) - **Requerido**
Texto que se mostrará en el tooltip.

```html
<input appTooltip="Ingresa tu nombre completo" />
```

### `tooltipPosition` (string) - Opcional
Posición del tooltip relativa al elemento. Por defecto: `'top'`

Valores permitidos:
- `'top'` - Arriba del elemento
- `'bottom'` - Abajo del elemento
- `'left'` - Izquierda del elemento
- `'right'` - Derecha del elemento

```html
<input 
  appTooltip="Texto del tooltip"
  tooltipPosition="bottom"
/>
```

## 📱 Ejemplos de Uso

### Input de Texto
```html
<input 
  type="text" 
  formControlName="username"
  class="input-field"
  appTooltip="Nombre de usuario único, sin espacios"
  tooltipPosition="top"
/>
```

### Select
```html
<select 
  formControlName="category"
  class="input-field"
  appTooltip="Selecciona la categoría del producto"
  tooltipPosition="bottom"
>
  <option>Opción 1</option>
</select>
```

### Textarea
```html
<textarea 
  formControlName="description"
  rows="3"
  appTooltip="Descripción detallada del producto"
  tooltipPosition="right"
></textarea>
```

### Botones
```html
<button 
  type="button"
  appTooltip="Click para guardar los cambios"
  tooltipPosition="left"
>
  Guardar
</button>
```

## 🎨 Características

- ✅ **Automático**: Se muestra al pasar el mouse o hacer focus
- ✅ **Responsive**: Se adapta a la pantalla
- ✅ **Animado**: Transiciones suaves de entrada/salida
- ✅ **Accesible**: Funciona con teclado (focus/blur)
- ✅ **Limpio**: Se elimina automáticamente al destruir el componente
- ✅ **Estilizado**: Gradiente moderno con flecha indicadora

## 🎨 Personalización de Estilos

Los estilos del tooltip están en `src/styles.scss` bajo la clase `.custom-tooltip`.

Puedes personalizarlos modificando:

```scss
.custom-tooltip {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  max-width: 280px;
  // ... más estilos
}
```

## 🔧 Casos de Uso Comunes

### Formularios de Registro/Login
Explica qué debe ingresar el usuario en cada campo.

### Configuración de Productos
Ayuda a entender unidades de medida, precios, etc.

### Roles y Permisos
Clarifica qué puede hacer cada rol de usuario.

### Opciones Avanzadas
Explica configuraciones complejas de manera simple.

## ⚡ Performance

- **Ligero**: No impacta el rendimiento
- **Eficiente**: Se crea/destruye solo cuando es necesario
- **Sin memoria**: Limpia automáticamente los recursos

## 🐛 Solución de Problemas

### El tooltip no aparece
- Verifica que hayas importado `TooltipDirective` en el componente
- Asegúrate de que el texto no esté vacío
- Revisa que los estilos de `styles.scss` estén cargados

### El tooltip se corta
- Ajusta el `max-width` en los estilos
- Cambia la posición con `tooltipPosition`
- Verifica que haya espacio suficiente en la ventana

### Múltiples tooltips se superponen
- Esto no debería pasar, cada tooltip se elimina automáticamente
- Si ocurre, revisa la consola por errores

## 📄 Licencia

Parte del sistema de gestión para restaurantes/kioskos.

