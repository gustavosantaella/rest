export interface Customer {
  id: number;
  business_id: number;
  nombre: string;
  apellido?: string | null;
  dni?: string | null;
  telefono?: string | null;
  correo?: string | null;
  created_at: string;
  updated_at?: string | null;
}

export interface CustomerCreate {
  nombre: string;
  apellido?: string;
  dni?: string;
  telefono?: string;
  correo?: string;
}

export interface CustomerUpdate {
  nombre?: string;
  apellido?: string;
  dni?: string;
  telefono?: string;
  correo?: string;
}

