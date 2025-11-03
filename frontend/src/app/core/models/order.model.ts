export enum OrderStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
  PAID = 'paid'
}

export enum PaymentMethod {
  CASH = 'cash',
  CARD = 'card',
  TRANSFER = 'transfer',
  MIXED = 'mixed'
}

export interface OrderItem {
  id: number;
  product_id: number;
  quantity: number;
  unit_price: number;
  subtotal: number;
  notes?: string;
  created_at: string;
}

export interface Order {
  id: number;
  table_id?: number;
  user_id: number;
  status: OrderStatus;
  payment_method?: PaymentMethod;
  subtotal: number;
  tax: number;
  discount: number;
  total: number;
  notes?: string;
  created_at: string;
  paid_at?: string;
  items: OrderItem[];
}

export interface OrderItemCreate {
  product_id: number;
  quantity: number;
  notes?: string;
}

export interface OrderCreate {
  table_id?: number;
  notes?: string;
  items: OrderItemCreate[];
}

