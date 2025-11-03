import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { OrderService } from '../../core/services/order.service';
import { ProductService } from '../../core/services/product.service';
import { TableService } from '../../core/services/table.service';
import { MenuService } from '../../core/services/menu.service';
import { Order, OrderStatus, PaymentMethod, OrderCreate, OrderItemCreate } from '../../core/models/order.model';
import { Product } from '../../core/models/product.model';
import { Table, TableStatus } from '../../core/models/table.model';
import { MenuItem } from '../../core/models/menu.model';
import { TooltipDirective } from '../../shared/directives/tooltip.directive';

@Component({
  selector: 'app-orders',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, TooltipDirective],
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.scss']
})
export class OrdersComponent implements OnInit {
  private orderService = inject(OrderService);
  private productService = inject(ProductService);
  private tableService = inject(TableService);
  private menuService = inject(MenuService);
  private fb = inject(FormBuilder);
  
  orders: Order[] = [];
  products: Product[] = [];
  menuItems: MenuItem[] = [];
  tables: Table[] = [];
  
  showMenuItems = true; // Toggle para mostrar menú o inventario
  
  showModal = false;
  showDetailModal = false;
  selectedOrder: Order | null = null;
  orderForm!: FormGroup;
  loading = true;
  
  orderStatuses = Object.values(OrderStatus);
  paymentMethods = Object.values(PaymentMethod);
  
  // Exponer OrderStatus para el template
  OrderStatus = OrderStatus;
  PaymentMethod = PaymentMethod;
  
  statusLabels: Record<OrderStatus, string> = {
    [OrderStatus.PENDING]: 'Pendiente',
    [OrderStatus.IN_PROGRESS]: 'En Progreso',
    [OrderStatus.COMPLETED]: 'Completada',
    [OrderStatus.PAID]: 'Pagada',
    [OrderStatus.CANCELLED]: 'Cancelada'
  };
  
  paymentMethodLabels: Record<PaymentMethod, string> = {
    [PaymentMethod.CASH]: 'Efectivo',
    [PaymentMethod.CARD]: 'Tarjeta',
    [PaymentMethod.TRANSFER]: 'Transferencia',
    [PaymentMethod.MIXED]: 'Mixto'
  };
  
  constructor() {
    this.initForm();
  }
  
  ngOnInit(): void {
    this.loadData();
  }
  
  initForm(): void {
    this.orderForm = this.fb.group({
      table_id: [''],
      notes: [''],
      items: this.fb.array([])
    });
  }
  
  get itemsArray(): FormArray {
    return this.orderForm.get('items') as FormArray;
  }
  
  addItem(): void {
    const item = this.fb.group({
      product_id: ['', Validators.required],
      quantity: [1, [Validators.required, Validators.min(0.01)]],
      notes: ['']
    });
    this.itemsArray.push(item);
  }
  
  removeItem(index: number): void {
    this.itemsArray.removeAt(index);
  }
  
  loadData(): void {
    this.loading = true;
    
    this.orderService.getOrders().subscribe({
      next: (orders) => {
        this.orders = orders.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
      }
    });
    
    this.productService.getProducts().subscribe({
      next: (products) => {
        this.products = products;
      }
    });
    
    this.menuService.getMenuItems(undefined, true).subscribe({
      next: (items) => {
        this.menuItems = items;
      }
    });
    
    this.tableService.getTables().subscribe({
      next: (tables) => {
        this.tables = tables.filter(t => t.status === TableStatus.AVAILABLE || t.status === TableStatus.OCCUPIED);
        this.loading = false;
      }
    });
  }
  
  openModal(): void {
    this.orderForm.reset();
    this.itemsArray.clear();
    this.addItem();
    this.showModal = true;
  }
  
  closeModal(): void {
    this.showModal = false;
  }
  
  saveOrder(): void {
    if (this.orderForm.invalid || this.itemsArray.length === 0) return;
    
    const orderData: OrderCreate = {
      table_id: this.orderForm.value.table_id || undefined,
      notes: this.orderForm.value.notes,
      items: this.orderForm.value.items
    };
    
    this.orderService.createOrder(orderData).subscribe({
      next: () => {
        this.loadData();
        this.closeModal();
      },
      error: (err) => {
        alert('Error al crear la orden: ' + (err.error?.detail || 'Error desconocido'));
      }
    });
  }
  
  viewOrderDetail(order: Order): void {
    this.selectedOrder = order;
    this.showDetailModal = true;
  }
  
  closeDetailModal(): void {
    this.showDetailModal = false;
    this.selectedOrder = null;
  }
  
  updateOrderStatus(order: Order, status: OrderStatus, paymentMethod?: PaymentMethod): void {
    const update: any = { status };
    if (paymentMethod) {
      update.payment_method = paymentMethod;
    }
    
    this.orderService.updateOrder(order.id, update).subscribe({
      next: () => {
        this.loadData();
        if (this.selectedOrder?.id === order.id) {
          this.closeDetailModal();
        }
      }
    });
  }
  
  markAsPaid(order: Order): void {
    const paymentMethod = prompt('Método de pago:\n1. Efectivo\n2. Tarjeta\n3. Transferencia\n4. Mixto\n\nIngresa el número:');
    
    const methods: Record<string, PaymentMethod> = {
      '1': PaymentMethod.CASH,
      '2': PaymentMethod.CARD,
      '3': PaymentMethod.TRANSFER,
      '4': PaymentMethod.MIXED
    };
    
    if (paymentMethod && methods[paymentMethod]) {
      this.updateOrderStatus(order, OrderStatus.PAID, methods[paymentMethod]);
    }
  }
  
  deleteOrder(order: Order): void {
    if (confirm(`¿Estás seguro de eliminar la orden #${order.id}?`)) {
      this.orderService.deleteOrder(order.id).subscribe({
        next: () => {
          this.loadData();
        }
      });
    }
  }
  
  getStatusClass(status: OrderStatus): string {
    const classes: Record<OrderStatus, string> = {
      [OrderStatus.PENDING]: 'badge-warning',
      [OrderStatus.IN_PROGRESS]: 'badge-info',
      [OrderStatus.COMPLETED]: 'badge-success',
      [OrderStatus.PAID]: 'badge-success',
      [OrderStatus.CANCELLED]: 'badge-danger'
    };
    return classes[status];
  }
  
  getProductName(productId: number): string {
    const product = this.products.find(p => p.id === productId);
    return product?.name || 'Producto desconocido';
  }
  
  getTableNumber(tableId?: number): string {
    if (!tableId) return 'Para llevar';
    const table = this.tables.find(t => t.id === tableId);
    return table ? `Mesa ${table.number}` : `Mesa ${tableId}`;
  }
  
  getMenuItemName(menuItemId: number): string {
    const item = this.menuItems.find(m => m.id === menuItemId);
    return item?.name || '';
  }
  
  getMenuItemPrice(menuItemId: number): number {
    const item = this.menuItems.find(m => m.id === menuItemId);
    return item?.price || 0;
  }
  
  toggleItemSource(): void {
    this.showMenuItems = !this.showMenuItems;
  }
  
  get featuredMenuItems(): MenuItem[] {
    return this.menuItems.filter(m => m.is_featured);
  }
  
  get hasFeaturedItems(): boolean {
    return this.featuredMenuItems.length > 0;
  }
}

