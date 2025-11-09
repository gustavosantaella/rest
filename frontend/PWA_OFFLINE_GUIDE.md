# Guía de PWA y Funcionalidad Offline

## 🚀 Características

Tu aplicación ahora es una **Progressive Web App (PWA)** con las siguientes capacidades:

### ✨ Instalación en Desktop/Móvil
- La app se puede instalar como aplicación nativa en computadoras y dispositivos móviles
- Funciona con ícono propio en el escritorio o pantalla de inicio
- Se abre en su propia ventana sin la barra de navegación del navegador

### 🔌 Funcionalidad Offline
- La aplicación funciona sin conexión a internet
- Los datos se guardan localmente cuando no hay conexión
- Al recuperar la conexión, los datos se sincronizan automáticamente con el servidor

### 🔄 Sincronización Automática
- Detección automática del estado de conexión
- Sincronización en segundo plano cada 30 segundos
- Notificaciones visuales del estado de sincronización
- Contador de operaciones pendientes de sincronizar

## 📱 Cómo Instalar la Aplicación

### En Chrome/Edge (Desktop)
1. Abre la aplicación en tu navegador
2. Busca el ícono de instalación ➕ en la barra de direcciones (derecha)
3. Click en "Instalar"
4. La app se instalará como aplicación de escritorio

### En Chrome/Edge (Android)
1. Abre la aplicación en Chrome
2. Toca el menú (⋮) en la esquina superior derecha
3. Selecciona "Agregar a pantalla de inicio" o "Instalar aplicación"
4. Confirma la instalación

### En Safari (iOS)
1. Abre la aplicación en Safari
2. Toca el botón de compartir (□↑)
3. Selecciona "Agregar a pantalla de inicio"
4. Dale un nombre y confirma

## 🔄 Uso Offline

### Funcionamiento Automático
La aplicación detecta automáticamente cuando pierdes la conexión y:

1. **Muestra un indicador** en la esquina inferior derecha con el estado de conexión
2. **Guarda todas las operaciones** localmente en IndexedDB
3. **Permite seguir trabajando** con normalidad
4. **Sincroniza automáticamente** cuando recuperas la conexión

### Operaciones Soportadas en Modo Offline

#### ✅ Completamente Soportadas:
- **Crear órdenes**: Las órdenes se guardan localmente y se envían al servidor al reconectar
- **Actualizar items de órdenes**: Los cambios se guardan para sincronización posterior
- **Procesar pagos**: Los pagos se almacenan y sincronizan cuando hay conexión
- **Actualizar estado de mesas**: Los cambios se guardan localmente

#### 📖 Solo Lectura (con caché):
- Ver productos del inventario
- Ver items del menú
- Ver órdenes existentes
- Ver mesas

### Indicador de Conexión

El indicador en la esquina inferior derecha muestra:

- 🟢 **En línea**: Conectado al servidor, todo funcionando normalmente
- 🔄 **Sincronizando**: Enviando datos pendientes al servidor
- 🔴 **Sin conexión**: Modo offline, los datos se guardarán localmente
- **Contador**: Número de operaciones pendientes de sincronizar

#### Interacción con el Indicador:
- **Click**: Abre/cierra el panel de detalles
- **Panel de detalles**: Muestra información completa del estado
- **Botón "Sincronizar ahora"**: Fuerza una sincronización inmediata (solo si hay conexión)

## 🛠️ Aspectos Técnicos

### Service Worker
- Cachea automáticamente la aplicación para uso offline
- Gestiona el caché de datos maestros (productos, menú, etc.)
- Estrategia de caché:
  - **Freshness**: Para datos maestros (intenta red primero, luego caché)
  - **Performance**: Para datos transaccionales (caché primero, luego red)

### IndexedDB
- Base de datos local en el navegador
- Almacena operaciones pendientes de sincronización
- Caché de datos para acceso offline
- Límite de almacenamiento: Depende del navegador (típicamente 50MB+)

### Sincronización
- **Automática**: Cada 30 segundos si hay conexión
- **Manual**: Click en "Sincronizar ahora" en el indicador
- **Reintentos**: Máximo 3 intentos por operación
- **Notificaciones**: Informa del éxito o falla de sincronización

## 🔒 Seguridad

### Datos Sensibles
- El token de autenticación se mantiene en localStorage
- Los datos offline se almacenan en IndexedDB del navegador
- Solo accesibles desde el mismo origen (dominio)
- Se eliminan al cerrar sesión

### Limitaciones en Modo Offline
- No se pueden crear nuevos usuarios
- No se puede modificar la configuración del negocio
- No se puede gestionar roles y permisos
- Funciones administrativas requieren conexión

## 📊 Monitoreo y Depuración

### Consola del Navegador
Puedes ver logs detallados en la consola del navegador:
```javascript
// Estado de conexión
console.log(navigator.onLine);

// Ver datos en IndexedDB
// Chrome DevTools > Application > Storage > IndexedDB > RestaurantPOS
```

### Chrome DevTools
1. Abre DevTools (F12)
2. Pestaña **Application**
3. **Service Workers**: Ver estado del service worker
4. **Storage > IndexedDB**: Inspeccionar datos locales
5. **Cache Storage**: Ver archivos cacheados
6. **Network**: Simular offline (dropdown en la esquina superior)

## ⚙️ Configuración Avanzada

### Modificar Tiempo de Sincronización
En `frontend/src/app/core/services/sync.service.ts`:
```typescript
// Cambiar 30000 (30 segundos) por el valor deseado en milisegundos
this.syncInterval = setInterval(() => {
  if (this.isOnline() && !this.syncInProgress) {
    this.syncPendingData();
  }
}, 30000);  // <-- Modificar aquí
```

### Modificar TTL del Caché
En `frontend/src/app/core/services/indexed-db.service.ts`:
```typescript
const cacheEntry = {
  key,
  data,
  timestamp: Date.now(),
  ttl: ttl || (1000 * 60 * 60) // <-- Modificar aquí (en milisegundos)
};
```

### Agregar Más URLs al Service Worker
En `frontend/ngsw-config.json`:
```json
{
  "dataGroups": [
    {
      "name": "api-new-endpoint",
      "urls": [
        "/api/new-endpoint/**"
      ],
      "cacheConfig": {
        "strategy": "freshness",
        "maxSize": 100,
        "maxAge": "1h",
        "timeout": "5s"
      }
    }
  ]
}
```

## 🐛 Troubleshooting

### La app no se puede instalar
- Verifica que estés usando HTTPS (o localhost)
- Asegúrate de que el service worker esté registrado (DevTools > Application > Service Workers)
- Limpia el caché del navegador y recarga

### Los datos no se sincronizan
- Verifica el indicador de conexión
- Abre la consola y busca errores
- Verifica que el backend esté funcionando
- Revisa las operaciones pendientes en DevTools > Application > IndexedDB

### El service worker no se actualiza
- En Chrome DevTools > Application > Service Workers
- Click en "Update" para forzar actualización
- O marca "Update on reload"

### Limpiar todos los datos offline
En la consola del navegador:
```javascript
// Eliminar IndexedDB
indexedDB.deleteDatabase('RestaurantPOS');

// Eliminar caché del service worker
caches.keys().then(keys => keys.forEach(key => caches.delete(key)));

// Desregistrar service worker
navigator.serviceWorker.getRegistrations().then(registrations => {
  registrations.forEach(registration => registration.unregister());
});

// Recargar la página
location.reload();
```

## 📝 Notas Importantes

1. **Primera carga**: Requiere conexión para cargar datos iniciales
2. **Imágenes**: Las imágenes de productos se cachean automáticamente
3. **Actualizaciones**: El service worker se actualiza automáticamente al desplegar nueva versión
4. **Límites**: IndexedDB tiene límites de almacenamiento según el navegador
5. **Privacidad**: Los datos se almacenan solo en el dispositivo, no se comparten entre dispositivos

## 🎯 Mejores Prácticas

1. **Sincroniza regularmente**: No dejes muchas operaciones pendientes
2. **Verifica el indicador**: Antes de cerrar la app, asegúrate de que no haya operaciones pendientes
3. **Conexión estable**: Para operaciones importantes, usa conexión estable
4. **Respaldo**: Los datos más importantes deberían respaldarse en el servidor
5. **Cierre de sesión**: Al cerrar sesión, los datos offline se mantienen hasta la siguiente sesión

## 📞 Soporte

Si encuentras problemas:
1. Revisa esta guía
2. Consulta la consola del navegador
3. Verifica el estado en Chrome DevTools
4. Contacta al equipo de desarrollo con capturas de pantalla y mensajes de error

