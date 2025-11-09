import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StatisticsService } from '../../../core/services/statistics.service';
import { CustomerStatistics } from '../../../core/models/statistics.model';
import { BarChartComponent } from '../../../shared/components/charts/bar-chart.component';

@Component({
  selector: 'app-statistics-customers',
  standalone: true,
  imports: [CommonModule, BarChartComponent],
  templateUrl: './statistics-customers.component.html',
  styleUrls: ['./statistics-customers.component.scss']
})
export class StatisticsCustomersComponent implements OnInit {
  private statisticsService = inject(StatisticsService);
  
  statistics: CustomerStatistics | null = null;
  loading = true;
  
  // Datos pre-calculados
  debtChartData: { labels: string[], data: number[] } = { labels: [], data: [] };
  
  ngOnInit(): void {
    this.loadStatistics();
  }
  
  loadStatistics(): void {
    this.loading = true;
    this.statisticsService.getCustomerStatistics().subscribe({
      next: (stats) => {
        this.statistics = stats;
        this.calculateChartData();
        this.loading = false;
      },
      error: (err) => {
        console.error('Error:', err);
        this.loading = false;
      }
    });
  }
  
  calculateChartData(): void {
    if (!this.statistics) return;
    
    // Calcular datos del gráfico una sola vez
    this.debtChartData = {
      labels: this.statistics.customers_with_debt.map(c => c.name),
      data: this.statistics.customers_with_debt.map(c => c.total_pending)
    };
  }
}

