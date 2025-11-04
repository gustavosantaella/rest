import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { TableService } from '../../core/services/table.service';
import { OrderService } from '../../core/services/order.service';
import { ProductService } from '../../core/services/product.service';
import { MenuService } from '../../core/services/menu.service';
import { PaymentMethodService } from '../../core/services/payment-method.service';
import { NotificationService } from '../../core/services/notification.service';
import { Table, TableStatus } from '../../core/models/table.model';
import { Order, UpdateOrderItems, AddPaymentsToOrder, OrderPayment } from '../../core/models/order.model';
import { Product } from '../../core/models/product.model';
import { MenuItem } from '../../core/models/menu.model';
import { PaymentMethod as PaymentMethodModel } from '../../core/models/payment-method.model';

@Component({
  selector: 'app-cashier-pos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './cashier-pos.component.html',
  styleUrls: ['./cashier-pos.component.scss']
})
export class CashierPosComponent implements OnInit, OnDestroy {
  private tableService = inject(TableService);
  private orderService = inject(OrderService);
  private productService = inject(ProductService);
  private menuService = inject(MenuService);
  private paymentMethodService = inject(PaymentMethodService);
  private notificationService = inject(NotificationService);
  private router = inject(Router);
  
  tables: Table[] = [];
  products: Product[] = [];
  menuItems: MenuItem[] = [];
  productCategories: any[] = [];
  menuCategories: any[] = [];
  activePaymentMethods: PaymentMethodModel[] = [];
  
  currentTable: Table | null = null;
  currentOrder: Order | null = null;
  selectedCategory: any = null;
  posItems: any[] = [];
  
  // Modal de pago
  showPaymentModal = false;
  orderToPay: Order | null = null;
  orderPayments: OrderPayment[] = [];
  
  private refreshInterval: any;
  
  ngOnInit(): void {
    this.loadData();
    
    // Actualizar cada 10 segundos
    this.refreshInterval = setInterval(() => {
      if (!this.showPaymentModal) {
        this.loadTables();
      }
    }, 10000);
  }
  
  ngOnDestroy(): void {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  }
  
  loadData(): void {
    this.loadTables();
    this.loadProducts();
    this.loadMenuItems();
    this.loadProductCategories();
    this.loadMenuCategories();
    this.loadPaymentMethods();
  }
  
  loadTables(): void {
    this.tableService.getTables().subscribe({
      next: (tables) => {
        this.tables = tables;
      },
      error: () => {}
    });
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
  
  loadPaymentMethods(): void {
    this.paymentMethodService.getPaymentMethods().subscribe({
      next: (methods) => {
        this.activePaymentMethods = methods.filter(m => m.is_active);
      },
      error: () => {}
    });
  }
  
  get allCategories(): any[] {
    return [...this.productCategories, ...this.menuCategories];
  }
  
  selectTable(table: Table): void {
    this.currentTable = table;
    this.posItems = [];
    
    if (table.status === TableStatus.OCCUPIED) {
      this.orderService.getOrderByTable(table.id).subscribe({
        next: (order: Order | null) => {
          if (order) {
            this.currentOrder = order;
            this.posItems = order.items.map(item => ({
              id: item.id,
              product_id: item.product_id,
              menu_item_id: item.menu_item_id,
              source_type: item.source_type,
              name: this.getItemName(item),
              quantity: item.quantity,
              unit_price: item.unit_price,
              subtotal: item.subtotal,
              notes: item.notes
            }));
          }
        },
        error: () => {
          this.currentOrder = null;
        }
      });
    } else {
      this.currentOrder = null;
    }
  }
  
  selectCategory(category: any): void {
    this.selectedCategory = category;
  }
  
  addItem(item: MenuItem | Product): void {
    const existingItem = this.posItems.find(i => 
      (item as any).price !== undefined 
        ? i.menu_item_id === item.id 
        : i.product_id === item.id
    );
    
    if (existingItem) {
      existingItem.quantity += 1;
      existingItem.subtotal = existingItem.quantity * existingItem.unit_price;
    } else {
      const isMenu = (item as any).price !== undefined;
      this.posItems.push({
        product_id: isMenu ? undefined : item.id,
        menu_item_id: isMenu ? item.id : undefined,
        source_type: isMenu ? 'menu' : 'product',
        name: item.name,
        quantity: 1,
        unit_price: isMenu ? (item as MenuItem).price : (item as Product).sale_price,
        subtotal: isMenu ? (item as MenuItem).price : (item as Product).sale_price,
        notes: ''
      });
    }
  }
  
  removeItem(index: number): void {
    this.posItems.splice(index, 1);
  }
  
  updateItemQuantity(index: number, quantity: number): void {
    if (quantity <= 0) {
      this.removeItem(index);
    } else {
      this.posItems[index].quantity = quantity;
      this.posItems[index].subtotal = quantity * this.posItems[index].unit_price;
    }
  }
  
  get subtotal(): number {
    return this.posItems.reduce((sum, item) => sum + item.subtotal, 0);
  }
  
  get tax(): number {
    return this.subtotal * 0.16;
  }
  
  get total(): number {
    return this.subtotal + this.tax;
  }
  
  saveOrder(): void {
    if (!this.currentTable || this.posItems.length === 0) {
      this.notificationService.warning('Debe seleccionar una mesa y agregar items');
      return;
    }
    
    const transformedItems = this.posItems.map(item => {
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
    
    if (this.currentOrder) {
      const itemsData: UpdateOrderItems = { items: transformedItems };
      
      this.orderService.updateOrderItems(this.currentOrder.id, itemsData).subscribe({
        next: () => {
          this.notificationService.success('Orden actualizada');
          this.loadTables();
          this.clear();
        },
        error: (err) => {
          this.notificationService.error('Error: ' + (err.error?.detail || 'Error al actualizar'));
        }
      });
    } else {
      const orderData = {
        table_id: this.currentTable.id,
        notes: undefined,
        items: transformedItems,
        payments: []
      };
      
      this.orderService.createOrder(orderData).subscribe({
        next: () => {
          this.notificationService.success('Orden creada');
          this.loadTables();
          this.clear();
        },
        error: (err) => {
          this.notificationService.error('Error: ' + (err.error?.detail || 'Error al crear orden'));
        }
      });
    }
  }
  
  clear(): void {
    this.posItems = [];
    this.currentTable = null;
    this.currentOrder = null;
    this.selectedCategory = null;
  }
  
  openPayment(): void {
    if (!this.currentTable || !this.currentOrder) {
      this.notificationService.warning('Debe guardar la orden primero');
      return;
    }
    
    this.orderToPay = this.currentOrder;
    const alreadyPaid = this.currentOrder.payments?.reduce((sum, p) => sum + p.amount, 0) || 0;
    const remaining = this.currentOrder.total - alreadyPaid;
    
    this.orderPayments = [{
      payment_method_id: 0,
      amount: remaining,
      reference: ''
    }];
    
    this.showPaymentModal = true;
  }
  
  closePaymentModal(): void {
    this.showPaymentModal = false;
    this.orderToPay = null;
    this.orderPayments = [];
  }
  
  addPayment(): void {
    this.orderPayments.push({
      payment_method_id: 0,
      amount: 0,
      reference: ''
    });
  }
  
  removePayment(index: number): void {
    this.orderPayments.splice(index, 1);
  }
  
  processPayment(): void {
    if (!this.orderToPay) return;
    
    const validPayments = this.orderPayments.filter(p => p.payment_method_id > 0 && p.amount > 0);
    
    if (validPayments.length === 0) {
      this.notificationService.warning('Debe agregar al menos un método de pago');
      return;
    }
    
    const alreadyPaid = this.orderToPay.payments?.reduce((sum, p) => sum + p.amount, 0) || 0;
    const newPaymentsTotal = validPayments.reduce((sum, p) => sum + p.amount, 0);
    const totalAfterPayments = alreadyPaid + newPaymentsTotal;
    
    if (totalAfterPayments > this.orderToPay.total + 0.01) {
      this.notificationService.error(`Los pagos exceden el total`);
      return;
    }
    
    const paymentData: AddPaymentsToOrder = { payments: validPayments };
    
    this.orderService.addPaymentsToOrder(this.orderToPay.id, paymentData).subscribe({
      next: () => {
        this.loadTables();
        this.closePaymentModal();
        this.notificationService.success('Pago registrado exitosamente');
      },
      error: (err) => {
        this.notificationService.error('Error: ' + (err.error?.detail || 'Error desconocido'));
      }
    });
  }
  
  getAlreadyPaid(order: Order): number {
    return order.payments?.reduce((sum, p) => sum + p.amount, 0) || 0;
  }
  
  getRemainingToPay(order: Order): number {
    return order.total - this.getAlreadyPaid(order);
  }
  
  calculatePaidAmount(): number {
    return this.orderPayments.reduce((sum, p) => sum + (Number(p.amount) || 0), 0);
  }
  
  hasValidPayments(): boolean {
    return this.orderPayments.some(p => p.payment_method_id > 0 && p.amount > 0);
  }
  
  getPaymentMethodIcon(type: string): string {
    const icons: Record<string, string> = {
      'cash': '💵',
      'card': '💳',
      'transfer': '🏦',
      'mobile_payment': '📱',
      'pago_movil': '📱',
      'transferencia': '🏦',
      'efectivo': '💵',
      'bolivares': '💵',
      'dolares': '💵',
      'euros': '💶',
      'other': '💰'
    };
    return icons[type] || '💰';
  }
  
  getItemsByCategory(categoryId: number): (MenuItem | Product)[] {
    const isMenuCategory = this.menuCategories.some(c => c.id === categoryId);
    
    if (isMenuCategory) {
      return this.menuItems.filter(m => m.category_id === categoryId && m.is_available);
    } else {
      return this.products.filter(p => p.category_id === categoryId && p.show_in_catalog === true);
    }
  }
  
  getItemName(item: any): string {
    if (item.source_type === 'menu' && item.menu_item_id) {
      const menuItem = this.menuItems.find(m => m.id === item.menu_item_id);
      return menuItem ? menuItem.name : `Menu Item #${item.menu_item_id}`;
    } else if (item.product_id) {
      const product = this.products.find(p => p.id === item.product_id);
      return product ? product.name : `Producto #${item.product_id}`;
    }
    return 'Item desconocido';
  }
  
  getItemDisplayPrice(item: any): number {
    return item.price !== undefined ? item.price : item.sale_price;
  }
  
  backToNormalView(): void {
    this.router.navigate(['/tables']);
  }
}

