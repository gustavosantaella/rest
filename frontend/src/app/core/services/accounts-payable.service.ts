import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { 
  AccountPayable, 
  AccountPayableCreate, 
  AccountPayableUpdate, 
  AccountPaymentCreate,
  AccountPayment,
  AccountsSummary
} from '../models/accounts.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AccountsPayableService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/accounts-payable`;
  
  getAccountsPayable(status?: string): Observable<AccountPayable[]> {
    let params = new HttpParams();
    if (status) {
      params = params.set('status', status);
    }
    return this.http.get<AccountPayable[]>(this.apiUrl, { params });
  }
  
  getAccountPayable(id: number): Observable<AccountPayable> {
    return this.http.get<AccountPayable>(`${this.apiUrl}/${id}`);
  }
  
  createAccountPayable(account: AccountPayableCreate): Observable<AccountPayable> {
    return this.http.post<AccountPayable>(this.apiUrl, account);
  }
  
  updateAccountPayable(id: number, account: AccountPayableUpdate): Observable<AccountPayable> {
    return this.http.put<AccountPayable>(`${this.apiUrl}/${id}`, account);
  }
  
  deleteAccountPayable(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
  
  addPayment(accountId: number, payment: AccountPaymentCreate): Observable<AccountPayment> {
    return this.http.post<AccountPayment>(`${this.apiUrl}/${accountId}/payments`, payment);
  }
  
  getSummary(): Observable<AccountsSummary> {
    return this.http.get<AccountsSummary>(`${this.apiUrl}/summary/stats`);
  }
}

