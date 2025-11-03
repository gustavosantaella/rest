import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ProductService } from '../../core/services/product.service';
import { AuthPermissionsService } from '../../core/services/auth-permissions.service';
import { Product, Category, UnitType, ProductCreate, CategoryCreate } from '../../core/models/product.model';
import { TooltipDirective } from '../../shared/directives/tooltip.directive';
import { ImageUploadComponent } from '../../shared/components/image-upload/image-upload.component';
import { UploadService } from '../../core/services/upload.service';

@Component({
  selector: 'app-inventory',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, TooltipDirective, ImageUploadComponent],
  templateUrl: './inventory.component.html',
  styleUrls: ['./inventory.component.scss']
})
export class InventoryComponent implements OnInit {
  private productService = inject(ProductService);
  private authPermissionsService = inject(AuthPermissionsService);
  private fb = inject(FormBuilder);
  public uploadService = inject(UploadService);
  
  products: Product[] = [];
  categories: Category[] = [];
  filteredProducts: Product[] = [];
  
  showProductModal = false;
  showCategoryModal = false;
  editingProduct: Product | null = null;
  
  productForm!: FormGroup;
  categoryForm!: FormGroup;
  
  searchTerm = '';
  selectedCategory = '';
  
  unitTypes = Object.values(UnitType);
  unitTypeLabels: Record<UnitType, string> = {
    [UnitType.UNIT]: 'Unidad',
    [UnitType.WEIGHT_GRAM]: 'Gramo',
    [UnitType.WEIGHT_KG]: 'Kilogramo',
    [UnitType.VOLUME_ML]: 'Mililitro',
    [UnitType.VOLUME_L]: 'Litro',
    [UnitType.BULK]: 'A granel'
  };
  
  loading = true;
  
  constructor() {
    this.initForms();
  }
  
  ngOnInit(): void {
    this.loadData();
  }
  
  initForms(): void {
    this.productForm = this.fb.group({
      name: ['', Validators.required],
      description: [''],
      category_id: ['', Validators.required],
      unit_type: [UnitType.UNIT, Validators.required],
      purchase_price: [0, [Validators.required, Validators.min(0)]],
      sale_price: [0, [Validators.required, Validators.min(0)]],
      stock: [0, [Validators.required, Validators.min(0)]],
      min_stock: [0, [Validators.required, Validators.min(0)]],
      show_in_catalog: [false],  // Por defecto no se muestra
      image_url: [null]  // URL de la imagen
    });
    
    this.categoryForm = this.fb.group({
      name: ['', Validators.required],
      description: ['']
    });
  }
  
  loadData(): void {
    this.loading = true;
    
    this.productService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      }
    });
    
    this.productService.getProducts().subscribe({
      next: (products) => {
        this.products = products;
        this.filteredProducts = products;
        this.loading = false;
      }
    });
  }
  
  filterProducts(): void {
    this.filteredProducts = this.products.filter(product => {
      const matchesSearch = product.name.toLowerCase().includes(this.searchTerm.toLowerCase());
      const matchesCategory = !this.selectedCategory || product.category_id.toString() === this.selectedCategory;
      return matchesSearch && matchesCategory;
    });
  }
  
  openProductModal(product?: Product): void {
    this.editingProduct = product || null;
    
    if (product) {
      this.productForm.patchValue(product);
    } else {
      this.productForm.reset({
        unit_type: UnitType.UNIT,
        purchase_price: 0,
        sale_price: 0,
        stock: 0,
        min_stock: 0
      });
    }
    
    this.showProductModal = true;
  }
  
  closeProductModal(): void {
    this.showProductModal = false;
    this.editingProduct = null;
  }
  
  saveProduct(): void {
    if (this.productForm.invalid) return;
    
    const productData: ProductCreate = this.productForm.value;
    
    if (this.editingProduct) {
      this.productService.updateProduct(this.editingProduct.id, productData).subscribe({
        next: () => {
          this.loadData();
          this.closeProductModal();
        }
      });
    } else {
      this.productService.createProduct(productData).subscribe({
        next: () => {
          this.loadData();
          this.closeProductModal();
        }
      });
    }
  }
  
  deleteProduct(product: Product): void {
    if (confirm(`¿Estás seguro de eliminar el producto "${product.name}"?`)) {
      this.productService.deleteProduct(product.id).subscribe({
        next: () => {
          this.loadData();
        }
      });
    }
  }
  
  openCategoryModal(): void {
    this.categoryForm.reset();
    this.showCategoryModal = true;
  }
  
  closeCategoryModal(): void {
    this.showCategoryModal = false;
  }
  
  saveCategory(): void {
    if (this.categoryForm.invalid) return;
    
    const categoryData: CategoryCreate = this.categoryForm.value;
    
    this.productService.createCategory(categoryData).subscribe({
      next: () => {
        this.loadData();
        this.closeCategoryModal();
      }
    });
  }
  
  getCategoryName(categoryId: number): string {
    const category = this.categories.find(c => c.id === categoryId);
    return category?.name || 'Sin categoría';
  }

  onImageError(event: Event): void {
    const img = event.target as HTMLImageElement;
    img.src = 'https://via.placeholder.com/48?text=No+Image';
  }
  
  isLowStock(product: Product): boolean {
    return product.stock <= product.min_stock;
  }
  
  // Métodos de verificación de permisos
  canViewInventory(): boolean {
    return this.authPermissionsService.hasAnyPermission([
      'inventory.view',
      'inventory.manage',
      'products.view',
      'products.create',
      'products.edit',
      'products.delete'
    ]);
  }
  
  canManageInventory(): boolean {
    return this.authPermissionsService.hasAnyPermission([
      'inventory.manage',
      'products.create',
      'products.edit',
      'products.delete'
    ]);
  }
}

