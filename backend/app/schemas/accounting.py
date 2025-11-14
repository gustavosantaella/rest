"""
Schemas Pydantic para el módulo contable
"""
from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# Enums
class AccountType(str):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"
    COST_OF_SALES = "cost_of_sales"


class AccountNature(str):
    DEBIT = "debit"
    CREDIT = "credit"


class JournalEntryStatus(str):
    DRAFT = "draft"
    POSTED = "posted"
    REVERSED = "reversed"


# Plan de Cuentas
class ChartOfAccountsBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    account_type: str
    nature: str
    parent_id: Optional[int] = None
    level: int = 1
    allows_manual_entries: bool = True
    is_active: bool = True
    initial_balance: Optional[Decimal] = 0
    initial_balance_date: Optional[datetime] = None


class ChartOfAccountsCreate(ChartOfAccountsBase):
    pass


class ChartOfAccountsUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    account_type: Optional[str] = None
    nature: Optional[str] = None
    parent_id: Optional[int] = None
    level: Optional[int] = None
    allows_manual_entries: Optional[bool] = None
    is_active: Optional[bool] = None
    initial_balance: Optional[Decimal] = None
    initial_balance_date: Optional[datetime] = None


class ChartOfAccountsResponse(ChartOfAccountsBase):
    id: int
    business_id: int
    is_system: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    children: List['ChartOfAccountsResponse'] = []
    
    class Config:
        from_attributes = True


# Asientos Contables
class JournalEntryLineBase(BaseModel):
    account_id: int
    debit: Decimal = 0
    credit: Decimal = 0
    description: Optional[str] = None
    reference: Optional[str] = None
    cost_center_id: Optional[int] = None
    
    @field_validator('debit', 'credit')
    def validate_amounts(cls, v):
        if v < 0:
            raise ValueError('Los montos no pueden ser negativos')
        return v


class JournalEntryLineCreate(JournalEntryLineBase):
    pass


class JournalEntryLineResponse(JournalEntryLineBase):
    id: int
    entry_id: int
    created_at: datetime
    account_code: Optional[str] = None
    account_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class JournalEntryBase(BaseModel):
    entry_date: datetime
    reference: Optional[str] = None
    description: str
    period_id: Optional[int] = None
    lines: List[JournalEntryLineCreate]


class JournalEntryCreate(JournalEntryBase):
    pass


class JournalEntryUpdate(BaseModel):
    entry_date: Optional[datetime] = None
    reference: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    period_id: Optional[int] = None
    lines: Optional[List[JournalEntryLineCreate]] = None


class JournalEntryResponse(JournalEntryBase):
    id: int
    business_id: int
    entry_number: str
    status: str
    posted_at: Optional[datetime] = None
    posted_by: Optional[int] = None
    reversed_entry_id: Optional[int] = None
    is_reversal: bool
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    lines: List[JournalEntryLineResponse] = []
    total_debit: Decimal = 0
    total_credit: Decimal = 0
    
    class Config:
        from_attributes = True


# Períodos Contables
class AccountingPeriodBase(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime


class AccountingPeriodCreate(AccountingPeriodBase):
    pass


class AccountingPeriodUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_closed: Optional[bool] = None


class AccountingPeriodResponse(AccountingPeriodBase):
    id: int
    business_id: int
    is_closed: bool
    closed_at: Optional[datetime] = None
    closed_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Centros de Costo
class CostCenterBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: bool = True


class CostCenterCreate(CostCenterBase):
    pass


class CostCenterUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None


class CostCenterResponse(CostCenterBase):
    id: int
    business_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    children: List['CostCenterResponse'] = []
    
    class Config:
        from_attributes = True


# Libro Mayor
class GeneralLedgerResponse(BaseModel):
    id: int
    business_id: int
    account_id: int
    account_code: Optional[str] = None
    account_name: Optional[str] = None
    period_id: Optional[int] = None
    entry_date: datetime
    entry_id: int
    entry_number: Optional[str] = None
    debit: Decimal
    credit: Decimal
    balance_debit: Decimal
    balance_credit: Decimal
    description: Optional[str] = None
    reference: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Balance de Comprobación
class TrialBalanceResponse(BaseModel):
    account_id: int
    account_code: str
    account_name: str
    account_type: str
    initial_balance: Decimal
    debit: Decimal
    credit: Decimal
    final_balance_debit: Decimal
    final_balance_credit: Decimal


# Estados Financieros
class FinancialStatementLine(BaseModel):
    account_code: str
    account_name: str
    amount: Decimal
    level: int
    is_total: bool = False


class BalanceSheetResponse(BaseModel):
    assets: List[FinancialStatementLine]
    liabilities: List[FinancialStatementLine]
    equity: List[FinancialStatementLine]
    total_assets: Decimal
    total_liabilities: Decimal
    total_equity: Decimal
    date: datetime


class IncomeStatementResponse(BaseModel):
    revenue: List[FinancialStatementLine]
    cost_of_sales: List[FinancialStatementLine]
    expenses: List[FinancialStatementLine]
    total_revenue: Decimal
    total_cost_of_sales: Decimal
    gross_profit: Decimal
    total_expenses: Decimal
    net_income: Decimal
    period_start: datetime
    period_end: datetime

