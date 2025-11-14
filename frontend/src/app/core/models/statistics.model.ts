export interface GeneralStatistics {
  period_days: number;
  total_orders: number;
  completed_orders: number;
  cancelled_orders: number;
  total_revenue: number;
  average_ticket: number;
  orders_by_day: { [date: string]: number };
  revenue_by_day: { [date: string]: number };
  total_receivable: number;
  total_payable: number;
  net_balance: number;
}

export interface ProductSales {
  id: number;
  name: string;
  quantity: number;
  total_sales: number;
}

export interface BestSellersStatistics {
  period_days: number;
  best_products: ProductSales[];
  best_menu_items: ProductSales[];
  worst_products: ProductSales[];
}

export interface CustomerDebt {
  id: number;
  name: string;
  accounts_count: number;
  total_pending: number;
}

export interface CustomerStatistics {
  total_customers: number;
  new_customers_last_30_days: number;
  customers_with_debt: CustomerDebt[];
  total_debt_from_customers: number;
}

export interface FinancialStatistics {
  period_days: number;
  total_income: number;
  total_expenses: number;
  net_profit: number;
  income_by_method: { [method: string]: number };
  total_pending_income?: number;
  total_pending_expenses?: number;
  projected_balance: number;
  profit_margin: number;
}

