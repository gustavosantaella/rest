import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Table, TableCreate } from '../models/table.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class TableService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/tables`;
  
  getTables(): Observable<Table[]> {
    return this.http.get<Table[]>(this.apiUrl);
  }
  
  getTable(id: number): Observable<Table> {
    return this.http.get<Table>(`${this.apiUrl}/${id}`);
  }
  
  createTable(table: TableCreate): Observable<Table> {
    return this.http.post<Table>(this.apiUrl, table);
  }
  
  updateTable(id: number, table: Partial<Table>): Observable<Table> {
    return this.http.put<Table>(`${this.apiUrl}/${id}`, table);
  }
  
  deleteTable(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}

