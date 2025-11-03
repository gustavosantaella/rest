export interface UserPermission {
  id: number;
  user_id: number;
  can_access_dashboard: boolean;
  can_access_inventory: boolean;
  can_access_products: boolean;
  can_access_menu: boolean;
  can_access_tables: boolean;
  can_access_orders: boolean;
  can_access_users: boolean;
  can_access_configuration: boolean;
  can_access_reports: boolean;
  created_at: string;
  updated_at?: string;
}

export interface PermissionUpdate {
  can_access_dashboard?: boolean;
  can_access_inventory?: boolean;
  can_access_products?: boolean;
  can_access_menu?: boolean;
  can_access_tables?: boolean;
  can_access_orders?: boolean;
  can_access_users?: boolean;
  can_access_configuration?: boolean;
  can_access_reports?: boolean;
}

export interface PermissionModule {
  key: keyof Omit<UserPermission, 'id' | 'user_id' | 'created_at' | 'updated_at'>;
  label: string;
  description: string;
  icon: string;
}

export const PERMISSION_MODULES: PermissionModule[] = [
  {
    key: 'can_access_dashboard',
    label: 'Dashboard',
    description: 'Acceso al panel principal',
    icon: '📊'
  },
  {
    key: 'can_access_inventory',
    label: 'Inventario',
    description: 'Gestión de inventario',
    icon: '📦'
  },
  {
    key: 'can_access_products',
    label: 'Productos',
    description: 'Gestión de productos',
    icon: '🏷️'
  },
  {
    key: 'can_access_menu',
    label: 'Menú',
    description: 'Gestión del menú',
    icon: '🍽️'
  },
  {
    key: 'can_access_tables',
    label: 'Mesas',
    description: 'Gestión de mesas',
    icon: '🪑'
  },
  {
    key: 'can_access_orders',
    label: 'Órdenes',
    description: 'Gestión de órdenes',
    icon: '📋'
  },
  {
    key: 'can_access_users',
    label: 'Usuarios',
    description: 'Gestión de usuarios',
    icon: '👥'
  },
  {
    key: 'can_access_configuration',
    label: 'Configuración',
    description: 'Configuración del negocio',
    icon: '⚙️'
  },
  {
    key: 'can_access_reports',
    label: 'Reportes',
    description: 'Acceso a reportes',
    icon: '📈'
  }
];

