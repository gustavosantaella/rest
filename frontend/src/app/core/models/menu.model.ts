export interface MenuCategory {
  id: number;
  name: string;
  description?: string;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface IngredientItem {
  product_id: number;
  quantity: number;
  product_name?: string;
}

export interface MenuItem {
  id: number;
  name: string;
  description?: string;
  category_id: number;
  price: number;
  preparation_time?: number;
  is_available: boolean;
  is_featured: boolean;
  image_url?: string;
  created_at?: string;
  updated_at?: string;
  ingredients?: IngredientItem[];  // Opcional para catálogo público
}

export interface MenuCategoryCreate {
  name: string;
  description?: string;
  display_order?: number;
  is_active?: boolean;
}

export interface MenuItemCreate {
  name: string;
  description?: string;
  category_id: number;
  price: number;
  preparation_time?: number;
  is_available?: boolean;
  is_featured?: boolean;
  image_url?: string;
  ingredients: IngredientItem[];
}

