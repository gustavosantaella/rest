import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Product } from '../models/product.model';
import { MenuItem, MenuCategory } from '../models/menu.model';

export interface BusinessInfo {
  business_name: string;
  slug: string;
  phone?: string;
  email?: string;
  address?: string;
  logo_url?: string;
  currency: string;
}

@Injectable({
  providedIn: 'root'
})
export class PublicService {
  private apiUrl = `${environment.apiUrl}/public`;

  constructor(private http: HttpClient) { }

  getBusinessInfo(slug: string): Observable<BusinessInfo> {
    return this.http.get<BusinessInfo>(`${this.apiUrl}/${slug}/info`);
  }

  getProducts(slug: string): Observable<Product[]> {
    return this.http.get<Product[]>(`${this.apiUrl}/${slug}/products`);
  }

  getMenu(slug: string): Observable<MenuItem[]> {
    return this.http.get<MenuItem[]>(`${this.apiUrl}/${slug}/menu`);
  }

  getMenuCategories(slug: string): Observable<MenuCategory[]> {
    return this.http.get<MenuCategory[]>(`${this.apiUrl}/${slug}/menu-categories`);
  }

  getMenuItemDetail(slug: string, itemId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${slug}/menu/${itemId}`);
  }
}

