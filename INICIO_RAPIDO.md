# ⚡ INICIO RÁPIDO - 2 Pasos

## 🎯 Para Usar el Sistema AHORA MISMO

### 📍 **Paso 1: Iniciar Backend**

```bash
# Abre una terminal en la carpeta del proyecto
cd backend

# Activa el entorno virtual
.venv\Scripts\activate

# Ejecutar
python run.py
```

**✅ Debes ver esto:**
```
✅ Usuario administrador creado:
   Usuario: admin
   Email: admin@admin.admin
   Password: 123456.Ab!

INFO:     Started server process [XXXX]
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**🔍 Verifica:** Abre http://localhost:8000 en tu navegador
- Si ves JSON con info de la API = ✅ Backend funcionando

### 📍 **Paso 2: Iniciar Frontend**

```bash
# Abre OTRA terminal (deja el backend corriendo)
cd frontend

# Ejecutar
npm start
```

**✅ Debes ver esto:**
```
✔ Compiled successfully.
** Angular Live Development Server is listening on localhost:4200 **
```

**🔍 Verifica:** Abre http://localhost:4200 en tu navegador
- Si ves la página de login = ✅ Frontend funcionando

### 📍 **Paso 3: Usar el Sistema**

```
1. Ir a: http://localhost:4200
2. Login:
   Usuario: admin
   Password: 123456.Ab!
3. ¡Listo! 🎉
```

---

## ⚠️ PROBLEMA COMÚN: "Loader se queda cargando"

### 🔍 Causa:
El **backend NO está corriendo**.

### ✅ Solución:
```bash
# En una terminal:
cd backend
.venv\Scripts\activate
python run.py

# Espera a que diga "Uvicorn running..."
# Luego recarga el frontend (F5)
```

---

## 🐛 Si Aún Hay Problemas

### El Backend No Inicia:

```bash
# Verificar que PostgreSQL esté corriendo
# Windows - Administrador de tareas → Servicios → postgresql

# Verificar que el .env esté configurado
cd backend
type .env  # Windows
cat .env   # Linux/Mac

# Reinstalar dependencias
pip install -r requirements.txt
```

### El Frontend No Compila:

```bash
# Reinstalar dependencias
cd frontend
rm -rf node_modules
npm install
npm start
```

### Loader Atascado:

```
1. Abre DevTools (F12)
2. Ve a la consola
3. Mira los logs 🔄 y ✅
4. Si el contador no llega a 0:
   - Presiona F5 para recargar
   - O ejecuta: localStorage.clear(); location.reload();
```

---

## 📊 Orden de Inicio Correcto

```
1️⃣ PostgreSQL (debe estar corriendo siempre)
2️⃣ Backend (python run.py)
3️⃣ Frontend (npm start)
4️⃣ Navegador (http://localhost:4200)
```

---

## 🎯 URLs Importantes

```
Backend:    http://localhost:8000
API Docs:   http://localhost:8000/docs
Health:     http://localhost:8000/health

Frontend:   http://localhost:4200
Login:      http://localhost:4200/login
Dashboard:  http://localhost:4200/dashboard
```

---

## 🔑 Credenciales

```
Usuario:  admin
Password: 123456.Ab!
```

---

## ✅ Checklist de Verificación

Antes de usar el sistema:

- [ ] PostgreSQL instalado y corriendo
- [ ] Base de datos `restaurant_db` creada
- [ ] Python 3.8+ instalado
- [ ] Node.js 18+ instalado
- [ ] Dependencias backend instaladas
- [ ] Dependencias frontend instaladas
- [ ] Backend corriendo (terminal 1)
- [ ] Frontend corriendo (terminal 2)
- [ ] Sin errores en consola

---

**¡Con esto deberías poder usar el sistema inmediatamente!** 🚀

Si tienes problemas, verifica primero que el backend esté corriendo.

