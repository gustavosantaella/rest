export interface Partner {
  id: number;
  business_config_id: number;
  user_id: number;
  participation_percentage: number;
  investment_amount: number;
  join_date: string;
  is_active: boolean;
  notes?: string;
  created_at: string;
  updated_at?: string;
  user_name?: string;
  user_email?: string;
}

export interface BusinessType {
  id: number;
  name: string;
  slug: string;
  description?: string;
  has_menu: boolean;
  has_tables: boolean;
  has_ingredients: boolean;
  has_menu_statistics: boolean;
  has_product_statistics: boolean;
}

export interface BusinessConfiguration {
  id: number;
  business_name: string;
  slug?: string;
  legal_name?: string;
  rif?: string;
  phone?: string;
  email?: string;
  address?: string;
  tax_rate: number;
  currency: string;
  logo_url?: string;
  business_type_id?: number;
  business_type?: BusinessType;
  created_at: string;
  updated_at?: string;
  partners: Partner[];
}

export interface BusinessConfigurationCreate {
  business_name: string;
  slug?: string;
  legal_name?: string;
  rif?: string;
  phone?: string;
  email?: string;
  address?: string;
  tax_rate?: number;
  currency?: string;
  logo_url?: string;
  business_type_id?: number;
}

export interface PartnerCreate {
  user_id: number;
  participation_percentage: number;
  investment_amount?: number;
  join_date?: string;
  is_active?: boolean;
  notes?: string;
}

