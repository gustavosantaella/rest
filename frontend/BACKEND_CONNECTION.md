# 🔌 Guía de Conexión Backend

## ⚠️ Error Común: "Backend no disponible"

Si ves este mensaje en la consola:
```
⚠️ Backend no disponible. Manteniendo sesión local.
⚠️ Error de red detectado. Verifica que el backend esté corriendo en: http://localhost:8000/api/...
```

## 🔍 Causas

1. **Backend no está corriendo** ✅ (Más común)
2. **Puerto incorrecto** en configuración
3. **CORS no configurado** correctamente
4. **Firewall bloqueando** la conexión
5. **URL incorrecta** en environment.ts

## ✅ Solución Rápida

### Paso 1: Verificar Backend

```bash
cd backend

# Asegúrate de tener el entorno virtual activado
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Ejecutar backend
python run.py
```

**Deberías ver:**
```
✅ Usuario administrador creado:
   Usuario: admin
   Email: admin@admin.admin
   Password: 123456.Ab!

INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Paso 2: Verificar que Responde

Abre en tu navegador:
```
http://localhost:8000
```

Deberías ver:
```json
{
  "message": "Sistema de Gestión para Restaurante/Kiosko API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### Paso 3: Verificar CORS

Si el backend está corriendo pero aún hay errores de red, verifica en `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # ✅ Puerto del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Paso 4: Verificar URL en Frontend

Archivo: `frontend/src/environments/environment.ts`

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'  // ✅ Debe coincidir con el backend
};
```

## 🔧 Diagnóstico Avanzado

### Test 1: Ping al Backend
```bash
curl http://localhost:8000
# Debe retornar JSON con información de la API
```

### Test 2: Verificar Puerto
```bash
# Linux/Mac
lsof -i :8000

# Windows
netstat -ano | findstr :8000
```

### Test 3: Test de Autenticación
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -F "username=admin" \
  -F "password=123456.Ab!"
```

Debería retornar:
```json
{
  "access_token": "eyJ0eXAiOiJKV1...",
  "token_type": "bearer"
}
```

### Test 4: Verificar Base de Datos

```bash
# Entrar a PostgreSQL
psql -U postgres

# Ver bases de datos
\l

# Conectar a la base de datos
\c restaurant_db

# Ver tablas
\dt

# Salir
\q
```

## 🐛 Errores Específicos y Soluciones

### Error: "Connection refused"
```
❌ Problema: Backend no está corriendo
✅ Solución: Ejecuta python run.py
```

### Error: "CORS policy"
```
❌ Problema: CORS no configurado
✅ Solución: Verifica allow_origins en main.py
```

### Error: "ERR_NAME_NOT_RESOLVED"
```
❌ Problema: URL incorrecta
✅ Solución: Verifica environment.ts
```

### Error: "504 Gateway Timeout"
```
❌ Problema: Backend muy lento o bloqueado
✅ Solución: Reinicia el backend
```

### Error: "Cannot connect to database"
```
❌ Problema: PostgreSQL no está corriendo
✅ Solución: 
# Linux
sudo service postgresql start

# Mac
brew services start postgresql

# Windows
net start postgresql-x64-14
```

## ✅ Checklist de Verificación

- [ ] PostgreSQL está corriendo
- [ ] Base de datos `restaurant_db` existe
- [ ] Entorno virtual de Python está activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` configurado correctamente
- [ ] Backend corriendo en http://localhost:8000
- [ ] Frontend corriendo en http://localhost:4200
- [ ] CORS configurado para localhost:4200
- [ ] No hay firewall bloqueando puertos

## 🎯 Configuración Recomendada

### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/restaurant_db
SECRET_KEY=tu-clave-secreta-super-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (environment.ts)
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

### Puertos por Defecto
```
Backend:  8000
Frontend: 4200
PostgreSQL: 5432
```

## 🔄 Reinicio Completo (Si Nada Funciona)

```bash
# 1. Detener todo
Ctrl+C en backend
Ctrl+C en frontend

# 2. Reiniciar PostgreSQL
sudo service postgresql restart  # Linux
brew services restart postgresql  # Mac

# 3. Backend
cd backend
source venv/bin/activate
python run.py

# 4. Frontend (en otra terminal)
cd frontend
npm start

# 5. Verificar
# Backend: http://localhost:8000
# Frontend: http://localhost:4200
```

## 💡 Modo Desarrollo Sin Backend

Si necesitas trabajar en el frontend sin backend:

```typescript
// Comentar temporalmente en main.ts
provideHttpClient(
  // withInterceptors([loadingInterceptor, authInterceptor])
)

// Y en auth.guard.ts, comentar temporalmente:
export const authGuard: CanActivateFn = () => {
  return true; // Permitir acceso sin autenticación (solo desarrollo)
};
```

⚠️ **No olvides descomentarlo después**

## 📞 Ayuda Rápida

### ¿El backend está corriendo?
```bash
curl http://localhost:8000/health
# Debe retornar: {"status":"healthy"}
```

### ¿El frontend puede conectarse?
Abre la consola del navegador (F12) y ejecuta:
```javascript
fetch('http://localhost:8000/api/users/me', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
  }
})
.then(r => r.json())
.then(console.log)
```

### ¿Hay problemas de CORS?
Busca en la consola del navegador errores que mencionen "CORS" o "Access-Control-Allow-Origin".

## 🎯 Estado Esperado

Cuando todo funciona correctamente:

**Consola del Backend:**
```
✅ Usuario administrador creado:
   Usuario: admin
   Email: admin@admin.admin
   Password: 123456.Ab!

INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Consola del Frontend:**
```
** Angular Live Development Server is listening on localhost:4200 **
✔ Compiled successfully.
```

**Consola del Navegador:**
```
Sin errores (o solo warnings menores)
```

---

**Si sigues teniendo problemas, asegúrate de que el backend esté corriendo primero** ✅

