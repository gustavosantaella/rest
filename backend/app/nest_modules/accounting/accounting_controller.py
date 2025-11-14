"""
Controlador de contabilidad usando PyNest
"""
from nest.core import Controller, Get, Post, Put, Delete, Depends
from fastapi import status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .accounting_service import AccountingService
from ...core.database import get_db
from ...models.user import User
from ...schemas.accounting import (
    ChartOfAccountsCreate, ChartOfAccountsUpdate, ChartOfAccountsResponse,
    JournalEntryCreate, JournalEntryUpdate, JournalEntryResponse,
    AccountingPeriodCreate, AccountingPeriodUpdate, AccountingPeriodResponse,
    CostCenterCreate, CostCenterUpdate, CostCenterResponse,
    GeneralLedgerResponse, TrialBalanceResponse,
    BalanceSheetResponse, IncomeStatementResponse
)
from ...utils.dependencies import get_current_user, get_current_active_admin


@Controller("api/accounting")
class AccountingController:
    """Controlador para rutas de contabilidad"""
    
    def __init__(self, service: AccountingService):
        self.service = service
    
    # ========== Plan de Cuentas ==========
    
    @Get("/chart-of-accounts")
    def get_chart_of_accounts(
        self,
        active_only: bool = Query(True),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[ChartOfAccountsResponse]:
        """Obtener plan de cuentas"""
        return self.service.get_chart_of_accounts(
            current_user.business_id,
            db,
            active_only
        )
    
    @Get("/chart-of-accounts/{account_id}")
    def get_account(
        self,
        account_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> ChartOfAccountsResponse:
        """Obtener cuenta por ID"""
        return self.service.get_account(account_id, current_user.business_id, db)
    
    @Post("/chart-of-accounts", status_code=status.HTTP_201_CREATED)
    def create_account(
        self,
        account: ChartOfAccountsCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> ChartOfAccountsResponse:
        """Crear nueva cuenta"""
        return self.service.create_account(account, current_user.business_id, db)
    
    @Put("/chart-of-accounts/{account_id}")
    def update_account(
        self,
        account_id: int,
        account_update: ChartOfAccountsUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> ChartOfAccountsResponse:
        """Actualizar cuenta"""
        return self.service.update_account(
            account_id,
            account_update,
            current_user.business_id,
            db
        )
    
    @Delete("/chart-of-accounts/{account_id}", status_code=status.HTTP_200_OK)
    def delete_account(
        self,
        account_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> dict:
        """Eliminar cuenta"""
        return self.service.delete_account(account_id, current_user.business_id, db)
    
    # ========== Asientos Contables ==========
    
    @Get("/journal-entries")
    def get_journal_entries(
        self,
        skip: int = Query(0),
        limit: int = Query(100),
        period_id: Optional[int] = Query(None),
        status: Optional[str] = Query(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[JournalEntryResponse]:
        """Obtener asientos contables"""
        return self.service.get_journal_entries(
            current_user.business_id,
            skip,
            limit,
            db,
            period_id,
            status
        )
    
    @Get("/journal-entries/{entry_id}")
    def get_journal_entry(
        self,
        entry_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> JournalEntryResponse:
        """Obtener asiento por ID"""
        return self.service.get_journal_entry(entry_id, current_user.business_id, db)
    
    @Post("/journal-entries", status_code=status.HTTP_201_CREATED)
    def create_journal_entry(
        self,
        entry: JournalEntryCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> JournalEntryResponse:
        """Crear nuevo asiento contable"""
        return self.service.create_journal_entry(
            entry,
            current_user.business_id,
            current_user.id,
            db
        )
    
    @Put("/journal-entries/{entry_id}")
    def update_journal_entry(
        self,
        entry_id: int,
        entry_update: JournalEntryUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> JournalEntryResponse:
        """Actualizar asiento contable"""
        return self.service.update_journal_entry(
            entry_id,
            entry_update,
            current_user.business_id,
            db
        )
    
    @Post("/journal-entries/{entry_id}/post", status_code=status.HTTP_200_OK)
    def post_journal_entry(
        self,
        entry_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> JournalEntryResponse:
        """Contabilizar un asiento"""
        return self.service.post_journal_entry(
            entry_id,
            current_user.business_id,
            current_user.id,
            db
        )
    
    @Delete("/journal-entries/{entry_id}", status_code=status.HTTP_200_OK)
    def delete_journal_entry(
        self,
        entry_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> dict:
        """Eliminar asiento"""
        return self.service.delete_journal_entry(entry_id, current_user.business_id, db)
    
    # ========== Períodos Contables ==========
    
    @Get("/periods")
    def get_periods(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[AccountingPeriodResponse]:
        """Obtener períodos contables"""
        return self.service.get_periods(current_user.business_id, db)
    
    @Get("/periods/{period_id}")
    def get_period(
        self,
        period_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> AccountingPeriodResponse:
        """Obtener período por ID"""
        return self.service.get_period(period_id, current_user.business_id, db)
    
    @Post("/periods", status_code=status.HTTP_201_CREATED)
    def create_period(
        self,
        period: AccountingPeriodCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> AccountingPeriodResponse:
        """Crear nuevo período contable"""
        return self.service.create_period(period, current_user.business_id, db)
    
    @Put("/periods/{period_id}")
    def update_period(
        self,
        period_id: int,
        period_update: AccountingPeriodUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> AccountingPeriodResponse:
        """Actualizar período contable"""
        return self.service.update_period(
            period_id,
            period_update,
            current_user.business_id,
            db
        )
    
    @Post("/periods/{period_id}/close", status_code=status.HTTP_200_OK)
    def close_period(
        self,
        period_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> AccountingPeriodResponse:
        """Cerrar período contable"""
        return self.service.close_period(
            period_id,
            current_user.business_id,
            current_user.id,
            db
        )
    
    # ========== Centros de Costo ==========
    
    @Get("/cost-centers")
    def get_cost_centers(
        self,
        active_only: bool = Query(True),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[CostCenterResponse]:
        """Obtener centros de costo"""
        return self.service.get_cost_centers(
            current_user.business_id,
            db,
            active_only
        )
    
    @Post("/cost-centers", status_code=status.HTTP_201_CREATED)
    def create_cost_center(
        self,
        center: CostCenterCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> CostCenterResponse:
        """Crear centro de costo"""
        return self.service.create_cost_center(center, current_user.business_id, db)
    
    # ========== Libro Mayor ==========
    
    @Get("/general-ledger/{account_id}")
    def get_general_ledger(
        self,
        account_id: int,
        start_date: Optional[datetime] = Query(None),
        end_date: Optional[datetime] = Query(None),
        period_id: Optional[int] = Query(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[GeneralLedgerResponse]:
        """Obtener libro mayor de una cuenta"""
        return self.service.get_general_ledger(
            account_id,
            current_user.business_id,
            db,
            start_date,
            end_date,
            period_id
        )
    
    # ========== Balance de Comprobación ==========
    
    @Get("/trial-balance")
    def get_trial_balance(
        self,
        period_id: Optional[int] = Query(None),
        start_date: Optional[datetime] = Query(None),
        end_date: Optional[datetime] = Query(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[TrialBalanceResponse]:
        """Obtener balance de comprobación"""
        return self.service.get_trial_balance(
            current_user.business_id,
            db,
            period_id,
            start_date,
            end_date
        )
    
    # ========== Estados Financieros ==========
    
    @Get("/balance-sheet")
    def get_balance_sheet(
        self,
        as_of_date: datetime = Query(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> BalanceSheetResponse:
        """Obtener Balance General"""
        return self.service.get_balance_sheet(
            current_user.business_id,
            db,
            as_of_date
        )
    
    @Get("/income-statement")
    def get_income_statement(
        self,
        start_date: datetime = Query(...),
        end_date: datetime = Query(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> IncomeStatementResponse:
        """Obtener Estado de Resultados"""
        return self.service.get_income_statement(
            current_user.business_id,
            db,
            start_date,
            end_date
        )

