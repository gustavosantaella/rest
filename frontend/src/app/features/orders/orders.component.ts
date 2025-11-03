import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { OrderService } from '../../core/services/order.service';
import { ProductService } from '../../core/services/product.service';
import { TableService } from '../../core/services/table.service';
import { MenuService } from '../../core/services/menu.service';
import { PaymentMethodService } from '../../core/services/payment-method.service';
import { Order, OrderStatus, PaymentMethod, OrderCreate, OrderItemCreate, OrderPayment, PaymentStatus, AddPaymentsToOrder } from '../../core/models/order.model';
import { PaymentMethod as PaymentMethodModel, PAYMENT_METHOD_LABELS } from '../../core/models/payment-method.model';
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
  private paymentMethodService = inject(PaymentMethodService);
  private fb = inject(FormBuilder);
  
  orders: Order[] = [];
  products: Product[] = [];
  menuItems: MenuItem[] = [];
  tables: Table[] = [];
  activePaymentMethods: PaymentMethodModel[] = [];
  
  // Pagos de la orden actual
  orderPayments: OrderPayment[] = [];
  
  showMenuItems = true; // Toggle para mostrar menú o inventario
  
  showModal = false;
  showDetailModal = false;
  showPaymentModal = false;
  selectedOrder: Order | null = null;
  orderToPay: Order | null = null;
  orderForm!: FormGroup;
  paymentForm!: FormGroup;
  loading = true;
  
  orderStatuses = Object.values(OrderStatus);
  paymentMethods = Object.values(PaymentMethod);
  
  // Exponer OrderStatus para el template
  OrderStatus = OrderStatus;
  PaymentMethod = PaymentMethod;
  PaymentStatus = PaymentStatus;
  Math = Math; // Exponer Math para usar en template
  
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
      customer_name: [''],
      customer_email: [''],
      customer_phone: [''],
      items: this.fb.array([])
    });
    
    this.paymentForm = this.fb.group({
      customer_name: [''],
      customer_email: ['', Validators.email],
      customer_phone: ['']
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
    
    // Cargar métodos de pago activos
    this.paymentMethodService.getActivePaymentMethods().subscribe({
      next: (methods) => {
        this.activePaymentMethods = methods;
      }
    });
    
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
    
    // Reset payments - iniciar vacío (pago opcional)
    this.orderPayments = [];
    
    this.showModal = true;
  }
  
  closeModal(): void {
    this.showModal = false;
  }
  
  saveOrder(): void {
    if (this.orderForm.invalid || this.itemsArray.length === 0) return;
    
    // Filtrar pagos válidos (que tengan método seleccionado y monto > 0)
    const validPayments = this.orderPayments.filter(p => p.payment_method_id > 0 && p.amount > 0);
    
    // Si hay pagos, validar que la suma sea correcta
    if (validPayments.length > 0) {
      const totalEstimado = this.calculateEstimatedTotal();
      const totalPagado = validPayments.reduce((sum, p) => sum + p.amount, 0);
      
      if (Math.abs(totalPagado - totalEstimado) > 0.01) {
        const falta = totalEstimado - totalPagado;
        if (falta > 0) {
          const confirmacion = confirm(
            `El pago no está completo. Faltan $${falta.toFixed(2)}\n\n` +
            `¿Deseas crear la orden de todas formas?\n` +
            `(Se marcará como "Pendiente de Pago")`
          );
          if (!confirmacion) return;
        } else {
          alert(`El pago excede el total. Sobran $${Math.abs(falta).toFixed(2)}\n\nAjusta los montos.`);
          return;
        }
      }
    }
    
    const orderData: OrderCreate = {
      table_id: this.orderForm.value.table_id || undefined,
      notes: this.orderForm.value.notes,
      customer_name: this.orderForm.value.customer_name || undefined,
      customer_email: this.orderForm.value.customer_email || undefined,
      customer_phone: this.orderForm.value.customer_phone || undefined,
      items: this.orderForm.value.items,
      payments: validPayments.map(p => ({
        payment_method_id: p.payment_method_id,
        amount: p.amount,
        reference: p.reference || undefined
      }))
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
  
  // Método eliminado - Los pagos se manejan al crear la orden
  
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
  
  // Métodos de Pago
  addPayment(): void {
    this.orderPayments.push({
      payment_method_id: 0,
      amount: 0,
      reference: ''
    });
  }
  
  removePayment(index: number): void {
    if (this.orderPayments.length > 1) {
      this.orderPayments.splice(index, 1);
    } else {
      alert('Debe haber al menos un método de pago');
    }
  }
  
  calculatePaidAmount(): number {
    return this.orderPayments.reduce((sum, p) => sum + (p.amount || 0), 0);
  }
  
  calculateEstimatedTotal(): number {
    let subtotal = 0;
    
    for (const item of this.orderForm.value.items) {
      if (this.showMenuItems) {
        // Si usa menú
        const menuItem = this.menuItems.find(m => m.id === item.product_id);
        if (menuItem) {
          subtotal += menuItem.price * item.quantity;
        }
      } else {
        // Si usa inventario
        const product = this.products.find(p => p.id === item.product_id);
        if (product) {
          subtotal += product.sale_price * item.quantity;
        }
      }
    }
    
    const tax = subtotal * 0.16; // 16% IVA
    return subtotal + tax;
  }
  
  getRemainingAmount(): number {
    return this.calculateEstimatedTotal() - this.calculatePaidAmount();
  }
  
  isFullyPaid(): boolean {
    return Math.abs(this.getRemainingAmount()) <= 0.01;
  }
  
  getPaymentMethodName(methodId: number): string {
    const method = this.activePaymentMethods.find(m => m.id === methodId);
    return method ? method.name : 'Seleccionar método';
  }
  
  getPaymentMethodIcon(type: string): string {
    const icons: Record<string, string> = {
      'pago_movil': '💳',
      'transferencia': '🏦',
      'efectivo': '💵',
      'bolivares': 'Bs',
      'dolares': '$',
      'euros': '€'
    };
    return icons[type] || '💰';
  }
  
  getPaymentStatusBadge(status: string): string {
    const badges: Record<string, string> = {
      'pending': 'badge-warning',
      'partial': 'badge-info',
      'paid': 'badge-success'
    };
    return badges[status] || 'badge-secondary';
  }
  
  getPaymentStatusLabel(status: string): string {
    const labels: Record<string, string> = {
      'pending': 'Pendiente',
      'partial': 'Parcial',
      'paid': 'Pagado'
    };
    return labels[status] || status;
  }
  
  getAbsoluteValue(value: number): number {
    return Math.abs(value);
  }
  
  hasValidPayments(): boolean {
    return this.orderPayments.length > 0 && 
           this.orderPayments.some(p => p.payment_method_id > 0 && p.amount > 0);
  }
  
  // Modal de Pago
  openPaymentModal(order: Order): void {
    this.orderToPay = order;
    
    // Calcular cuánto falta por pagar
    const alreadyPaid = order.payments?.reduce((sum, p) => sum + p.amount, 0) || 0;
    const remaining = order.total - alreadyPaid;
    
    // Iniciar con un pago por el monto restante
    this.orderPayments = [
      {
        payment_method_id: 0,
        amount: remaining,
        reference: ''
      }
    ];
    
    // Reset form de cliente
    this.paymentForm.patchValue({
      customer_name: order.customer_name || '',
      customer_email: order.customer_email || '',
      customer_phone: order.customer_phone || ''
    });
    
    this.showPaymentModal = true;
  }
  
  closePaymentModal(): void {
    this.showPaymentModal = false;
    this.orderToPay = null;
    this.orderPayments = [];
  }
  
  processPayment(): void {
    if (!this.orderToPay) return;
    
    // Filtrar pagos válidos
    const validPayments = this.orderPayments.filter(p => p.payment_method_id > 0 && p.amount > 0);
    
    if (validPayments.length === 0) {
      alert('Debe agregar al menos un método de pago');
      return;
    }
    
    // Calcular totales
    const alreadyPaid = this.orderToPay.payments?.reduce((sum, p) => sum + p.amount, 0) || 0;
    const newPaymentsTotal = validPayments.reduce((sum, p) => sum + p.amount, 0);
    const totalAfterPayments = alreadyPaid + newPaymentsTotal;
    
    // Validar que no exceda
    if (totalAfterPayments > this.orderToPay.total + 0.01) {
      alert(`Los pagos exceden el total.\n\nYa pagado: $${alreadyPaid.toFixed(2)}\nNuevo: $${newPaymentsTotal.toFixed(2)}\nTotal orden: $${this.orderToPay.total.toFixed(2)}`);
      return;
    }
    
    // Preparar datos
    const paymentData: AddPaymentsToOrder = {
      payments: validPayments
    };
    
    // Actualizar datos del cliente si se llenaron
    const customerData = this.paymentForm.value;
    if (customerData.customer_name || customerData.customer_email || customerData.customer_phone) {
      this.orderService.updateOrder(this.orderToPay.id, {
        customer_name: customerData.customer_name || undefined,
        customer_email: customerData.customer_email || undefined,
        customer_phone: customerData.customer_phone || undefined
      }).subscribe();
    }
    
    // Agregar pagos
    this.orderService.addPaymentsToOrder(this.orderToPay.id, paymentData).subscribe({
      next: () => {
        this.loadData();
        this.closePaymentModal();
        alert('✅ Pago registrado exitosamente');
      },
      error: (err) => {
        alert('Error al procesar el pago: ' + (err.error?.detail || 'Error desconocido'));
      }
    });
  }
  
  getAlreadyPaid(order: Order): number {
    return order.payments?.reduce((sum, p) => sum + p.amount, 0) || 0;
  }
  
  getRemainingToPay(order: Order): number {
    return order.total - this.getAlreadyPaid(order);
  }
  
  canPayOrder(order: Order): boolean {
    return order.payment_status !== 'paid';
  }
}

