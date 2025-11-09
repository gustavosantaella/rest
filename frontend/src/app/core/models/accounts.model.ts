export enum AccountStatus {
  PENDING = 'pending',
  PARTIAL = 'partial',
  PAID = 'paid',
  OVERDUE = 'overdue'
}

export interface AccountPayment {
  id: number;
  account_id: number;
  amount: number;
  payment_date: string;
  payment_method?: string;
  reference?: string;
  notes?: string;
  created_at: string;
}

export interface AccountPaymentCreate {
  amount: number;
  payment_method?: string;
  reference?: string;
  notes?: string;
}

// Cuentas por Cobrar
export interface AccountReceivable {
  id: number;
  business_id: number;
  customer_id?: number;
  invoice_number?: string;
  description: string;
  amount: number;
  amount_paid: number;
  amount_pending: number;
  issue_date: string;
  due_date: string;
  paid_date?: string;
  status: AccountStatus;
  notes?: string;
  created_at: string;
  updated_at?: string;
  payments: AccountPayment[];
  customer_name?: string;
}

export interface AccountReceivableCreate {
  customer_id?: number;
  invoice_number?: string;
  description: string;
  amount: number;
  due_date: string;
  notes?: string;
}

export interface AccountReceivableUpdate {
  customer_id?: number;
  invoice_number?: string;
  description?: string;
  amount?: number;
  due_date?: string;
  notes?: string;
  status?: string;
}

// Cuentas por Pagar
export interface AccountPayable {
  id: number;
  business_id: number;
  supplier_name: string;
  supplier_phone?: string;
  supplier_email?: string;
  invoice_number?: string;
  description: string;
  amount: number;
  amount_paid: number;
  amount_pending: number;
  issue_date: string;
  due_date: string;
  paid_date?: string;
  status: AccountStatus;
  notes?: string;
  created_at: string;
  updated_at?: string;
  payments: AccountPayment[];
}

export interface AccountPayableCreate {
  supplier_name: string;
  supplier_phone?: string;
  supplier_email?: string;
  invoice_number?: string;
  description: string;
  amount: number;
  due_date: string;
  notes?: string;
}

export interface AccountPayableUpdate {
  supplier_name?: string;
  supplier_phone?: string;
  supplier_email?: string;
  invoice_number?: string;
  description?: string;
  amount?: number;
  due_date?: string;
  notes?: string;
  status?: string;
}

export interface AccountsSummary {
  total_pending: number;
  total_overdue: number;
  count_pending: number;
  count_overdue: number;
}

