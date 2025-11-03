import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BusinessConfiguration, BusinessConfigurationCreate, Partner, PartnerCreate } from '../models/configuration.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ConfigurationService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/configuration`;
  
  // Business Configuration
  getConfiguration(): Observable<BusinessConfiguration> {
    return this.http.get<BusinessConfiguration>(this.apiUrl);
  }
  
  createConfiguration(config: BusinessConfigurationCreate): Observable<BusinessConfiguration> {
    return this.http.post<BusinessConfiguration>(this.apiUrl, config);
  }
  
  updateConfiguration(config: Partial<BusinessConfigurationCreate>): Observable<BusinessConfiguration> {
    return this.http.put<BusinessConfiguration>(this.apiUrl, config);
  }
  
  // Partners
  getPartners(): Observable<Partner[]> {
    return this.http.get<Partner[]>(`${this.apiUrl}/partners`);
  }
  
  addPartner(partner: PartnerCreate): Observable<Partner> {
    return this.http.post<Partner>(`${this.apiUrl}/partners`, partner);
  }
  
  updatePartner(id: number, partner: Partial<PartnerCreate>): Observable<Partner> {
    return this.http.put<Partner>(`${this.apiUrl}/partners/${id}`, partner);
  }
  
  deletePartner(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/partners/${id}`);
  }

  // QR Code
  downloadQRCode(): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/qr-code`, {
      responseType: 'blob'
    });
  }
}

