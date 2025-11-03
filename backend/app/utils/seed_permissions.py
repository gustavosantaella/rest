"""
Permisos predefinidos del sistema
Estos permisos se crean automáticamente en la base de datos
"""

SYSTEM_PERMISSIONS = [
    # Dashboard
    {"code": "dashboard.view", "name": "Ver Dashboard", "module": "dashboard", "description": "Acceso al panel principal con estadísticas"},
    
    # Productos
    {"code": "products.view", "name": "Ver Productos", "module": "products", "description": "Ver lista de productos"},
    {"code": "products.create", "name": "Crear Productos", "module": "products", "description": "Crear nuevos productos"},
    {"code": "products.edit", "name": "Editar Productos", "module": "products", "description": "Modificar productos existentes"},
    {"code": "products.delete", "name": "Eliminar Productos", "module": "products", "description": "Eliminar productos"},
    
    # Inventario
    {"code": "inventory.view", "name": "Ver Inventario", "module": "inventory", "description": "Ver niveles de inventario"},
    {"code": "inventory.manage", "name": "Gestionar Inventario", "module": "inventory", "description": "Ajustar stock y niveles"},
    
    # Menú
    {"code": "menu.view", "name": "Ver Menú", "module": "menu", "description": "Ver items del menú"},
    {"code": "menu.create", "name": "Crear Items de Menú", "module": "menu", "description": "Agregar platillos al menú"},
    {"code": "menu.edit", "name": "Editar Menú", "module": "menu", "description": "Modificar items del menú"},
    {"code": "menu.delete", "name": "Eliminar Items", "module": "menu", "description": "Eliminar platillos del menú"},
    
    # Mesas
    {"code": "tables.view", "name": "Ver Mesas", "module": "tables", "description": "Ver estado de mesas"},
    {"code": "tables.manage", "name": "Gestionar Mesas", "module": "tables", "description": "Crear, editar y eliminar mesas"},
    
    # Órdenes
    {"code": "orders.view", "name": "Ver Órdenes", "module": "orders", "description": "Ver órdenes del sistema"},
    {"code": "orders.create", "name": "Crear Órdenes", "module": "orders", "description": "Crear nuevas órdenes"},
    {"code": "orders.edit", "name": "Editar Órdenes", "module": "orders", "description": "Modificar órdenes existentes"},
    {"code": "orders.delete", "name": "Cancelar Órdenes", "module": "orders", "description": "Cancelar órdenes"},
    {"code": "orders.change_status", "name": "Cambiar Estado", "module": "orders", "description": "Cambiar el estado de órdenes (pendiente, preparando, completada)"},
    {"code": "orders.process_payment", "name": "Procesar Pagos", "module": "orders", "description": "Registrar pagos de órdenes"},
    
    # Usuarios
    {"code": "users.view", "name": "Ver Usuarios", "module": "users", "description": "Ver lista de usuarios"},
    {"code": "users.create", "name": "Crear Usuarios", "module": "users", "description": "Crear nuevos usuarios"},
    {"code": "users.edit", "name": "Editar Usuarios", "module": "users", "description": "Modificar usuarios"},
    {"code": "users.delete", "name": "Eliminar Usuarios", "module": "users", "description": "Eliminar usuarios"},
    {"code": "users.manage_permissions", "name": "Gestionar Permisos", "module": "users", "description": "Asignar roles y permisos"},
    
    # Configuración
    {"code": "config.view", "name": "Ver Configuración", "module": "configuration", "description": "Ver configuración del negocio"},
    {"code": "config.edit", "name": "Editar Configuración", "module": "configuration", "description": "Modificar configuración"},
    {"code": "config.manage_roles", "name": "Gestionar Roles", "module": "configuration", "description": "Crear y editar roles personalizados"},
    {"code": "config.manage_permissions", "name": "Gestionar Permisos", "module": "configuration", "description": "Asignar permisos a roles"},
    
    # Reportes
    {"code": "reports.view", "name": "Ver Reportes", "module": "reports", "description": "Acceso a reportes básicos"},
    {"code": "reports.generate", "name": "Generar Reportes", "module": "reports", "description": "Generar reportes personalizados"},
    {"code": "reports.export", "name": "Exportar Reportes", "module": "reports", "description": "Exportar datos a Excel/PDF"},
    
    # Métodos de Pago
    {"code": "payment_methods.view", "name": "Ver Métodos de Pago", "module": "payment_methods", "description": "Ver métodos de pago disponibles"},
    {"code": "payment_methods.manage", "name": "Gestionar Métodos de Pago", "module": "payment_methods", "description": "Crear y editar métodos de pago"},
]


def get_permissions_by_module():
    """Agrupa permisos por módulo para mejor organización"""
    modules = {}
    for perm in SYSTEM_PERMISSIONS:
        module = perm["module"]
        if module not in modules:
            modules[module] = []
        modules[module].append(perm)
    return modules

