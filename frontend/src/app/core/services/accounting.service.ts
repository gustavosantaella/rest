import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  ChartOfAccounts,
  ChartOfAccountsCreate,
  JournalEntry,
  JournalEntryCreate,
  AccountingPeriod,
  AccountingPeriodCreate,
  CostCenter,
  CostCenterCreate,
  GeneralLedger,
  TrialBalance,
  BalanceSheet,
  IncomeStatement
} from '../models/accounting.model';

@Injectable({
  providedIn: 'root'
})
export class AccountingService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/accounting`;

  // Plan de Cuentas
  getChartOfAccounts(activeOnly: boolean = true): Observable<ChartOfAccounts[]> {
    const params = new HttpParams().set('active_only', activeOnly.toString());
    return this.http.get<ChartOfAccounts[]>(`${this.apiUrl}/chart-of-accounts`, { params });
  }

  getAccount(accountId: number): Observable<ChartOfAccounts> {
    return this.http.get<ChartOfAccounts>(`${this.apiUrl}/chart-of-accounts/${accountId}`);
  }

  createAccount(account: ChartOfAccountsCreate): Observable<ChartOfAccounts> {
    return this.http.post<ChartOfAccounts>(`${this.apiUrl}/chart-of-accounts`, account);
  }

  updateAccount(accountId: number, account: Partial<ChartOfAccountsCreate>): Observable<ChartOfAccounts> {
    return this.http.put<ChartOfAccounts>(`${this.apiUrl}/chart-of-accounts/${accountId}`, account);
  }

  deleteAccount(accountId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/chart-of-accounts/${accountId}`);
  }

  // Asientos Contables
  getJournalEntries(
    skip: number = 0,
    limit: number = 100,
    periodId?: number,
    status?: string
  ): Observable<JournalEntry[]> {
    let params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    
    if (periodId) {
      params = params.set('period_id', periodId.toString());
    }
    if (status) {
      params = params.set('status', status);
    }
    
    return this.http.get<JournalEntry[]>(`${this.apiUrl}/journal-entries`, { params });
  }

  getJournalEntry(entryId: number): Observable<JournalEntry> {
    return this.http.get<JournalEntry>(`${this.apiUrl}/journal-entries/${entryId}`);
  }

  createJournalEntry(entry: JournalEntryCreate): Observable<JournalEntry> {
    return this.http.post<JournalEntry>(`${this.apiUrl}/journal-entries`, entry);
  }

  updateJournalEntry(entryId: number, entry: Partial<JournalEntryCreate> | JournalEntryCreate): Observable<JournalEntry> {
    return this.http.put<JournalEntry>(`${this.apiUrl}/journal-entries/${entryId}`, entry);
  }

  postJournalEntry(entryId: number): Observable<JournalEntry> {
    return this.http.post<JournalEntry>(`${this.apiUrl}/journal-entries/${entryId}/post`, {});
  }

  deleteJournalEntry(entryId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/journal-entries/${entryId}`);
  }

  // Períodos Contables
  getPeriods(): Observable<AccountingPeriod[]> {
    return this.http.get<AccountingPeriod[]>(`${this.apiUrl}/periods`);
  }

  getPeriod(periodId: number): Observable<AccountingPeriod> {
    return this.http.get<AccountingPeriod>(`${this.apiUrl}/periods/${periodId}`);
  }

  createPeriod(period: AccountingPeriodCreate): Observable<AccountingPeriod> {
    return this.http.post<AccountingPeriod>(`${this.apiUrl}/periods`, period);
  }

  updatePeriod(periodId: number, period: Partial<AccountingPeriodCreate>): Observable<AccountingPeriod> {
    return this.http.put<AccountingPeriod>(`${this.apiUrl}/periods/${periodId}`, period);
  }

  closePeriod(periodId: number): Observable<AccountingPeriod> {
    return this.http.post<AccountingPeriod>(`${this.apiUrl}/periods/${periodId}/close`, {});
  }

  // Centros de Costo
  getCostCenters(activeOnly: boolean = true): Observable<CostCenter[]> {
    const params = new HttpParams().set('active_only', activeOnly.toString());
    return this.http.get<CostCenter[]>(`${this.apiUrl}/cost-centers`, { params });
  }

  createCostCenter(center: CostCenterCreate): Observable<CostCenter> {
    return this.http.post<CostCenter>(`${this.apiUrl}/cost-centers`, center);
  }

  // Libro Mayor
  getGeneralLedger(
    accountId: number,
    startDate?: string,
    endDate?: string,
    periodId?: number
  ): Observable<GeneralLedger[]> {
    let params = new HttpParams();
    if (startDate) {
      params = params.set('start_date', startDate);
    }
    if (endDate) {
      params = params.set('end_date', endDate);
    }
    if (periodId) {
      params = params.set('period_id', periodId.toString());
    }
    
    return this.http.get<GeneralLedger[]>(`${this.apiUrl}/general-ledger/${accountId}`, { params });
  }

  // Balance de Comprobación
  getTrialBalance(
    periodId?: number,
    startDate?: string,
    endDate?: string
  ): Observable<TrialBalance[]> {
    let params = new HttpParams();
    if (periodId) {
      params = params.set('period_id', periodId.toString());
    }
    if (startDate) {
      params = params.set('start_date', startDate);
    }
    if (endDate) {
      params = params.set('end_date', endDate);
    }
    
    return this.http.get<TrialBalance[]>(`${this.apiUrl}/trial-balance`, { params });
  }

  // Estados Financieros
  getBalanceSheet(asOfDate: string): Observable<BalanceSheet> {
    const params = new HttpParams().set('as_of_date', asOfDate);
    return this.http.get<BalanceSheet>(`${this.apiUrl}/balance-sheet`, { params });
  }

  getIncomeStatement(startDate: string, endDate: string): Observable<IncomeStatement> {
    const params = new HttpParams()
      .set('start_date', startDate)
      .set('end_date', endDate);
    return this.http.get<IncomeStatement>(`${this.apiUrl}/income-statement`, { params });
  }
}

