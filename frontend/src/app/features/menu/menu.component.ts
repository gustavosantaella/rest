import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { MenuService } from '../../core/services/menu.service';
import { ProductService } from '../../core/services/product.service';
import { AuthPermissionsService } from '../../core/services/auth-permissions.service';
import { MenuItem, MenuCategory, MenuItemCreate, MenuCategoryCreate, IngredientItem } from '../../core/models/menu.model';
import { Product } from '../../core/models/product.model';
import { TooltipDirective } from '../../shared/directives/tooltip.directive';
import { ImageUploadComponent } from '../../shared/components/image-upload/image-upload.component';
import { UploadService } from '../../core/services/upload.service';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, TooltipDirective, ImageUploadComponent],
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})
export class MenuComponent implements OnInit {
  private menuService = inject(MenuService);
  private productService = inject(ProductService);
  private authPermissionsService = inject(AuthPermissionsService);
  private fb = inject(FormBuilder);
  public uploadService = inject(UploadService);
  
  menuItems: MenuItem[] = [];
  categories: MenuCategory[] = [];
  products: Product[] = [];
  filteredItems: MenuItem[] = [];
  
  showItemModal = false;
  showCategoryModal = false;
  editingItem: MenuItem | null = null;
  editingCategory: MenuCategory | null = null;
  
  itemForm!: FormGroup;
  categoryForm!: FormGroup;
  
  searchTerm = '';
  selectedCategory = '';
  showOnlyAvailable = false;
  
  loading = true;
  
  constructor() {
    this.initForms();
  }
  
  ngOnInit(): void {
    this.loadData();
  }
  
  initForms(): void {
    this.itemForm = this.fb.group({
      name: ['', Validators.required],
      description: [''],
      category_id: ['', Validators.required],
      price: [0, [Validators.required, Validators.min(0)]],
      preparation_time: [0],
      is_available: [true],
      is_featured: [false],
      image_url: [''],
      ingredients: this.fb.array([])
    });
    
    this.categoryForm = this.fb.group({
      name: ['', Validators.required],
      description: [''],
      display_order: [0],
      is_active: [true]
    });
  }
  
  get ingredientsArray(): FormArray {
    return this.itemForm.get('ingredients') as FormArray;
  }
  
  addIngredient(): void {
    const ingredient = this.fb.group({
      product_id: ['', Validators.required],
      quantity: [0, [Validators.required, Validators.min(0.01)]]
    });
    this.ingredientsArray.push(ingredient);
  }
  
  removeIngredient(index: number): void {
    this.ingredientsArray.removeAt(index);
  }
  
  loadData(): void {
    this.loading = true;
    
    this.menuService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      }
    });
    
    this.productService.getProducts().subscribe({
      next: (products) => {
        this.products = products;
      }
    });
    
    this.menuService.getMenuItems().subscribe({
      next: (items) => {
        this.menuItems = items;
        this.filteredItems = items;
        this.loading = false;
      }
    });
  }
  
  filterItems(): void {
    this.filteredItems = this.menuItems.filter(item => {
      const matchesSearch = item.name.toLowerCase().includes(this.searchTerm.toLowerCase());
      const matchesCategory = !this.selectedCategory || item.category_id.toString() === this.selectedCategory;
      const matchesAvailability = !this.showOnlyAvailable || item.is_available;
      return matchesSearch && matchesCategory && matchesAvailability;
    });
  }
  
  // Item Modal
  openItemModal(item?: MenuItem): void {
    this.editingItem = item || null;
    this.ingredientsArray.clear();
    
    if (item) {
      this.itemForm.patchValue(item);
      
      // Cargar ingredientes
      if (item.ingredients && item.ingredients.length > 0) {
        item.ingredients.forEach(ing => {
          const ingredient = this.fb.group({
            product_id: [ing.product_id, Validators.required],
            quantity: [ing.quantity, [Validators.required, Validators.min(0.01)]]
          });
          this.ingredientsArray.push(ingredient);
        });
      }
    } else {
      this.itemForm.reset({
        price: 0,
        preparation_time: 0,
        is_available: true,
        is_featured: false
      });
    }
    
    this.showItemModal = true;
  }
  
  closeItemModal(): void {
    this.showItemModal = false;
    this.editingItem = null;
  }
  
  saveItem(): void {
    if (this.itemForm.invalid) return;
    
    const itemData: MenuItemCreate = this.itemForm.value;
    
    if (this.editingItem) {
      this.menuService.updateMenuItem(this.editingItem.id, itemData).subscribe({
        next: () => {
          this.loadData();
          this.closeItemModal();
        }
      });
    } else {
      this.menuService.createMenuItem(itemData).subscribe({
        next: () => {
          this.loadData();
          this.closeItemModal();
        }
      });
    }
  }
  
  deleteItem(item: MenuItem): void {
    if (confirm(`¿Estás seguro de eliminar "${item.name}" del menú?`)) {
      this.menuService.deleteMenuItem(item.id).subscribe({
        next: () => {
          this.loadData();
        }
      });
    }
  }
  
  toggleAvailability(item: MenuItem): void {
    this.menuService.updateMenuItem(item.id, { is_available: !item.is_available }).subscribe({
      next: () => {
        this.loadData();
      }
    });
  }
  
  // Category Modal
  openCategoryModal(category?: MenuCategory): void {
    this.editingCategory = category || null;
    
    if (category) {
      this.categoryForm.patchValue(category);
    } else {
      this.categoryForm.reset({ display_order: 0, is_active: true });
    }
    
    this.showCategoryModal = true;
  }
  
  closeCategoryModal(): void {
    this.showCategoryModal = false;
    this.editingCategory = null;
  }
  
  saveCategory(): void {
    if (this.categoryForm.invalid) return;
    
    const categoryData: MenuCategoryCreate = this.categoryForm.value;
    
    if (this.editingCategory) {
      this.menuService.updateCategory(this.editingCategory.id, categoryData).subscribe({
        next: () => {
          this.loadData();
          this.closeCategoryModal();
        }
      });
    } else {
      this.menuService.createCategory(categoryData).subscribe({
        next: () => {
          this.loadData();
          this.closeCategoryModal();
        }
      });
    }
  }
  
  getCategoryName(categoryId: number): string {
    const category = this.categories.find(c => c.id === categoryId);
    return category?.name || 'Sin categoría';
  }

  onImageError(event: Event): void {
    const img = event.target as HTMLImageElement;
    img.src = 'https://via.placeholder.com/400x300?text=No+Image';
  }
  
  getProductName(productId: number): string {
    const product = this.products.find(p => p.id === productId);
    return product?.name || 'Producto desconocido';
  }
  
  getProductUnit(productId: number): string {
    const product = this.products.find(p => p.id === productId);
    if (!product) return '';
    
    const units: Record<string, string> = {
      'unit': 'unidad',
      'weight_gram': 'g',
      'weight_kg': 'kg',
      'volume_ml': 'ml',
      'volume_l': 'L',
      'bulk': 'a granel'
    };
    
    return units[product.unit_type] || '';
  }
  
  // Métodos de verificación de permisos
  canViewMenu(): boolean {
    return this.authPermissionsService.hasPermission('menu.view');
  }
  
  canCreateMenu(): boolean {
    return this.authPermissionsService.hasPermission('menu.create');
  }
  
  canEditMenu(): boolean {
    return this.authPermissionsService.hasPermission('menu.edit');
  }
  
  canDeleteMenu(): boolean {
    return this.authPermissionsService.hasPermission('menu.delete');
  }
}

