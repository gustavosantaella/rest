export enum UserRole {
  ADMIN = 'admin',
  MANAGER = 'manager',
  WAITER = 'waiter',
  CASHIER = 'cashier',
  CHEF = 'chef'  // Cocinero
}

export interface User {
  id: number;
  business_id?: number;
  username: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  dni?: string;
  country?: string;
  created_at: string;
  business_name?: string;  // Nombre del negocio al que pertenece
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface UserCreate {
  username: string;
  email: string;
  full_name: string;
  password: string;
  role: UserRole;
  dni?: string;
  country?: string;
}

export interface RegisterRequest {
  // Datos del usuario
  email: string;
  password: string;
  full_name: string;
  
  // Datos del negocio
  business_name: string;
  legal_name?: string;
  phone?: string;
}

export interface RegisterResponse {
  message: string;
  business_slug: string;
  user_email: string;
}

