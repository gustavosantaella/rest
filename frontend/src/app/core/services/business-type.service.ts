import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BusinessType } from '../models/configuration.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class BusinessTypeService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/business-types`;
  
  getBusinessTypes(): Observable<BusinessType[]> {
    return this.http.get<BusinessType[]>(this.apiUrl);
  }
  
  getBusinessTypeById(id: number): Observable<BusinessType> {
    return this.http.get<BusinessType>(`${this.apiUrl}/${id}`);
  }
}

