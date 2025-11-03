import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { OrderService } from '../../core/services/order.service';
import { ProductService } from '../../core/services/product.service';
import { TableService } from '../../core/services/table.service';
import { MenuService } from '../../core/services/menu.service';
import { PaymentMethodService } from '../../core/services/payment-method.service';
import { NotificationService } from '../../core/services/notification.service';
import { ConfirmService } from '../../core/services/confirm.service';
import { AuthPermissionsService } from '../../core/services/auth-permissions.service';
import { Order, OrderStatus, PaymentMethod, OrderCreate, OrderItemCreate, OrderPayment, PaymentStatus, AddPaymentsToOrder, UpdateOrderItems } from '../../core/models/order.model';
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
  private notificationService = inject(NotificationService);
  private confirmService = inject(ConfirmService);
  private authPermissionsService = inject(AuthPermissionsService);
  
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
  showEditModal = false;
  selectedOrder: Order | null = null;
  orderToPay: Order | null = null;
  orderToEdit: Order | null = null;
  orderForm!: FormGroup;
  editForm!: FormGroup;
  paymentForm!: FormGroup;
  loading = true;
  
  // Vista actual: 'list' | 'cards' | 'board'
  currentView: 'list' | 'cards' | 'board' = 'list';
  
  // Drag & Drop
  draggedOrder: Order | null = null;
  
  orderStatuses = Object.values(OrderStatus);
  paymentMethods = Object.values(PaymentMethod);
  
  // Exponer OrderStatus para el template
  OrderStatus = OrderStatus;
  PaymentMethod = PaymentMethod;
  PaymentStatus = PaymentStatus;
  Math = Math; // Exponer Math para usar en template
  
  statusLabels: Record<OrderStatus, string> = {
    [OrderStatus.PENDING]: 'Pendiente',
    [OrderStatus.PREPARING]: 'Preparando',
    [OrderStatus.COMPLETED]: 'Completada',
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
    
    this.editForm = this.fb.group({
      status: ['', Validators.required],
      items: this.fb.array([])
    });
  }
  
  get editItemsArray(): FormArray {
    return this.editForm.get('items') as FormArray;
  }
  
  get itemsArray(): FormArray {
    return this.orderForm.get('items') as FormArray;
  }
  
  addItem(): void {
    const item = this.fb.group({
      product_id: ['', Validators.required],
      quantity: [1, [Validators.required, Validators.min(0.01)]],
      notes: [''],
      source_type: [this.showMenuItems ? 'menu' : 'inventory'] // Recordar el tipo
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
        // Solo mostrar productos marcados como "mostrar en catálogo"
        this.products = products.filter(p => p.show_in_catalog);
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
    
    // Calcular el total estimado
    const totalEstimado = this.calculateEstimatedTotal();
    
    // Si hay pagos, validar que la suma sea correcta
    if (validPayments.length > 0) {
      const totalPagado = validPayments.reduce((sum, p) => sum + p.amount, 0);
      
      if (Math.abs(totalPagado - totalEstimado) > 0.01) {
        const falta = totalEstimado - totalPagado;
        if (falta > 0) {
          this.confirmService.confirm({
            title: 'Pago incompleto',
            message: `El pago no está completo. Faltan $${falta.toFixed(2)}\n\n¿Deseas crear la orden de todas formas?\n(Se marcará como "Pendiente de Pago")`,
            confirmText: 'Sí, crear orden',
            cancelText: 'No, revisar pago',
            type: 'warning'
          }).subscribe(confirmed => {
            if (confirmed) {
              this.createOrderWithData(validPayments);
            }
          });
          return;
        } else {
          this.notificationService.warning(`El pago excede el total. Sobran $${Math.abs(falta).toFixed(2)}. Ajusta los montos.`);
          return;
        }
      }
    }
    
    this.createOrderWithData(validPayments);
  }
  
  private createOrderWithData(validPayments: any[]): void {
    // Transformar items para usar menu_item_id o product_id según corresponda
    const transformedItems = this.orderForm.value.items.map((item: any) => {
      if (item.source_type === 'menu') {
        return {
          menu_item_id: Number(item.product_id),  // Renombrar product_id a menu_item_id
          quantity: item.quantity,
          notes: item.notes || '',
          source_type: 'menu'
        };
      } else {
        return {
          product_id: Number(item.product_id),
          quantity: item.quantity,
          notes: item.notes || '',
          source_type: 'product'  // Cambiar 'inventory' a 'product'
        };
      }
    });
    
    const orderData: OrderCreate = {
      table_id: this.orderForm.value.table_id || undefined,
      notes: this.orderForm.value.notes,
      customer_name: this.orderForm.value.customer_name || undefined,
      customer_email: this.orderForm.value.customer_email || undefined,
      customer_phone: this.orderForm.value.customer_phone || undefined,
      items: transformedItems,
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
        this.notificationService.success('Orden creada exitosamente');
      },
      error: (err) => {
        this.notificationService.error('Error al crear la orden: ' + (err.error?.detail || 'Error desconocido'));
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
      [OrderStatus.PENDING]: 'badge-warning',      // Amarillo - esperando
      [OrderStatus.PREPARING]: 'badge-info',       // Azul - en cocina
      [OrderStatus.COMPLETED]: 'badge-success',    // Verde - lista
      [OrderStatus.CANCELLED]: 'badge-danger'      // Rojo - cancelada
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
      this.notificationService.warning('Debe haber al menos un método de pago');
    }
  }
  
  calculatePaidAmount(): number {
    return this.orderPayments.reduce((sum, p) => sum + (p.amount || 0), 0);
  }
  
  get estimatedTotal(): number {
    let subtotal = 0;
    
    if (!this.orderForm) return 0;
    
    const items = this.orderForm.value.items || [];
    
    for (const item of items) {
      if (!item.product_id || !item.quantity) continue;
      
      // Verificar si el item es del menú o inventario según su source_type
      const isMenuType = item.source_type === 'menu';
      
      if (isMenuType) {
        // Buscar en el menú
        const menuItem = this.menuItems.find(m => m.id === Number(item.product_id));
        if (menuItem) {
          subtotal += menuItem.price * Number(item.quantity);
        }
      } else {
        // Buscar en el inventario
        const product = this.products.find(p => p.id === Number(item.product_id));
        if (product) {
          subtotal += product.sale_price * Number(item.quantity);
        }
      }
    }
    
    const tax = subtotal * 0.16; // 16% IVA
    return subtotal + tax;
  }
  
  calculateEstimatedTotal(): number {
    return this.estimatedTotal;
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
      this.notificationService.warning('Debe agregar al menos un método de pago');
      return;
    }
    
    // Calcular totales
    const alreadyPaid = this.orderToPay.payments?.reduce((sum, p) => sum + p.amount, 0) || 0;
    const newPaymentsTotal = validPayments.reduce((sum, p) => sum + p.amount, 0);
    const totalAfterPayments = alreadyPaid + newPaymentsTotal;
    
    // Validar que no exceda
    if (totalAfterPayments > this.orderToPay.total + 0.01) {
      this.notificationService.error(`Los pagos exceden el total.\n\nYa pagado: $${alreadyPaid.toFixed(2)}\nNuevo: $${newPaymentsTotal.toFixed(2)}\nTotal orden: $${this.orderToPay.total.toFixed(2)}`);
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
        this.notificationService.success('Pago registrado exitosamente');
      },
      error: (err) => {
        this.notificationService.error('Error al procesar el pago: ' + (err.error?.detail || 'Error desconocido'));
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
  
  // Modal de Edición
  openEditModal(order: Order): void {
    this.orderToEdit = order;
    this.editItemsArray.clear();
    
    // Cargar status actual
    this.editForm.patchValue({
      status: order.status
    });
    
    // Cargar items existentes
    order.items.forEach(item => {
      // Determinar si el item es del menú o inventario
      const isMenuItem = this.menuItems.some(m => m.id === item.product_id);
      
      const itemForm = this.fb.group({
        product_id: [item.product_id, Validators.required],
        quantity: [item.quantity, [Validators.required, Validators.min(0.01)]],
        notes: [item.notes || ''],
        source_type: [isMenuItem ? 'menu' : 'inventory']
      });
      this.editItemsArray.push(itemForm);
    });
    
    this.showEditModal = true;
  }
  
  closeEditModal(): void {
    this.showEditModal = false;
    this.orderToEdit = null;
  }
  
  addEditItem(): void {
    const item = this.fb.group({
      product_id: ['', Validators.required],
      quantity: [1, [Validators.required, Validators.min(0.01)]],
      notes: [''],
      source_type: [this.showMenuItems ? 'menu' : 'inventory'] // Recordar el tipo
    });
    this.editItemsArray.push(item);
  }
  
  removeEditItem(index: number): void {
    this.editItemsArray.removeAt(index);
  }

  // Método para verificar si un item es de menú
  isMenuItemSource(itemForm: any): boolean {
    return itemForm.get('source_type')?.value === 'menu';
  }
  
  saveEditedOrder(): void {
    if (!this.orderToEdit || this.editForm.invalid || this.editItemsArray.length === 0) return;
    
    // Transformar items para usar menu_item_id o product_id según corresponda
    const transformedItems = this.editForm.value.items.map((item: any) => {
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
    
    const itemsData: UpdateOrderItems = {
      items: transformedItems
    };
    
    const newStatus = this.editForm.value.status;
    
    // Actualizar items
    this.orderService.updateOrderItems(this.orderToEdit.id, itemsData).subscribe({
      next: () => {
        // Si el status cambió, actualizarlo también
        if (newStatus !== this.orderToEdit!.status) {
          this.orderService.updateOrder(this.orderToEdit!.id, { status: newStatus }).subscribe({
            next: () => {
              this.loadData();
              this.closeEditModal();
              this.notificationService.success('Orden actualizada exitosamente');
            }
          });
        } else {
          this.loadData();
          this.closeEditModal();
          this.notificationService.success('Orden actualizada exitosamente');
        }
      },
      error: (err) => {
        this.notificationService.error('Error al actualizar la orden: ' + (err.error?.detail || 'Error desconocido'));
      }
    });
  }
  
  canEditOrder(order: Order): boolean {
    // Solo se pueden editar órdenes pendientes o en preparación
    return order.status === OrderStatus.PENDING || order.status === OrderStatus.PREPARING;
  }
  
  getEditEstimatedTotal(): number {
    let subtotal = 0;
    
    if (!this.editForm) return 0;
    
    const items = this.editForm.value.items || [];
    
    for (const item of items) {
      if (!item.product_id || !item.quantity) continue;
      
      // Verificar si el item es del menú o inventario según su source_type
      const isMenuType = item.source_type === 'menu';
      
      if (isMenuType) {
        // Buscar en el menú
        const menuItem = this.menuItems.find(m => m.id === Number(item.product_id));
        if (menuItem) {
          subtotal += menuItem.price * Number(item.quantity);
        }
      } else {
        // Buscar en el inventario
        const product = this.products.find(p => p.id === Number(item.product_id));
        if (product) {
          subtotal += product.sale_price * Number(item.quantity);
        }
      }
    }
    
    const tax = subtotal * 0.16;
    return subtotal + tax;
  }
  
  // Métodos de verificación de permisos
  canViewOrders(): boolean {
    return this.authPermissionsService.hasPermission('orders.view');
  }
  
  canCreateOrders(): boolean {
    return this.authPermissionsService.hasPermission('orders.create');
  }
  
  canEditOrders(): boolean {
    return this.authPermissionsService.hasPermission('orders.edit');
  }
  
  canDeleteOrders(): boolean {
    return this.authPermissionsService.hasPermission('orders.delete');
  }
  
  canChangeOrderStatus(): boolean {
    return this.authPermissionsService.hasPermission('orders.change_status');
  }
  
  canProcessPayments(): boolean {
    return this.authPermissionsService.hasPermission('orders.process_payment');
  }
  
  quickChangeStatus(order: Order, newStatus: OrderStatus): void {
    if (!this.canChangeOrderStatus()) {
      this.notificationService.warning('No tienes permiso para cambiar el estado de órdenes');
      return;
    }
    
    this.orderService.updateOrder(order.id, { status: newStatus }).subscribe({
      next: () => {
        this.loadData();
        this.notificationService.success(`Estado cambiado a ${this.statusLabels[newStatus]}`);
      },
      error: (err) => {
        this.notificationService.error('Error al cambiar estado: ' + (err.error?.detail || 'Error desconocido'));
      }
    });
  }
  
  // ========== MÉTODOS PARA VISTAS ==========
  
  setView(view: 'list' | 'cards' | 'board'): void {
    this.currentView = view;
  }
  
  getOrdersByStatus(status: OrderStatus): Order[] {
    return this.orders.filter(order => order.status === status);
  }
  
  // ========== MÉTODOS PARA DRAG & DROP ==========
  
  onDragStart(event: DragEvent, order: Order): void {
    this.draggedOrder = order;
    if (event.dataTransfer) {
      event.dataTransfer.effectAllowed = 'move';
      event.dataTransfer.setData('text/html', '');
    }
  }
  
  onDragOver(event: DragEvent): void {
    if (event.preventDefault) {
      event.preventDefault();
    }
    if (event.dataTransfer) {
      event.dataTransfer.dropEffect = 'move';
    }
    return;
  }
  
  onDrop(event: DragEvent, newStatus: OrderStatus): void {
    if (event.stopPropagation) {
      event.stopPropagation();
    }
    event.preventDefault();
    
    if (this.draggedOrder && this.draggedOrder.status !== newStatus) {
      if (!this.canChangeOrderStatus()) {
        this.notificationService.warning('No tienes permiso para cambiar el estado de órdenes');
        this.draggedOrder = null;
        return;
      }
      
      this.quickChangeStatus(this.draggedOrder, newStatus);
    }
    
    this.draggedOrder = null;
    return;
  }
  
  onDragEnd(): void {
    this.draggedOrder = null;
  }
}

