import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { OrderService } from '../../core/services/order.service';
import { ProductService } from '../../core/services/product.service';
import { TableService } from '../../core/services/table.service';
import { Order, OrderStatus } from '../../core/models/order.model';
import { Product } from '../../core/models/product.model';
import { Table, TableStatus } from '../../core/models/table.model';

interface DashboardStats {
  totalOrders: number;
  pendingOrders: number;
  availableTables: number;
  lowStockProducts: number;
  todayRevenue: number;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  private orderService = inject(OrderService);
  private productService = inject(ProductService);
  private tableService = inject(TableService);
  
  stats: DashboardStats = {
    totalOrders: 0,
    pendingOrders: 0,
    availableTables: 0,
    lowStockProducts: 0,
    todayRevenue: 0
  };
  
  recentOrders: Order[] = [];
  loading = true;
  
  ngOnInit(): void {
    this.loadDashboardData();
  }
  
  loadDashboardData(): void {
    this.loading = true;
    
    // Load orders
    this.orderService.getOrders().subscribe({
      next: (orders) => {
        this.stats.totalOrders = orders.length;
        this.stats.pendingOrders = orders.filter(o => o.status === OrderStatus.PENDING || o.status === OrderStatus.IN_PROGRESS).length;
        this.stats.todayRevenue = orders
          .filter(o => o.status === OrderStatus.PAID)
          .reduce((sum, o) => sum + o.total, 0);
        this.recentOrders = orders.slice(0, 5);
      }
    });
    
    // Load tables
    this.tableService.getTables().subscribe({
      next: (tables) => {
        this.stats.availableTables = tables.filter(t => t.status === TableStatus.AVAILABLE).length;
      }
    });
    
    // Load products
    this.productService.getProducts().subscribe({
      next: (products) => {
        this.stats.lowStockProducts = products.filter(p => p.stock <= p.min_stock).length;
        this.loading = false;
      }
    });
  }
  
  getOrderStatusClass(status: OrderStatus): string {
    const classes: Record<OrderStatus, string> = {
      [OrderStatus.PENDING]: 'badge-warning',
      [OrderStatus.IN_PROGRESS]: 'badge-info',
      [OrderStatus.COMPLETED]: 'badge-success',
      [OrderStatus.PAID]: 'badge-success',
      [OrderStatus.CANCELLED]: 'badge-danger'
    };
    return classes[status];
  }
  
  getOrderStatusText(status: OrderStatus): string {
    const texts: Record<OrderStatus, string> = {
      [OrderStatus.PENDING]: 'Pendiente',
      [OrderStatus.IN_PROGRESS]: 'En Progreso',
      [OrderStatus.COMPLETED]: 'Completada',
      [OrderStatus.PAID]: 'Pagada',
      [OrderStatus.CANCELLED]: 'Cancelada'
    };
    return texts[status];
  }
}

