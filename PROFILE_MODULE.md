# 👤 Módulo de Perfil Personal

## 🎯 Descripción

Módulo para que cada usuario pueda gestionar su propia información personal y cambiar su contraseña de forma segura.

## ✨ Características

### 📋 Información Personal
- **Nombre Completo**: Actualizar nombre
- **Correo Electrónico**: Cambiar email
- **DNI/Cédula**: Documento de identidad
- **País**: Nacionalidad o residencia
- **Usuario**: Solo lectura (no editable)
- **Rol**: Solo lectura (solo admin puede cambiar)

### 🔒 Cambio de Contraseña Seguro
- **Contraseña Actual**: Requerida por seguridad
- **Nueva Contraseña**: Mínimo 6 caracteres
- **Confirmar Contraseña**: Validación de coincidencia
- **Cierre de Sesión Automático**: Por seguridad después del cambio

## 🎨 Diseño

### Card de Perfil
```
┌────────────────────────────────┐
│ Información Personal           │
├────────────────────────────────┤
│ Nombre: [Juan Pérez García]   │
│ Email:  [juan@restaurant.com]  │
│ DNI:    [12345678]             │
│ País:   [Venezuela ▼]          │
│                                │
│ Usuario: juan_admin (bloqueado)│
│ Rol:     admin (bloqueado)     │
│                                │
│ [Guardar Cambios]              │
└────────────────────────────────┘
```

### Card de Cambio de Contraseña (Destacada)
```
┌────────────────────────────────┐
│ 🔒 Cambiar Contraseña          │
│ Actualiza tu contraseña...     │
├────────────────────────────────┤
│ Contraseña Actual: [••••••]    │
│ Nueva Contraseña:  [••••••]    │
│ Confirmar:         [••••••]    │
│                                │
│ [🔒 Cambiar Contraseña]        │
└────────────────────────────────┘
```

## 🔐 Seguridad

### Validaciones:

1. **Email Único**
   ```
   ✅ Verifica que no esté en uso por otro usuario
   ❌ No permite duplicados
   ```

2. **DNI Único**
   ```
   ✅ Verifica que no esté en uso por otro usuario
   ❌ No permite duplicados (si se ingresa)
   ```

3. **Contraseña Actual**
   ```
   ✅ Debe ingresar contraseña actual para cambiarla
   ❌ No permite cambio sin verificación
   ```

4. **Contraseñas Coinciden**
   ```
   ✅ Nueva contraseña y confirmación deben ser iguales
   ❌ Muestra error si no coinciden
   ```

5. **Longitud Mínima**
   ```
   ✅ Mínimo 6 caracteres
   ❌ No permite contraseñas débiles
   ```

## 🔄 Flujo de Uso

### Actualizar Perfil:
```
1. Click en Configuración (sidebar)
2. Click en "Mi Perfil"
3. Actualiza tus datos
4. Click "Guardar Cambios"
5. Página se recarga con datos actualizados ✅
```

### Cambiar Contraseña:
```
1. Ve a Mi Perfil
2. En la card de "Cambiar Contraseña":
   a. Ingresa contraseña actual
   b. Ingresa nueva contraseña
   c. Confirma nueva contraseña
3. Click "Cambiar Contraseña"
4. Sistema cierra sesión automáticamente
5. Vuelve a login con nueva contraseña ✅
```

## 💡 Características Especiales

### 1. Validación en Tiempo Real
```html
Confirmar Contraseña: [••••••]
❌ Las contraseñas no coinciden
```

### 2. Card Destacada para Contraseña
- Gradiente de fondo
- Borde azul
- Icono de candado
- Diseño visual que llama la atención

### 3. Consejos de Seguridad
```
💡 Consejos de Seguridad:
• Usa una contraseña única
• Incluye mayúsculas, minúsculas, números y símbolos
• Cambia tu contraseña periódicamente
• No compartas tu contraseña
• Si sospechas compromiso, cambia inmediatamente
```

### 4. Campos Bloqueados
- **Usuario**: No editable (identificador único)
- **Rol**: Solo admin puede cambiar

## 🎯 Acceso

### Dropdown en Sidebar:
```
⚙️ Configuración
   ↓ (click para expandir)
   ├─ 👤 Mi Perfil (TODOS)
   └─ 🏢 Negocio y Socios (solo ADMIN)
```

### Todos los usuarios pueden:
- ✅ Ver y editar su perfil
- ✅ Cambiar su contraseña

### Solo Admin puede:
- ✅ Ver configuración del negocio
- ✅ Gestionar socios

## 📊 Campos del Perfil

| Campo | Requerido | Editable | Validación |
|-------|-----------|----------|------------|
| Nombre Completo | ✅ Sí | ✅ Sí | Texto no vacío |
| Email | ✅ Sí | ✅ Sí | Formato email, único |
| DNI | ❌ No | ✅ Sí | Único si se ingresa |
| País | ❌ No | ✅ Sí | Selección de lista |
| Usuario | N/A | ❌ No | Solo lectura |
| Rol | N/A | ❌ No | Solo lectura |

## 🌍 Países Disponibles

- Venezuela
- Colombia
- México
- Argentina
- Chile
- Perú
- Ecuador
- Bolivia
- Uruguay
- Paraguay
- España
- Estados Unidos

## 🔒 Cambio de Contraseña

### Proceso:
```python
1. Usuario ingresa contraseña actual
   ↓
2. Backend verifica con bcrypt
   ↓
3. Si es correcta:
   - Hash nueva contraseña
   - Actualizar en BD
   - Retornar éxito
   ↓
4. Frontend cierra sesión
   ↓
5. Usuario debe login con nueva contraseña
```

### API Endpoint:
```
POST /api/profile/change-password

Body:
{
  "current_password": "contraseña_actual",
  "new_password": "nueva_contraseña"
}

Respuesta Éxito:
{
  "message": "Contraseña actualizada exitosamente"
}

Respuesta Error:
{
  "detail": "La contraseña actual es incorrecta"
}
```

## 💻 Implementación Técnica

### Backend:
```python
@router.post("/change-password")
def change_password(password_data: PasswordChange, current_user: User):
    # 1. Verificar contraseña actual
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(400, "Contraseña actual incorrecta")
    
    # 2. Actualizar contraseña
    current_user.hashed_password = get_password_hash(password_data.new_password)
    
    # 3. Guardar
    db.commit()
    
    return {"message": "Contraseña actualizada"}
```

### Frontend:
```typescript
changePassword() {
  this.profileService.changePassword(passwords).subscribe({
    next: () => {
      alert('Contraseña cambiada. Inicia sesión nuevamente.');
      this.authService.logout();  // Cerrar sesión por seguridad
    },
    error: (err) => {
      alert('Error: ' + err.error.detail);
    }
  });
}
```

## 🎨 Diseño Visual

### Perfil Normal:
- Card blanca estándar
- Campos de formulario
- Botón azul "Guardar Cambios"

### Cambio de Contraseña:
- Card con **gradiente azul** (from-primary-50 to-white)
- **Borde azul** destacado (border-primary-100)
- **Icono de candado** grande
- Diseño que llama la atención
- Consejos de seguridad abajo

## ✅ Ventajas

1. **Autonomía**: Usuarios actualizan su propia info
2. **Seguridad**: Cambio de contraseña seguro
3. **Privacidad**: Solo ven su propia información
4. **Accesibilidad**: Todos los usuarios pueden acceder
5. **Validación**: Previene datos duplicados o inválidos

## 🚀 Uso Práctico

### Ejemplo 1: Actualizar Email
```
Juan inicia como: juan@gmail.com
Consigue email corporativo
1. Va a Mi Perfil
2. Cambia a: juan@restaurant.com
3. Guarda
4. Ahora usa el email corporativo ✅
```

### Ejemplo 2: Cambiar Contraseña
```
María olvidó su contraseña anterior
Admin le da una temporal: temp123
1. María hace login con temp123
2. Va a Mi Perfil → Cambiar Contraseña
3. Actual: temp123
4. Nueva: MiPasswordSegura2024!
5. Confirma y guarda
6. Sistema la desloguea
7. Login con nueva contraseña ✅
```

### Ejemplo 3: Actualizar DNI
```
Pedro no había ingresado su DNI
1. Va a Mi Perfil
2. Ingresa DNI: 98765432
3. Selecciona País: Venezuela
4. Guarda
5. Info completa en el sistema ✅
```

## 📱 Navegación

### Sidebar (Todos los Usuarios):
```
⚙️ Configuración ▼
   ├─ 👤 Mi Perfil
   └─ 🏢 Negocio y Socios (solo Admin)
```

### URLs:
```
Perfil:  http://localhost:4200/profile
Negocio: http://localhost:4200/configuration/business
```

## 🎯 Próximas Mejoras

- [ ] Avatar/foto de perfil
- [ ] Firma digital
- [ ] Configuración de notificaciones
- [ ] Preferencias de idioma
- [ ] Tema oscuro/claro
- [ ] Autenticación de dos factores (2FA)
- [ ] Historial de cambios de contraseña
- [ ] Recuperación de contraseña por email

---

**Módulo de Perfil completamente implementado** ✅

Características:
- ✅ Edición de información personal
- ✅ Cambio de contraseña seguro
- ✅ Dropdown en sidebar
- ✅ Validaciones completas
- ✅ Diseño moderno
- ✅ Tooltips informativos

