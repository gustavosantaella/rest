import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UploadService {
  private apiUrl = `${environment.apiUrl}/upload`;

  constructor(private http: HttpClient) { }

  uploadImage(file: File): Observable<{ image_url: string; filename: string }> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<{ image_url: string; filename: string }>(`${this.apiUrl}/image`, formData);
  }

  deleteImage(imageUrl: string): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${this.apiUrl}/image`, {
      params: { image_url: imageUrl }
    });
  }

  getFullImageUrl(imageUrl: string | undefined): string {
    if (!imageUrl) return '';
    
    // Si ya es una URL completa, retornarla tal cual
    if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) {
      return imageUrl;
    }
    
    // Si es una ruta relativa del servidor, agregar el base URL
    return `${environment.apiUrl.replace('/api', '')}${imageUrl}`;
  }
}

