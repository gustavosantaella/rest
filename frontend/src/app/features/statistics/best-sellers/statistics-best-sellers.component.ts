import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { StatisticsService } from '../../../core/services/statistics.service';
import { BestSellersStatistics } from '../../../core/models/statistics.model';
import { BarChartComponent } from '../../../shared/components/charts/bar-chart.component';

@Component({
  selector: 'app-statistics-best-sellers',
  standalone: true,
  imports: [CommonModule, FormsModule, BarChartComponent],
  templateUrl: './statistics-best-sellers.component.html',
  styleUrls: ['./statistics-best-sellers.component.scss']
})
export class StatisticsBestSellersComponent implements OnInit {
  private statisticsService = inject(StatisticsService);
  
  statistics: BestSellersStatistics | null = null;
  loading = true;
  selectedPeriod = 30;
  
  // Datos pre-calculados
  bestProductsChartData: { labels: string[], data: number[] } = { labels: [], data: [] };
  bestMenuChartData: { labels: string[], data: number[] } = { labels: [], data: [] };
  
  periodOptions = [
    { value: 7, label: 'Últimos 7 días' },
    { value: 30, label: 'Últimos 30 días' },
    { value: 60, label: 'Últimos 60 días' },
    { value: 90, label: 'Últimos 90 días' }
  ];
  
  ngOnInit(): void {
    this.loadStatistics();
  }
  
  loadStatistics(): void {
    this.loading = true;
    this.statisticsService.getBestSellers(this.selectedPeriod, 10).subscribe({
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
    
    // Calcular datos de gráficos una sola vez
    this.bestProductsChartData = {
      labels: this.statistics.best_products.map(p => p.name),
      data: this.statistics.best_products.map(p => p.quantity)
    };
    
    this.bestMenuChartData = {
      labels: this.statistics.best_menu_items.map(m => m.name),
      data: this.statistics.best_menu_items.map(m => m.quantity)
    };
  }
}

