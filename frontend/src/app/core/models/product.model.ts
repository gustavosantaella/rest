export enum UnitType {
  UNIT = 'unit',
  WEIGHT_GRAM = 'weight_gram',
  WEIGHT_KG = 'weight_kg',
  VOLUME_ML = 'volume_ml',
  VOLUME_L = 'volume_l',
  BULK = 'bulk'
}

export interface Category {
  id: number;
  name: string;
  description?: string;
  created_at: string;
}

export interface Product {
  id: number;
  name: string;
  description?: string;
  category_id: number;
  unit_type: UnitType;
  purchase_price: number;
  sale_price: number;
  stock: number;
  min_stock: number;
  show_in_catalog: boolean;  // Mostrar en selector de órdenes
  image_url?: string;  // URL de la imagen del producto
  created_at: string;
  updated_at?: string;
}

export interface ProductCreate {
  name: string;
  description?: string;
  category_id: number;
  unit_type: UnitType;
  purchase_price: number;
  sale_price: number;
  stock: number;
  min_stock: number;
  show_in_catalog: boolean;
  image_url?: string;
}

export interface CategoryCreate {
  name: string;
  description?: string;
}

