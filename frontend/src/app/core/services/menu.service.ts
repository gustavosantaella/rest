import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { MenuItem, MenuItemCreate, MenuCategory, MenuCategoryCreate } from '../models/menu.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MenuService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/menu`;
  
  // Categories
  getCategories(): Observable<MenuCategory[]> {
    return this.http.get<MenuCategory[]>(`${this.apiUrl}/categories`);
  }
  
  createCategory(category: MenuCategoryCreate): Observable<MenuCategory> {
    return this.http.post<MenuCategory>(`${this.apiUrl}/categories`, category);
  }
  
  updateCategory(id: number, category: Partial<MenuCategoryCreate>): Observable<MenuCategory> {
    return this.http.put<MenuCategory>(`${this.apiUrl}/categories/${id}`, category);
  }
  
  deleteCategory(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/categories/${id}`);
  }
  
  // Menu Items
  getMenuItems(categoryId?: number, availableOnly?: boolean): Observable<MenuItem[]> {
    let url = `${this.apiUrl}/items`;
    const params: string[] = [];
    
    if (categoryId) params.push(`category_id=${categoryId}`);
    if (availableOnly) params.push(`available_only=true`);
    
    if (params.length > 0) {
      url += `?${params.join('&')}`;
    }
    
    return this.http.get<MenuItem[]>(url);
  }
  
  getFeaturedMenuItems(): Observable<MenuItem[]> {
    return this.http.get<MenuItem[]>(`${this.apiUrl}/items/featured`);
  }
  
  getMenuItem(id: number): Observable<MenuItem> {
    return this.http.get<MenuItem>(`${this.apiUrl}/items/${id}`);
  }
  
  createMenuItem(item: MenuItemCreate): Observable<MenuItem> {
    return this.http.post<MenuItem>(`${this.apiUrl}/items`, item);
  }
  
  updateMenuItem(id: number, item: Partial<MenuItemCreate>): Observable<MenuItem> {
    return this.http.put<MenuItem>(`${this.apiUrl}/items/${id}`, item);
  }
  
  deleteMenuItem(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/items/${id}`);
  }
}

