# 🏗️ Arquitectura Limpia - Controller → Service → Repository

## 📋 Patrón Implementado

Tu aplicación ahora sigue el patrón **Repository Pattern** correctamente:

```
HTTP Request
    ↓
Controller (@Controller)
    ↓ [Maneja HTTP, validaciones de entrada]
Service (@Injectable)
    ↓ [Lógica de negocio, validaciones de dominio]
Repository (Class)
    ↓ [Solo queries de BD]
Base de Datos
```

---

## 🎯 Separación de Responsabilidades

### 1. **Controller** - Capa de Presentación

**Responsabilidad**: Manejar HTTP requests/responses

```python
@Controller("api/products")
class ProductsController:
    def __init__(self, products_service: ProductsService):
        self.products_service = products_service
    
    @Get("/")
    def get_products(
        self,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[ProductResponse]:
        # Solo pasar datos al servicio
        return self.products_service.get_products(
            current_user.business_id,
            skip,
            limit,
            db
        )
```

**✅ DEBE hacer:**
- Recibir parámetros HTTP
- Inyectar dependencias (db, user)
- Llamar al servicio
- Devolver response

**❌ NO debe hacer:**
- Queries de BD
- Lógica de negocio compleja
- Validaciones de dominio

---

### 2. **Service** - Capa de Lógica de Negocio

**Responsabilidad**: Validaciones y lógica de negocio

```python
@Injectable
class ProductsService:
    def create_product(
        self,
        product_data: ProductCreate,
        business_id: int,
        db: Session
    ) -> Product:
        product_repo = ProductRepository(db)
        category_repo = CategoryRepository(db)
        
        # VALIDACIÓN DE NEGOCIO
        category = category_repo.find_by_id(
            product_data.category_id,
            business_id
        )
        if not category:
            raise HTTPException(
                status_code=404,
                detail="Categoría no encontrada"
            )
        
        # LÓGICA DE NEGOCIO
        product_dict = product_data.model_dump()
        product_dict['business_id'] = business_id
        
        # DELEGAR AL REPOSITORIO
        return product_repo.create(product_dict)
```

**✅ DEBE hacer:**
- Validaciones de dominio
- Lógica de negocio
- Orquestar múltiples repositorios
- Lanzar excepciones de negocio

**❌ NO debe hacer:**
- Queries directas a BD (usar repository)
- Manejar HTTP requests/responses
- Crear objetos SQLAlchemy directamente

---

### 3. **Repository** - Capa de Acceso a Datos

**Responsabilidad**: SOLO queries de base de datos

```python
class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(
        self,
        product_id: int,
        business_id: int
    ) -> Optional[Product]:
        # SOLO la query
        return self.db.query(Product).filter(
            Product.id == product_id,
            Product.business_id == business_id,
            Product.deleted_at.is_(None)
        ).first()
    
    def create(self, product_data: dict) -> Product:
        # SOLO operaciones de BD
        product = Product(**product_data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
```

**✅ DEBE hacer:**
- Queries de BD
- CRUD básico
- Filtros de BD
- Commits y refreshes

**❌ NO debe hacer:**
- Validaciones de negocio
- Lanzar excepciones HTTP
- Lógica compleja
- Preparar datos (eso va en Service)

---

## 📊 Ejemplo Completo: Crear Producto

### 1. Controller recibe la petición:

```python
@Post("/", status_code=status.HTTP_201_CREATED)
def create_product(
    self,
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_manager)
) -> ProductResponse:
    # Solo pasar al servicio
    return self.products_service.create_product(
        product,
        current_user.business_id,
        db
    )
```

### 2. Service valida y procesa:

```python
def create_product(
    self,
    product_data: ProductCreate,
    business_id: int,
    db: Session
) -> Product:
    product_repo = ProductRepository(db)
    category_repo = CategoryRepository(db)
    
    # VALIDACIÓN: Categoría existe?
    category = category_repo.find_by_id(
        product_data.category_id,
        business_id
    )
    if not category:
        raise HTTPException(404, "Categoría no encontrada")
    
    # LÓGICA: Preparar datos
    product_dict = product_data.model_dump()
    product_dict['business_id'] = business_id
    
    # DELEGAR: Crear en BD
    return product_repo.create(product_dict)
```

### 3. Repository ejecuta la query:

```python
def create(self, product_data: dict) -> Product:
    # SOLO BD
    product = Product(**product_data)
    self.db.add(product)
    self.db.commit()
    self.db.refresh(product)
    return product
```

---

## 🎨 Estructura de Archivos

```
nest_modules/products/
├── products_controller.py       # HTTP + Routing
├── products_service.py          # Lógica de Negocio
├── products_repository.py       # Queries de BD
└── products_module.py           # Configuración PyNest
```

---

## ✅ Módulos con Repositorio Completo

Estos módulos YA siguen la arquitectura limpia:

1. ✅ **Products** - ProductRepository + CategoryRepository
2. ✅ **Customers** - CustomerRepository
3. ✅ **Users** - UserRepository + BusinessRepository
4. ✅ **Tables** - TableRepository
5. ✅ **Auth** - AuthRepository
6. ✅ **Profile** - ProfileRepository

---

## 🔄 Comparación

### ❌ ANTES (Service haciendo queries):

```python
@Injectable
class ProductsService:
    def get_products(self, business_id: int, db: Session):
        # ❌ MALO: Query directa en el servicio
        return db.query(Product).filter(
            Product.business_id == business_id
        ).all()
```

### ✅ DESPUÉS (Service usando Repository):

```python
@Injectable
class ProductsService:
    def get_products(self, business_id: int, db: Session):
        product_repo = ProductRepository(db)
        # ✅ BUENO: Delega al repositorio
        return product_repo.find_all(business_id, 0, 100)
```

---

## 🎯 Ventajas del Repository Pattern

### 1. **Testabilidad**
```python
# Fácil mockear el repository en tests
mock_repo = Mock(ProductRepository)
mock_repo.find_all.return_value = [producto1, producto2]
service = ProductsService()
```

### 2. **Reutilización**
```python
# Mismo repository usado por múltiples servicios
product_repo = ProductRepository(db)
order_service.validate_product(product_repo)
inventory_service.check_stock(product_repo)
```

### 3. **Mantenibilidad**
```python
# Cambiar la query en UN solo lugar
def find_all(self, business_id: int):
    # Agregar ordenamiento sin tocar el servicio
    return self.db.query(Product).filter(
        Product.business_id == business_id
    ).order_by(Product.created_at.desc()).all()
```

### 4. **Separación Clara**
```
Repository  → "Cómo se obtienen los datos" (queries)
Service     → "Qué hacer con los datos" (lógica)
Controller  → "Cómo presentar los datos" (HTTP)
```

---

## 📚 Métodos Típicos de un Repository

```python
class ProductRepository:
    # Búsqueda
    find_by_id(id, business_id) → Optional[Product]
    find_by_name(name, business_id) → Optional[Product]
    find_all(business_id, skip, limit) → List[Product]
    
    # Escritura
    create(product_data: dict) → Product
    update(product, update_data: dict) → Product
    
    # Eliminación
    delete(product) → None
    soft_delete(product) → None
    
    # Utilidades
    count(business_id) → int
    exists(id, business_id) → bool
```

---

## 🔍 Checklist de Validación

Para cada módulo, verifica:

### Controller:
- [ ] Solo tiene decoradores HTTP (@Get, @Post, etc.)
- [ ] Inyecta el servicio en __init__
- [ ] Pasa business_id del current_user al servicio
- [ ] No hace queries directas
- [ ] No tiene lógica de negocio compleja

### Service:
- [ ] Tiene decorador @Injectable
- [ ] Crea instancia del repository
- [ ] Contiene validaciones de dominio
- [ ] Orquesta múltiples repositorios si es necesario
- [ ] No hace queries directas (usa repository)
- [ ] Lanza HTTPException para errores

### Repository:
- [ ] Recibe Session en __init__
- [ ] Solo tiene métodos de BD (find, create, update, delete)
- [ ] No lanza HTTPException (eso va en Service)
- [ ] No tiene lógica de negocio
- [ ] Métodos nombrados semánticamente (find_by_id, find_all, etc.)

---

## 💡 Reglas de Oro

1. **Controller**: HTTP only
2. **Service**: Business logic only
3. **Repository**: Database only

4. **Controller** NO debe conocer la BD
5. **Repository** NO debe conocer HTTP
6. **Service** es el puente entre ambos

---

## 🚀 Próximos Pasos

Para migrar un módulo legacy a esta arquitectura:

1. Crear `nombre_repository.py`
2. Mover las queries del servicio al repository
3. Actualizar el servicio para usar el repository
4. Verificar que el controller solo llama al servicio

---

**Versión**: 2.0.0  
**Patrón**: Repository Pattern  
**Framework**: PyNest + FastAPI  
**Estado**: ✅ Implementado en 6 módulos

