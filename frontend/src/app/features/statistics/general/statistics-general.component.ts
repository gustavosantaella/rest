import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { StatisticsService } from '../../../core/services/statistics.service';
import { GeneralStatistics } from '../../../core/models/statistics.model';
import { LineChartComponent } from '../../../shared/components/charts/line-chart.component';

@Component({
  selector: 'app-statistics-general',
  standalone: true,
  imports: [CommonModule, FormsModule, LineChartComponent],
  templateUrl: './statistics-general.component.html',
  styleUrls: ['./statistics-general.component.scss']
})
export class StatisticsGeneralComponent implements OnInit {
  private statisticsService = inject(StatisticsService);
  
  statistics: GeneralStatistics | null = null;
  loading = true;
  selectedPeriod = 30;
  
  // Datos pre-calculados
  completionRate = 0;
  cancellationRate = 0;
  chartData: { labels: string[], values: number[] } = { labels: [], values: [] };
  
  periodOptions = [
    { value: 7, label: 'Últimos 7 días' },
    { value: 15, label: 'Últimos 15 días' },
    { value: 30, label: 'Últimos 30 días' },
    { value: 60, label: 'Últimos 60 días' },
    { value: 90, label: 'Últimos 90 días' }
  ];
  
  ngOnInit(): void {
    this.loadStatistics();
  }
  
  loadStatistics(): void {
    this.loading = true;
    this.statisticsService.getGeneralStatistics(this.selectedPeriod).subscribe({
      next: (stats) => {
        this.statistics = stats;
        this.calculateMetrics();
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando estadísticas:', err);
        this.loading = false;
      }
    });
  }
  
  onPeriodChange(): void {
    this.loadStatistics();
  }
  
  calculateMetrics(): void {
    if (!this.statistics) return;
    
    // Calcular tasas una sola vez
    if (this.statistics.total_orders > 0) {
      this.completionRate = (this.statistics.completed_orders / this.statistics.total_orders) * 100;
      this.cancellationRate = (this.statistics.cancelled_orders / this.statistics.total_orders) * 100;
    } else {
      this.completionRate = 0;
      this.cancellationRate = 0;
    }
    
    // Preparar datos del gráfico con validación defensiva
    const revenueByDay = this.statistics.revenue_by_day || {};
    const sortedDates = Object.keys(revenueByDay).sort();
    this.chartData = {
      labels: sortedDates.map(d => new Date(d).toLocaleDateString('es-ES', { month: 'short', day: 'numeric' })),
      values: sortedDates.map(d => revenueByDay[d] || 0)
    };
  }
}

