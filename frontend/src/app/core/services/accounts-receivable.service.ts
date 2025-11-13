import { Injectable, inject } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Observable } from "rxjs";
import {
  AccountReceivable,
  AccountReceivableCreate,
  AccountReceivableUpdate,
  AccountPaymentCreate,
  AccountPayment,
  AccountsSummary,
} from "../models/accounts.model";
import { environment } from "../../../environments/environment";

@Injectable({
  providedIn: "root",
})
export class AccountsReceivableService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/accounts-receivable`;

  getAccountsReceivable(status?: string): Observable<AccountReceivable[]> {
    let params = new HttpParams();
    if (status) {
      params = params.set("status", status);
    }
    return this.http.get<AccountReceivable[]>(this.apiUrl, { params });
  }

  getAccountReceivable(id: number): Observable<AccountReceivable> {
    return this.http.get<AccountReceivable>(`${this.apiUrl}/${id}`);
  }

  createAccountReceivable(
    account: AccountReceivableCreate
  ): Observable<AccountReceivable> {
    return this.http.post<AccountReceivable>(this.apiUrl, account);
  }

  updateAccountReceivable(
    id: number,
    account: AccountReceivableUpdate
  ): Observable<AccountReceivable> {
    return this.http.put<AccountReceivable>(`${this.apiUrl}/${id}`, account);
  }

  deleteAccountReceivable(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  addPayment(
    accountId: number,
    payment: AccountPaymentCreate
  ): Observable<AccountPayment> {
    return this.http.post<AccountPayment>(
      `${this.apiUrl}/${accountId}/payments`,
      payment
    );
  }

  getSummary(): Observable<AccountsSummary> {
    return this.http.get<AccountsSummary>(`${this.apiUrl}/summary`);
  }
}
