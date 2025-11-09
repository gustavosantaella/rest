import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { OrderService } from '../../core/services/order.service';
import { PaymentMethodService } from '../../core/services/payment-method.service';
import { Order, OrderStatus } from '../../core/models/order.model';
import { PaymentMethod } from '../../core/models/payment-method.model';

interface DailySummary {
  totalSales: number;
  totalOrders: number;
  completedOrders: number;
  cancelledOrders: number;
  averageTicket: number;
}

interface PaymentMethodSummary {
  methodId: number;
  methodName: string;
  amount: number;
  count: number;
}

interface ProductSummary {
  productName: string;
  quantity: number;
  total: number;
}

@Component({
  selector: 'app-cash-closing',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './cash-closing.component.html',
  styleUrls: ['./cash-closing.component.scss']
})
export class CashClosingComponent implements OnInit {
  private orderService = inject(OrderService);
  private paymentMethodService = inject(PaymentMethodService);
  
  selectedDate: string = '';
  loading = false;
  currentDate = new Date();
  
  summary: DailySummary = {
    totalSales: 0,
    totalOrders: 0,
    completedOrders: 0,
    cancelledOrders: 0,
    averageTicket: 0
  };
  
  paymentMethodSummaries: PaymentMethodSummary[] = [];
  productSummaries: ProductSummary[] = [];
  todayOrders: Order[] = [];
  paymentMethods: PaymentMethod[] = [];
  
  ngOnInit(): void {
    // Establecer la fecha de hoy por defecto
    const today = new Date();
    this.selectedDate = this.formatDateForInput(today);
    this.loadPaymentMethods();
    this.loadDailyData();
  }
  
  formatDateForInput(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
  
  loadPaymentMethods(): void {
    this.paymentMethodService.getPaymentMethods().subscribe({
      next: (methods) => {
        this.paymentMethods = methods;
      },
      error: (err) => {
        console.error('Error cargando métodos de pago:', err);
      }
    });
  }
  
  loadDailyData(): void {
    this.loading = true;
    this.currentDate = new Date(); // Actualizar timestamp del reporte
    
    this.orderService.getOrders().subscribe({
      next: (orders) => {
        this.processOrders(orders);
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando órdenes:', err);
        this.loading = false;
      }
    });
  }
  
  processOrders(allOrders: Order[]): void {
    // Parsear la fecha seleccionada correctamente (evitar problemas de timezone)
    const [year, month, day] = this.selectedDate.split('-').map(Number);
    
    this.todayOrders = allOrders.filter(order => {
      const orderDate = new Date(order.created_at);
      const orderYear = orderDate.getFullYear();
      const orderMonth = orderDate.getMonth() + 1; // getMonth() retorna 0-11
      const orderDay = orderDate.getDate();
      
      return orderYear === year && orderMonth === month && orderDay === day;
    });
    
    // Calcular resumen general
    this.calculateSummary();
    
    // Calcular resumen por métodos de pago
    this.calculatePaymentMethodSummary();
    
    // Calcular productos vendidos
    this.calculateProductSummary();
  }
  
  calculateSummary(): void {
    const paidOrders = this.todayOrders.filter(o => o.payment_status === 'paid');
    
    this.summary = {
      totalOrders: this.todayOrders.length,
      completedOrders: this.todayOrders.filter(o => o.status === OrderStatus.COMPLETED).length,
      cancelledOrders: this.todayOrders.filter(o => o.status === OrderStatus.CANCELLED).length,
      totalSales: paidOrders.reduce((sum, o) => sum + o.total, 0),
      averageTicket: paidOrders.length > 0 
        ? paidOrders.reduce((sum, o) => sum + o.total, 0) / paidOrders.length 
        : 0
    };
  }
  
  calculatePaymentMethodSummary(): void {
    const paidOrders = this.todayOrders.filter(o => o.payment_status === 'paid');
    const paymentMap = new Map<number, { amount: number; count: number; name: string }>();
    
    paidOrders.forEach(order => {
      if (order.payments && order.payments.length > 0) {
        order.payments.forEach(payment => {
          const methodId = payment.payment_method_id;
          const methodName = payment.payment_method_name || this.getPaymentMethodName(methodId);
          
          if (!paymentMap.has(methodId)) {
            paymentMap.set(methodId, { amount: 0, count: 0, name: methodName });
          }
          
          const current = paymentMap.get(methodId)!;
          current.amount += payment.amount;
          current.count += 1;
        });
      }
    });
    
    this.paymentMethodSummaries = Array.from(paymentMap.entries()).map(([methodId, data]) => ({
      methodId,
      methodName: data.name,
      amount: data.amount,
      count: data.count
    })).sort((a, b) => b.amount - a.amount);
  }
  
  getPaymentMethodName(methodId: number): string {
    const method = this.paymentMethods.find(m => m.id === methodId);
    return method ? method.name : `Método ${methodId}`;
  }
  
  calculateProductSummary(): void {
    const productMap = new Map<string, { quantity: number; total: number }>();
    
    this.todayOrders.forEach(order => {
      if (order.items && order.items.length > 0) {
        order.items.forEach(item => {
          // Usar el nombre del producto o ítem de menú
          const productName = this.getItemName(item);
          
          if (!productMap.has(productName)) {
            productMap.set(productName, { quantity: 0, total: 0 });
          }
          
          const current = productMap.get(productName)!;
          current.quantity += item.quantity;
          current.total += item.subtotal;
        });
      }
    });
    
    this.productSummaries = Array.from(productMap.entries())
      .map(([productName, data]) => ({
        productName,
        quantity: data.quantity,
        total: data.total
      }))
      .sort((a, b) => b.quantity - a.quantity)
      .slice(0, 10); // Top 10 productos
  }
  
  getItemName(item: any): string {
    // Aquí podrías hacer una llamada para obtener el nombre real del producto
    // Por ahora retornamos un identificador
    if (item.product_id) {
      return `Producto #${item.product_id}`;
    } else if (item.menu_item_id) {
      return `Menú #${item.menu_item_id}`;
    }
    return 'Producto desconocido';
  }
  
  onDateChange(): void {
    this.loadDailyData();
  }
  
  printReport(): void {
    window.print();
  }
  
  exportToCSV(): void {
    // Preparar datos para CSV
    let csv = 'CIERRE DE CAJA - ' + this.selectedDate + '\n\n';
    
    csv += 'RESUMEN GENERAL\n';
    csv += `Total Ventas,$${this.summary.totalSales.toFixed(2)}\n`;
    csv += `Total Órdenes,${this.summary.totalOrders}\n`;
    csv += `Órdenes Completadas,${this.summary.completedOrders}\n`;
    csv += `Órdenes Canceladas,${this.summary.cancelledOrders}\n`;
    csv += `Ticket Promedio,$${this.summary.averageTicket.toFixed(2)}\n\n`;
    
    csv += 'MÉTODOS DE PAGO\n';
    csv += 'Método,Cantidad,Monto\n';
    this.paymentMethodSummaries.forEach(pm => {
      csv += `${pm.methodName},${pm.count},$${pm.amount.toFixed(2)}\n`;
    });
    
    csv += '\nPRODUCTOS MÁS VENDIDOS\n';
    csv += 'Producto,Cantidad,Total\n';
    this.productSummaries.forEach(ps => {
      csv += `${ps.productName},${ps.quantity},$${ps.total.toFixed(2)}\n`;
    });
    
    // Descargar CSV
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `cierre-caja-${this.selectedDate}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
  
  getOrderStatusClass(status: OrderStatus): string {
    const classes: Record<OrderStatus, string> = {
      [OrderStatus.PENDING]: 'badge-warning',
      [OrderStatus.PREPARING]: 'badge-info',
      [OrderStatus.COMPLETED]: 'badge-success',
      [OrderStatus.CANCELLED]: 'badge-danger'
    };
    return classes[status];
  }
  
  getOrderStatusText(status: OrderStatus): string {
    const texts: Record<OrderStatus, string> = {
      [OrderStatus.PENDING]: 'Pendiente',
      [OrderStatus.PREPARING]: 'Preparando',
      [OrderStatus.COMPLETED]: 'Completada',
      [OrderStatus.CANCELLED]: 'Cancelada'
    };
    return texts[status];
  }
  
  formatDateTime(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleString('es-ES', {
      hour: '2-digit',
      minute: '2-digit',
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  }
}

