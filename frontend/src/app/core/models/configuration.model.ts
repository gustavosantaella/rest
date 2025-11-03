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

export interface BusinessConfiguration {
  id: number;
  business_name: string;
  legal_name?: string;
  rif?: string;
  phone?: string;
  email?: string;
  address?: string;
  tax_rate: number;
  currency: string;
  logo_url?: string;
  created_at: string;
  updated_at?: string;
  partners: Partner[];
}

export interface BusinessConfigurationCreate {
  business_name: string;
  legal_name?: string;
  rif?: string;
  phone?: string;
  email?: string;
  address?: string;
  tax_rate?: number;
  currency?: string;
  logo_url?: string;
}

export interface PartnerCreate {
  user_id: number;
  participation_percentage: number;
  investment_amount?: number;
  join_date?: string;
  is_active?: boolean;
  notes?: string;
}

