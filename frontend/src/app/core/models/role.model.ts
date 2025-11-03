export interface Permission {
  id: number;
  code: string;
  name: string;
  description?: string;
  module: string;
  created_at: string;
}

export interface Role {
  id: number;
  business_id: number;
  name: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  permissions: Permission[];
}

export interface RoleCreate {
  name: string;
  description?: string;
  is_active?: boolean;
  permission_ids: number[];
}

export interface RoleUpdate {
  name?: string;
  description?: string;
  is_active?: boolean;
  permission_ids?: number[];
}

export interface UserRolesUpdate {
  role_ids: number[];
}

export interface UserRolesResponse {
  user_id: number;
  roles: Role[];
}

// Agrupación de permisos por módulo
export interface PermissionsByModule {
  [module: string]: Permission[];
}

// Módulos del sistema
export const SYSTEM_MODULES = [
  { code: 'dashboard', name: 'Dashboard', icon: '📊' },
  { code: 'products', name: 'Productos', icon: '🏷️' },
  { code: 'inventory', name: 'Inventario', icon: '📦' },
  { code: 'menu', name: 'Menú', icon: '🍽️' },
  { code: 'tables', name: 'Mesas', icon: '🪑' },
  { code: 'orders', name: 'Órdenes', icon: '📋' },
  { code: 'users', name: 'Usuarios', icon: '👥' },
  { code: 'configuration', name: 'Configuración', icon: '⚙️' },
  { code: 'reports', name: 'Reportes', icon: '📈' },
  { code: 'payment_methods', name: 'Métodos de Pago', icon: '💳' }
];

