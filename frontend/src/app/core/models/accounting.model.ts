/**
 * Modelos para el módulo contable
 */

export enum AccountType {
  ASSET = 'asset',
  LIABILITY = 'liability',
  EQUITY = 'equity',
  REVENUE = 'revenue',
  EXPENSE = 'expense',
  COST_OF_SALES = 'cost_of_sales'
}

export enum AccountNature {
  DEBIT = 'debit',
  CREDIT = 'credit'
}

export enum JournalEntryStatus {
  DRAFT = 'draft',
  POSTED = 'posted',
  REVERSED = 'reversed'
}

export interface ChartOfAccounts {
  id: number;
  business_id: number;
  code: string;
  name: string;
  description?: string;
  account_type: AccountType;
  nature: AccountNature;
  parent_id?: number;
  level: number;
  allows_manual_entries: boolean;
  is_active: boolean;
  is_system: boolean;
  initial_balance: number;
  initial_balance_date?: string;
  created_at: string;
  updated_at?: string;
  children?: ChartOfAccounts[];
}

export interface ChartOfAccountsCreate {
  code: string;
  name: string;
  description?: string;
  account_type: AccountType;
  nature: AccountNature;
  parent_id?: number;
  level?: number;
  allows_manual_entries?: boolean;
  is_active?: boolean;
  initial_balance?: number;
  initial_balance_date?: string;
}

export interface JournalEntryLine {
  id: number;
  entry_id: number;
  account_id: number;
  debit: number;
  credit: number;
  description?: string;
  reference?: string;
  cost_center_id?: number;
  created_at: string;
  account_code?: string;
  account_name?: string;
}

export interface JournalEntryLineCreate {
  account_id: number;
  debit: number;
  credit: number;
  description?: string;
  reference?: string;
  cost_center_id?: number;
}

export interface JournalEntry {
  id: number;
  business_id: number;
  entry_number: string;
  entry_date: string;
  reference?: string;
  description: string;
  status: JournalEntryStatus;
  posted_at?: string;
  posted_by?: number;
  reversed_entry_id?: number;
  is_reversal: boolean;
  period_id?: number;
  created_by: number;
  created_at: string;
  updated_at?: string;
  lines: JournalEntryLine[];
  total_debit: number;
  total_credit: number;
}

export interface JournalEntryCreate {
  entry_date: string;
  reference?: string;
  description: string;
  period_id?: number;
  lines: JournalEntryLineCreate[];
}

export interface AccountingPeriod {
  id: number;
  business_id: number;
  name: string;
  start_date: string;
  end_date: string;
  is_closed: boolean;
  closed_at?: string;
  closed_by?: number;
  created_at: string;
  updated_at?: string;
}

export interface AccountingPeriodCreate {
  name: string;
  start_date: string;
  end_date: string;
}

export interface CostCenter {
  id: number;
  business_id: number;
  code: string;
  name: string;
  description?: string;
  parent_id?: number;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  children?: CostCenter[];
}

export interface CostCenterCreate {
  code: string;
  name: string;
  description?: string;
  parent_id?: number;
  is_active?: boolean;
}

export interface GeneralLedger {
  id: number;
  business_id: number;
  account_id: number;
  account_code?: string;
  account_name?: string;
  period_id?: number;
  entry_date: string;
  entry_id: number;
  entry_number?: string;
  debit: number;
  credit: number;
  balance_debit: number;
  balance_credit: number;
  description?: string;
  reference?: string;
  created_at: string;
}

export interface TrialBalance {
  account_id: number;
  account_code: string;
  account_name: string;
  account_type: AccountType;
  initial_balance: number;
  debit: number;
  credit: number;
  final_balance_debit: number;
  final_balance_credit: number;
}

export interface FinancialStatementLine {
  account_code: string;
  account_name: string;
  amount: number;
  level: number;
  is_total: boolean;
}

export interface BalanceSheet {
  assets: FinancialStatementLine[];
  liabilities: FinancialStatementLine[];
  equity: FinancialStatementLine[];
  total_assets: number;
  total_liabilities: number;
  total_equity: number;
  date: string;
}

export interface IncomeStatement {
  revenue: FinancialStatementLine[];
  cost_of_sales: FinancialStatementLine[];
  expenses: FinancialStatementLine[];
  total_revenue: number;
  total_cost_of_sales: number;
  gross_profit: number;
  total_expenses: number;
  net_income: number;
  period_start: string;
  period_end: string;
}

