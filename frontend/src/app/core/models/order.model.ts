export enum OrderStatus {
  PENDING = 'pending',       // Pendiente
  PREPARING = 'preparing',   // Preparando
  COMPLETED = 'completed',   // Completada
  CANCELLED = 'cancelled'    // Cancelada
}

export enum PaymentMethod {
  CASH = 'cash',
  CARD = 'card',
  TRANSFER = 'transfer',
  MIXED = 'mixed'
}

export enum PaymentStatus {
  PENDING = 'pending',
  PARTIAL = 'partial',
  PAID = 'paid'
}

export interface OrderPayment {
  id?: number;
  order_id?: number;
  payment_method_id: number;
  payment_method_name?: string;
  amount: number;
  reference?: string;
}

export interface OrderPaymentCreate {
  payment_method_id: number;
  amount: number;
  reference?: string;
}

export interface OrderItem {
  id: number;
  product_id?: number;
  menu_item_id?: number;
  source_type?: string;
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
  payment_status: PaymentStatus;
  subtotal: number;
  tax: number;
  discount: number;
  total: number;
  customer_name?: string;
  customer_email?: string;
  customer_phone?: string;
  notes?: string;
  created_at: string;
  paid_at?: string;
  items: OrderItem[];
  payments: OrderPayment[];
}

export interface OrderItemCreate {
  product_id?: number;
  menu_item_id?: number;
  source_type?: string;
  quantity: number;
  notes?: string;
}

export interface OrderCreate {
  table_id?: number;
  notes?: string;
  customer_id?: number;
  items: OrderItemCreate[];
  payments: OrderPaymentCreate[];
}

export interface AddPaymentsToOrder {
  payments: OrderPaymentCreate[];
}

export interface UpdateOrderItems {
  items: OrderItemCreate[];
}

