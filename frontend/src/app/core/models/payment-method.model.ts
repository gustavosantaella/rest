export enum PaymentMethodType {
  PAGO_MOVIL = 'pago_movil',
  TRANSFERENCIA = 'transferencia',
  EFECTIVO = 'efectivo',
  BOLIVARES = 'bolivares',
  DOLARES = 'dolares',
  EUROS = 'euros'
}

export interface PaymentMethod {
  id: number;
  name: string;
  type: PaymentMethodType;
  phone?: string;
  dni?: string;
  bank?: string;
  account_holder?: string;
  account_number?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface PaymentMethodCreate {
  name: string;
  type: PaymentMethodType;
  phone?: string;
  dni?: string;
  bank?: string;
  account_holder?: string;
  account_number?: string;
  is_active?: boolean;
}

export interface PaymentMethodUpdate {
  name?: string;
  phone?: string;
  dni?: string;
  bank?: string;
  account_holder?: string;
  account_number?: string;
  is_active?: boolean;
}

export const PAYMENT_METHOD_LABELS: Record<PaymentMethodType, string> = {
  [PaymentMethodType.PAGO_MOVIL]: 'Pago Móvil',
  [PaymentMethodType.TRANSFERENCIA]: 'Transferencia Bancaria',
  [PaymentMethodType.EFECTIVO]: 'Efectivo',
  [PaymentMethodType.BOLIVARES]: 'Bolívares',
  [PaymentMethodType.DOLARES]: 'Dólares',
  [PaymentMethodType.EUROS]: 'Euros'
};

