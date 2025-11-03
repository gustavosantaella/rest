import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User } from '../models/user.model';
import { environment } from '../../../environments/environment';

export interface ProfileUpdate {
  email?: string;
  full_name?: string;
  dni?: string;
  country?: string;
}

export interface PasswordChange {
  current_password: string;
  new_password: string;
}

export interface DeleteAccountResponse {
  message: string;
  warning: string;
}

@Injectable({
  providedIn: 'root'
})
export class ProfileService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/profile`;
  
  getMyProfile(): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/me`);
  }
  
  updateMyProfile(profile: ProfileUpdate): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}/me`, profile);
  }
  
  changePassword(passwords: PasswordChange): Observable<{message: string}> {
    return this.http.post<{message: string}>(`${this.apiUrl}/change-password`, passwords);
  }
  
  deleteAccountPermanently(password: string): Observable<DeleteAccountResponse> {
    return this.http.delete<DeleteAccountResponse>(
      `${this.apiUrl}/delete-account-permanently`,
      { params: { password_confirmation: password } }
    );
  }
}

