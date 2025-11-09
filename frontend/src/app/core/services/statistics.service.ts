import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  GeneralStatistics,
  BestSellersStatistics,
  CustomerStatistics,
  FinancialStatistics
} from '../models/statistics.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class StatisticsService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/statistics`;

  getGeneralStatistics(days: number = 30): Observable<GeneralStatistics> {
    const params = new HttpParams().set('days', days.toString());
    return this.http.get<GeneralStatistics>(`${this.apiUrl}/general`, { params });
  }

  getBestSellers(days: number = 30, limit: number = 10): Observable<BestSellersStatistics> {
    const params = new HttpParams()
      .set('days', days.toString())
      .set('limit', limit.toString());
    return this.http.get<BestSellersStatistics>(`${this.apiUrl}/best-sellers`, { params });
  }

  getCustomerStatistics(): Observable<CustomerStatistics> {
    return this.http.get<CustomerStatistics>(`${this.apiUrl}/customers`);
  }

  getFinancialStatistics(days: number = 30): Observable<FinancialStatistics> {
    const params = new HttpParams().set('days', days.toString());
    return this.http.get<FinancialStatistics>(`${this.apiUrl}/financial`, { params });
  }
}

