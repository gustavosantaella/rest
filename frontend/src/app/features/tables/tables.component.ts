import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators, FormArray } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { TableService } from '../../core/services/table.service';
import { OrderService } from '../../core/services/order.service';
import { ProductService } from '../../core/services/product.service';
import { MenuService } from '../../core/services/menu.service';
import { NotificationService } from '../../core/services/notification.service';
import { AuthPermissionsService } from '../../core/services/auth-permissions.service';
import { Table, TableStatus, TableCreate } from '../../core/models/table.model';
import { Order, OrderItem, UpdateOrderItems } from '../../core/models/order.model';
import { Product } from '../../core/models/product.model';
import { MenuItem } from '../../core/models/menu.model';
import { TooltipDirective } from '../../shared/directives/tooltip.directive';

@Component({
  selector: 'app-tables',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, RouterLink, TooltipDirective],
  templateUrl: './tables.component.html',
  styleUrls: ['./tables.component.scss']
})
export class TablesComponent implements OnInit, OnDestroy {
  private tableService = inject(TableService);
  private orderService = inject(OrderService);
  private productService = inject(ProductService);
  private menuService = inject(MenuService);
  private notificationService = inject(NotificationService);
  private authPermissionsService = inject(AuthPermissionsService);
  private fb = inject(FormBuilder);
  
  tables: Table[] = [];
  showModal = false;
  editingTable: Table | null = null;
  tableForm!: FormGroup;
  loading = true;
  private refreshInterval: any;
  
  // Vista de orden
  showOrderModal = false;
  selectedOrder: Order | null = null;
  selectedTable: Table | null = null;
  
  // Agregar items
  showAddItemsModal = false;
  addItemsForm!: FormGroup;
  products: Product[] = [];
  menuItems: MenuItem[] = [];
  showMenuItems = false; // Para cambiar entre productos y menú
  
  // Categorías
  productCategories: any[] = [];
  menuCategories: any[] = [];
  
  // Para el selector de categoría y productos
  currentItemIndex: number | null = null;
  selectedCategory: any = null;
  showCategorySelector = false;
  
  tableStatuses = Object.values(TableStatus);
  statusLabels: Record<TableStatus, string> = {
    [TableStatus.AVAILABLE]: 'Disponible',
    [TableStatus.OCCUPIED]: 'Ocupada',
    [TableStatus.RESERVED]: 'Reservada',
    [TableStatus.CLEANING]: 'Limpieza'
  };
  
  constructor() {
    this.initForm();
    this.initAddItemsForm();
  }
  
  ngOnInit(): void {
    this.loadTables();
    this.loadProducts();
    this.loadMenuItems();
    this.loadProductCategories();
    this.loadMenuCategories();
    
    // Actualizar cada 10 segundos para reflejar cambios de órdenes
    this.refreshInterval = setInterval(() => {
      if (!this.showModal && !this.showOrderModal && !this.showAddItemsModal) {
        this.loadTables();
      }
    }, 10000);
  }

  ngOnDestroy(): void {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  }
  
  initForm(): void {
    this.tableForm = this.fb.group({
      number: ['', Validators.required],
      capacity: [2, [Validators.required, Validators.min(1)]],
      location: ['']
    });
  }
  
  initAddItemsForm(): void {
    this.addItemsForm = this.fb.group({
      items: this.fb.array([])
    });
  }
  
  get addItemsArray(): FormArray {
    return this.addItemsForm.get('items') as FormArray;
  }
  
  loadTables(): void {
    const isInitialLoad = this.loading;
    if (isInitialLoad) {
      this.loading = true;
    }
    
    this.tableService.getTables().subscribe({
      next: (tables) => {
        this.tables = tables;
        if (isInitialLoad) {
          this.loading = false;
        }
      },
      error: () => {
        if (isInitialLoad) {
          this.loading = false;
        }
      }
    });
  }
  
  openModal(table?: Table): void {
    this.editingTable = table || null;
    
    if (table) {
      this.tableForm.patchValue(table);
    } else {
      this.tableForm.reset({ capacity: 2 });
    }
    
    this.showModal = true;
  }
  
  closeModal(): void {
    this.showModal = false;
    this.editingTable = null;
  }
  
  saveTable(): void {
    if (this.tableForm.invalid) return;
    
    const tableData: TableCreate = this.tableForm.value;
    
    if (this.editingTable) {
      this.tableService.updateTable(this.editingTable.id, tableData).subscribe({
        next: () => {
          this.loadTables();
          this.closeModal();
        }
      });
    } else {
      this.tableService.createTable(tableData).subscribe({
        next: () => {
          this.loadTables();
          this.closeModal();
        }
      });
    }
  }
  
  updateTableStatus(table: Table, status: TableStatus): void {
    this.tableService.updateTable(table.id, { status }).subscribe({
      next: () => {
        this.loadTables();
      }
    });
  }
  
  deleteTable(table: Table): void {
    if (confirm(`¿Estás seguro de eliminar la mesa "${table.number}"?`)) {
      this.tableService.deleteTable(table.id).subscribe({
        next: () => {
          this.loadTables();
        }
      });
    }
  }
  
  getStatusClass(status: TableStatus): string {
    const classes: Record<TableStatus, string> = {
      [TableStatus.AVAILABLE]: 'bg-green-100 text-green-800 border-green-300',
      [TableStatus.OCCUPIED]: 'bg-red-100 text-red-800 border-red-300',
      [TableStatus.RESERVED]: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      [TableStatus.CLEANING]: 'bg-blue-100 text-blue-800 border-blue-300'
    };
    return classes[status];
  }
  
  getTablesByStatus(status: TableStatus): Table[] {
    return this.tables.filter(t => t.status === status);
  }
  
  // Métodos de verificación de permisos
  canViewTables(): boolean {
    return this.authPermissionsService.hasPermission('tables.view');
  }
  
  canManageTables(): boolean {
    return this.authPermissionsService.hasPermission('tables.manage');
  }
  
  // Métodos para ver orden
  viewOrder(table: Table): void {
    if (table.status !== TableStatus.OCCUPIED) {
      this.notificationService.warning('Esta mesa no tiene orden activa');
      return;
    }
    
    this.selectedTable = table;
    this.orderService.getOrderByTable(table.id).subscribe({
      next: (order) => {
        this.selectedOrder = order;
        this.showOrderModal = true;
      },
      error: (err) => {
        this.notificationService.error('Error: ' + (err.error?.detail || 'No se pudo cargar la orden'));
      }
    });
  }
  
  closeOrderModal(): void {
    this.showOrderModal = false;
    this.selectedOrder = null;
    this.selectedTable = null;
  }
  
  getItemName(item: OrderItem): string {
    if (item.source_type === 'menu' && item.menu_item_id) {
      const menuItem = this.menuItems.find(m => m.id === item.menu_item_id);
      return menuItem ? menuItem.name : `Menu Item #${item.menu_item_id}`;
    } else if (item.product_id) {
      const product = this.products.find(p => p.id === item.product_id);
      return product ? product.name : `Producto #${item.product_id}`;
    }
    return 'Item desconocido';
  }
  
  // Métodos para agregar items
  openAddItemsModal(table: Table): void {
    this.selectedTable = table;
    
    if (table.status === TableStatus.OCCUPIED) {
      // Mesa ocupada - agregar a orden existente
      this.orderService.getOrderByTable(table.id).subscribe({
        next: (order) => {
          this.selectedOrder = order;
          this.addItemsArray.clear();
          this.addNewItem();
          this.showAddItemsModal = true;
        },
        error: (err) => {
          this.notificationService.error('Error: ' + (err.error?.detail || 'No se pudo cargar la orden'));
        }
      });
    } else {
      // Mesa disponible - crear nueva orden
      this.selectedOrder = null; // Indicador de que es nueva orden
      this.addItemsArray.clear();
      this.addNewItem();
      this.showAddItemsModal = true;
    }
  }
  
  closeAddItemsModal(): void {
    this.showAddItemsModal = false;
    this.selectedOrder = null;
    this.selectedTable = null;
    this.addItemsArray.clear();
  }
  
  addNewItem(): void {
    const item = this.fb.group({
      product_id: ['', Validators.required],
      quantity: [1, [Validators.required, Validators.min(0.01)]],
      notes: [''],
      source_type: [this.showMenuItems ? 'menu' : 'product']
    });
    this.addItemsArray.push(item);
  }
  
  removeItem(index: number): void {
    this.addItemsArray.removeAt(index);
  }
  
  toggleSource(): void {
    this.showMenuItems = !this.showMenuItems;
  }
  
  toggleItemSource(index: number): void {
    const item = this.addItemsArray.at(index);
    const currentSourceType = item.get('source_type')?.value;
    const newSourceType = currentSourceType === 'menu' ? 'product' : 'menu';
    
    item.patchValue({
      source_type: newSourceType,
      product_id: '' // Limpiar selección al cambiar de fuente
    });
  }
  
  get availableItems(): (MenuItem | Product)[] {
    return this.showMenuItems 
      ? this.menuItems.filter(m => m.is_available) 
      : this.products;
  }
  
  get availableMenuItems(): MenuItem[] {
    return this.menuItems.filter(m => m.is_available);
  }
  
  get availableProducts(): Product[] {
    return this.products.filter(p => p.show_in_catalog === true);
  }
  
  getItemPrice(item: any): number {
    // Si tiene la propiedad 'price', es un MenuItem
    if (item.price !== undefined) {
      return item.price;
    }
    // Si tiene 'sale_price', es un Product
    return item.sale_price || 0;
  }
  
  saveAddedItems(): void {
    if (!this.selectedTable || this.addItemsForm.invalid || this.addItemsArray.length === 0) return;
    
    // Transformar nuevos items
    const newItems = this.addItemsForm.value.items.map((item: any) => {
      if (item.source_type === 'menu') {
        return {
          menu_item_id: Number(item.product_id),
          quantity: item.quantity,
          notes: item.notes || '',
          source_type: 'menu'
        };
      } else {
        return {
          product_id: Number(item.product_id),
          quantity: item.quantity,
          notes: item.notes || '',
          source_type: 'product'
        };
      }
    });
    
    if (this.selectedOrder) {
      // Mesa ocupada - agregar a orden existente
      const existingItems = this.selectedOrder.items.map(item => {
        if (item.source_type === 'menu') {
          return {
            menu_item_id: item.menu_item_id,
            quantity: item.quantity,
            notes: item.notes || '',
            source_type: 'menu'
          };
        } else {
          return {
            product_id: item.product_id,
            quantity: item.quantity,
            notes: item.notes || '',
            source_type: 'product'
          };
        }
      });
      
      const allItems = [...existingItems, ...newItems];
      const itemsData: UpdateOrderItems = {
        items: allItems
      };
      
      this.orderService.updateOrderItems(this.selectedOrder.id, itemsData).subscribe({
        next: () => {
          this.notificationService.success('Items agregados exitosamente');
          this.closeAddItemsModal();
          this.loadTables();
        },
        error: (err) => {
          this.notificationService.error('Error: ' + (err.error?.detail || 'Error al agregar items'));
        }
      });
    } else {
      // Mesa disponible - crear nueva orden
      const orderData = {
        table_id: this.selectedTable.id,
        notes: undefined,
        items: newItems,
        payments: []
      };
      
      this.orderService.createOrder(orderData).subscribe({
        next: () => {
          this.notificationService.success('Orden creada exitosamente');
          this.closeAddItemsModal();
          this.loadTables();
        },
        error: (err) => {
          this.notificationService.error('Error: ' + (err.error?.detail || 'Error al crear la orden'));
        }
      });
    }
  }
  
  loadProducts(): void {
    this.productService.getProducts().subscribe({
      next: (products) => {
        this.products = products;
      },
      error: () => {}
    });
  }
  
  loadMenuItems(): void {
    this.menuService.getMenuItems().subscribe({
      next: (items) => {
        this.menuItems = items;
      },
      error: () => {}
    });
  }
  
  loadProductCategories(): void {
    this.productService.getCategories().subscribe({
      next: (categories) => {
        this.productCategories = categories;
      },
      error: () => {}
    });
  }
  
  loadMenuCategories(): void {
    this.menuService.getCategories().subscribe({
      next: (categories) => {
        this.menuCategories = categories;
      },
      error: () => {}
    });
  }
  
  // Métodos para selección de categoría y productos
  openCategorySelector(index: number): void {
    this.currentItemIndex = index;
    this.selectedCategory = null;
    this.showCategorySelector = true;
  }
  
  closeCategorySelector(): void {
    this.showCategorySelector = false;
    this.currentItemIndex = null;
    this.selectedCategory = null;
  }
  
  selectCategory(category: any): void {
    this.selectedCategory = category;
  }
  
  selectItem(itemId: number, itemType: 'menu' | 'product'): void {
    if (this.currentItemIndex !== null) {
      const item = this.addItemsArray.at(this.currentItemIndex);
      item.patchValue({
        product_id: itemId,
        source_type: itemType
      });
      this.closeCategorySelector();
    }
  }
  
  getProductsByCategory(categoryId: number): Product[] {
    return this.products.filter(p => p.category_id === categoryId && p.show_in_catalog === true);
  }
  
  getMenuItemsByCategory(categoryId: number): MenuItem[] {
    return this.menuItems.filter(m => m.category_id === categoryId && m.is_available);
  }
  
  getCurrentCategories() {
    const item = this.currentItemIndex !== null ? this.addItemsArray.at(this.currentItemIndex) : null;
    const sourceType = item?.get('source_type')?.value;
    return sourceType === 'menu' ? this.menuCategories : this.productCategories;
  }
  
  get currentItems(): (MenuItem | Product)[] {
    if (!this.selectedCategory) return [];
    const item = this.currentItemIndex !== null ? this.addItemsArray.at(this.currentItemIndex) : null;
    const sourceType = item?.get('source_type')?.value;
    
    if (sourceType === 'menu') {
      return this.getMenuItemsByCategory(this.selectedCategory.id);
    } else {
      return this.getProductsByCategory(this.selectedCategory.id);
    }
  }
  
  getItemDisplayPrice(item: any): number {
    return item.price !== undefined ? item.price : item.sale_price;
  }
  
  hasStock(item: any): boolean {
    return item.stock !== undefined;
  }
  
  getItemStock(item: any): number {
    return item.stock || 0;
  }
  
  isMenuItem(item: any): boolean {
    return item.price !== undefined;
  }
  
  getSelectedItemName(itemForm: any): string {
    const productId = itemForm.get('product_id')?.value;
    const sourceType = itemForm.get('source_type')?.value;
    
    if (!productId) return 'Ninguno seleccionado';
    
    if (sourceType === 'menu') {
      const menuItem = this.menuItems.find(m => m.id === Number(productId));
      return menuItem ? menuItem.name : 'Item no encontrado';
    } else {
      const product = this.products.find(p => p.id === Number(productId));
      return product ? product.name : 'Producto no encontrado';
    }
  }
}

