import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { StatisticsService } from '../../../core/services/statistics.service';
import { FinancialStatistics } from '../../../core/models/statistics.model';
import { PieChartComponent } from '../../../shared/components/charts/pie-chart.component';
import { BarChartComponent } from '../../../shared/components/charts/bar-chart.component';

@Component({
  selector: 'app-statistics-financial',
  standalone: true,
  imports: [CommonModule, FormsModule, PieChartComponent, BarChartComponent],
  templateUrl: './statistics-financial.component.html',
  styleUrls: ['./statistics-financial.component.scss']
})
export class StatisticsFinancialComponent implements OnInit {
  private statisticsService = inject(StatisticsService);
  
  statistics: FinancialStatistics | null = null;
  loading = true;
  selectedPeriod = 30;
  
  // Datos pre-calculados para evitar recalcular en cada ciclo de detección
  paymentMethods: { name: string, amount: number }[] = [];
  paymentMethodsChartData: { labels: string[], data: number[] } = { labels: [], data: [] };
  incomeVsExpensesData: { labels: string[], data: number[] } = { labels: [], data: [] };
  
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
    this.statisticsService.getFinancialStatistics(this.selectedPeriod).subscribe({
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
    
    // Validar que income_by_method existe y no es null
    const incomeByMethod = this.statistics.income_by_method || {};
    
    // Calcular métodos de pago una sola vez
    this.paymentMethods = Object.entries(incomeByMethod)
      .map(([name, amount]) => ({ name, amount: amount as number }))
      .sort((a, b) => b.amount - a.amount);
    
    // Datos para gráfico de pastel
    this.paymentMethodsChartData = {
      labels: this.paymentMethods.map(m => m.name),
      data: this.paymentMethods.map(m => m.amount)
    };
    
    // Datos para gráfico de barras comparativo - con valores por defecto
    this.incomeVsExpensesData = {
      labels: ['Ingresos', 'Egresos', 'Ganancia Neta'],
      data: [
        this.statistics.total_income ?? 0,
        this.statistics.total_expenses ?? 0,
        this.statistics.net_profit ?? 0
      ]
    };
  }
}

