"""
Servicio de contabilidad usando PyNest - Lógica de negocio
"""

from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException, status
from .accounting_repository import (
    ChartOfAccountsRepository,
    JournalEntryRepository,
    AccountingPeriodRepository,
    CostCenterRepository,
    GeneralLedgerRepository,
)
from ...schemas.accounting import (
    ChartOfAccountsCreate,
    ChartOfAccountsUpdate,
    ChartOfAccountsResponse,
    JournalEntryCreate,
    JournalEntryUpdate,
    JournalEntryResponse,
    JournalEntryLineCreate,
    JournalEntryLineResponse,
    AccountingPeriodCreate,
    AccountingPeriodUpdate,
    AccountingPeriodResponse,
    CostCenterCreate,
    CostCenterUpdate,
    CostCenterResponse,
    GeneralLedgerResponse,
    TrialBalanceResponse,
    BalanceSheetResponse,
    IncomeStatementResponse,
    FinancialStatementLine,
)
from ...models.accounting import AccountType, JournalEntryStatus


@Injectable
class AccountingService:
    """Servicio para lógica de negocio contable"""

    def __init__(self):
        pass

    # ========== Plan de Cuentas ==========

    def get_chart_of_accounts(
        self, business_id: int, db: Session, active_only: bool = True
    ) -> List[ChartOfAccountsResponse]:
        """Obtener plan de cuentas"""
        repo = ChartOfAccountsRepository(db)
        accounts = repo.find_all(business_id, active_only)
        return [
            ChartOfAccountsResponse.model_validate(acc, from_attributes=True)
            for acc in accounts
        ]

    def get_account(
        self, account_id: int, business_id: int, db: Session
    ) -> ChartOfAccountsResponse:
        """Obtener cuenta por ID"""
        repo = ChartOfAccountsRepository(db)
        account = repo.find_by_id(account_id, business_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada"
            )
        return ChartOfAccountsResponse.model_validate(account, from_attributes=True)

    def create_account(
        self, account_data: ChartOfAccountsCreate, business_id: int, db: Session
    ) -> ChartOfAccountsResponse:
        """Crear nueva cuenta"""
        repo = ChartOfAccountsRepository(db)

        # Verificar que el código no exista
        existing = repo.find_by_code(account_data.code, business_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una cuenta con este código",
            )

        account_dict = account_data.model_dump()
        account_dict["business_id"] = business_id
        account = repo.create(account_dict)
        return ChartOfAccountsResponse.model_validate(account, from_attributes=True)

    def update_account(
        self,
        account_id: int,
        account_update: ChartOfAccountsUpdate,
        business_id: int,
        db: Session,
    ) -> ChartOfAccountsResponse:
        """Actualizar cuenta"""
        repo = ChartOfAccountsRepository(db)
        account = repo.find_by_id(account_id, business_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada"
            )

        if account.is_system:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede modificar una cuenta del sistema",
            )

        # Verificar código único si se actualiza
        if account_update.code and account_update.code != account.code:
            existing = repo.find_by_code(account_update.code, business_id)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe una cuenta con este código",
                )

        update_data = account_update.model_dump(exclude_unset=True)
        account = repo.update(account, update_data)
        return ChartOfAccountsResponse.model_validate(account, from_attributes=True)

    def delete_account(self, account_id: int, business_id: int, db: Session) -> dict:
        """Eliminar cuenta"""
        repo = ChartOfAccountsRepository(db)
        account = repo.find_by_id(account_id, business_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada"
            )

        if account.is_system:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar una cuenta del sistema",
            )

        repo.soft_delete(account)
        return {"message": "Cuenta eliminada exitosamente"}

    # ========== Asientos Contables ==========

    def get_journal_entries(
        self,
        business_id: int,
        skip: int,
        limit: int,
        db: Session,
        period_id: Optional[int] = None,
        status: Optional[str] = None,
    ) -> List[JournalEntryResponse]:
        """Obtener asientos contables"""
        repo = JournalEntryRepository(db)
        entries = repo.find_all(business_id, skip, limit)

        # Filtrar por período si se especifica
        if period_id:
            entries = [e for e in entries if e.period_id == period_id]

        # Filtrar por estado si se especifica
        if status:
            entries = [
                e
                for e in entries
                if (e.status if isinstance(e.status, str) else e.status.value) == status
            ]

        result = []
        for entry in entries:
            entry_dict = JournalEntryResponse.model_validate(
                entry, from_attributes=True
            ).model_dump()
            # Calcular totales
            total_debit = sum(line.debit for line in entry.lines)
            total_credit = sum(line.credit for line in entry.lines)
            entry_dict["total_debit"] = total_debit
            entry_dict["total_credit"] = total_credit
            result.append(JournalEntryResponse(**entry_dict))

        return result

    def get_journal_entry(
        self, entry_id: int, business_id: int, db: Session
    ) -> JournalEntryResponse:
        """Obtener asiento por ID"""
        repo = JournalEntryRepository(db)
        entry = repo.find_by_id(entry_id, business_id)
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Asiento no encontrado"
            )

        entry_dict = JournalEntryResponse.model_validate(
            entry, from_attributes=True
        ).model_dump()
        total_debit = sum(line.debit for line in entry.lines)
        total_credit = sum(line.credit for line in entry.lines)
        entry_dict["total_debit"] = total_debit
        entry_dict["total_credit"] = total_credit
        return JournalEntryResponse(**entry_dict)

    def create_journal_entry(
        self,
        entry_data: JournalEntryCreate,
        business_id: int,
        user_id: int,
        db: Session,
    ) -> JournalEntryResponse:
        """Crear nuevo asiento contable"""
        repo = JournalEntryRepository(db)

        # Validar que el asiento esté balanceado
        total_debit = sum(line.debit for line in entry_data.lines)
        total_credit = sum(line.credit for line in entry_data.lines)

        if total_debit != total_credit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El asiento no está balanceado. Débito: {total_debit}, Crédito: {total_credit}",
            )

        if total_debit == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El asiento debe tener al menos un movimiento",
            )

        # Validar que las cuentas existan
        account_repo = ChartOfAccountsRepository(db)
        for line in entry_data.lines:
            account = account_repo.find_by_id(line.account_id, business_id)
            if not account:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Cuenta {line.account_id} no encontrada",
                )
            if not account.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"La cuenta {account.code} no está activa",
                )

        # Generar número de asiento
        entry_number = repo.generate_entry_number(business_id)

        # Crear asiento
        entry_dict = {
            "business_id": business_id,
            "entry_number": entry_number,
            "entry_date": entry_data.entry_date,
            "reference": entry_data.reference,
            "description": entry_data.description,
            "period_id": entry_data.period_id,
            "status": "draft",
            "created_by": user_id,
        }

        entry = repo.create(entry_dict)

        # Crear líneas
        for line_data in entry_data.lines:
            line_dict = line_data.model_dump()
            line_dict["entry_id"] = entry.id
            repo.create_line(line_dict)

        db.commit()
        db.refresh(entry)

        entry_dict = JournalEntryResponse.model_validate(
            entry, from_attributes=True
        ).model_dump()
        entry_dict["total_debit"] = total_debit
        entry_dict["total_credit"] = total_credit
        return JournalEntryResponse(**entry_dict)

    def update_journal_entry(
        self,
        entry_id: int,
        entry_update: JournalEntryUpdate,
        business_id: int,
        db: Session,
    ) -> JournalEntryResponse:
        """Actualizar asiento contable"""
        repo = JournalEntryRepository(db)
        entry = repo.find_by_id(entry_id, business_id)
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Asiento no encontrado"
            )

        entry_status = (
            entry.status if isinstance(entry.status, str) else entry.status.value
        )
        if entry_status == "posted":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede modificar un asiento contabilizado",
            )

        update_data = entry_update.model_dump(exclude_unset=True)

        # Si se actualizan las líneas, validar balance
        if "lines" in update_data:
            total_debit = sum(line.debit for line in update_data["lines"])
            total_credit = sum(line.credit for line in update_data["lines"])

            if total_debit != total_credit:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El asiento no está balanceado. Débito: {total_debit}, Crédito: {total_credit}",
                )

            # Eliminar líneas existentes y crear nuevas
            repo.delete_lines(entry_id)
            for line_data in update_data["lines"]:
                line_dict = line_data.model_dump()
                line_dict["entry_id"] = entry_id
                repo.create_line(line_dict)

            del update_data["lines"]

        if update_data:
            repo.update(entry, update_data)

        db.commit()
        db.refresh(entry)

        entry_dict = JournalEntryResponse.model_validate(
            entry, from_attributes=True
        ).model_dump()
        total_debit = sum(line.debit for line in entry.lines)
        total_credit = sum(line.credit for line in entry.lines)
        entry_dict["total_debit"] = total_debit
        entry_dict["total_credit"] = total_credit
        return JournalEntryResponse(**entry_dict)

    def post_journal_entry(
        self, entry_id: int, business_id: int, user_id: int, db: Session
    ) -> JournalEntryResponse:
        """Contabilizar un asiento"""
        repo = JournalEntryRepository(db)
        ledger_repo = GeneralLedgerRepository(db)

        entry = repo.find_by_id(entry_id, business_id)
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Asiento no encontrado"
            )

        entry_status = (
            entry.status if isinstance(entry.status, str) else entry.status.value
        )
        if entry_status == "posted":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El asiento ya está contabilizado",
            )

        # Contabilizar
        repo.post_entry(entry, user_id)

        # Actualizar libro mayor
        ledger_repo.rebuild_ledger(business_id, entry.period_id)

        entry_dict = JournalEntryResponse.model_validate(
            entry, from_attributes=True
        ).model_dump()
        total_debit = sum(line.debit for line in entry.lines)
        total_credit = sum(line.credit for line in entry.lines)
        entry_dict["total_debit"] = total_debit
        entry_dict["total_credit"] = total_credit
        return JournalEntryResponse(**entry_dict)

    def delete_journal_entry(
        self, entry_id: int, business_id: int, db: Session
    ) -> dict:
        """Eliminar asiento"""
        repo = JournalEntryRepository(db)
        entry = repo.find_by_id(entry_id, business_id)
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Asiento no encontrado"
            )

        entry_status = (
            entry.status if isinstance(entry.status, str) else entry.status.value
        )
        if entry_status == "posted":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar un asiento contabilizado",
            )

        repo.soft_delete(entry)
        return {"message": "Asiento eliminado exitosamente"}

    # ========== Períodos Contables ==========

    def get_periods(
        self, business_id: int, db: Session
    ) -> List[AccountingPeriodResponse]:
        """Obtener períodos contables"""
        repo = AccountingPeriodRepository(db)
        periods = repo.find_all(business_id)
        return [
            AccountingPeriodResponse.model_validate(p, from_attributes=True)
            for p in periods
        ]

    def get_period(
        self, period_id: int, business_id: int, db: Session
    ) -> AccountingPeriodResponse:
        """Obtener período por ID"""
        repo = AccountingPeriodRepository(db)
        period = repo.find_by_id(period_id, business_id)
        if not period:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Período no encontrado"
            )
        return AccountingPeriodResponse.model_validate(period, from_attributes=True)

    def create_period(
        self, period_data: AccountingPeriodCreate, business_id: int, db: Session
    ) -> AccountingPeriodResponse:
        """Crear nuevo período contable"""
        repo = AccountingPeriodRepository(db)

        # Validar que no se solapen períodos
        existing_periods = repo.find_all(business_id)
        for existing in existing_periods:
            if not existing.is_closed:
                if (
                    period_data.start_date <= existing.end_date
                    and period_data.end_date >= existing.start_date
                ):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El período se solapa con un período existente",
                    )

        period_dict = period_data.model_dump()
        period_dict["business_id"] = business_id
        period = repo.create(period_dict)
        return AccountingPeriodResponse.model_validate(period, from_attributes=True)

    def update_period(
        self,
        period_id: int,
        period_update: AccountingPeriodUpdate,
        business_id: int,
        db: Session,
    ) -> AccountingPeriodResponse:
        """Actualizar período contable"""
        repo = AccountingPeriodRepository(db)
        period = repo.find_by_id(period_id, business_id)
        if not period:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Período no encontrado"
            )

        if period.is_closed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede modificar un período cerrado",
            )

        update_data = period_update.model_dump(exclude_unset=True)
        period = repo.update(period, update_data)
        return AccountingPeriodResponse.model_validate(period, from_attributes=True)

    def close_period(
        self, period_id: int, business_id: int, user_id: int, db: Session
    ) -> AccountingPeriodResponse:
        """Cerrar período contable"""
        repo = AccountingPeriodRepository(db)
        period = repo.find_by_id(period_id, business_id)
        if not period:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Período no encontrado"
            )

        if period.is_closed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El período ya está cerrado",
            )

        repo.close_period(period, user_id)
        return AccountingPeriodResponse.model_validate(period, from_attributes=True)

    # ========== Centros de Costo ==========

    def get_cost_centers(
        self, business_id: int, db: Session, active_only: bool = True
    ) -> List[CostCenterResponse]:
        """Obtener centros de costo"""
        repo = CostCenterRepository(db)
        centers = repo.find_all(business_id, active_only)
        return [
            CostCenterResponse.model_validate(c, from_attributes=True) for c in centers
        ]

    def create_cost_center(
        self, center_data: CostCenterCreate, business_id: int, db: Session
    ) -> CostCenterResponse:
        """Crear centro de costo"""
        repo = CostCenterRepository(db)
        center_dict = center_data.model_dump()
        center_dict["business_id"] = business_id
        center = repo.create(center_dict)
        return CostCenterResponse.model_validate(center, from_attributes=True)

    # ========== Libro Mayor ==========

    def get_general_ledger(
        self,
        account_id: int,
        business_id: int,
        db: Session,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        period_id: Optional[int] = None,
    ) -> List[GeneralLedgerResponse]:
        """Obtener libro mayor de una cuenta"""
        repo = GeneralLedgerRepository(db)
        entries = repo.find_by_account(
            account_id, business_id, start_date, end_date, period_id
        )

        result = []
        for entry in entries:
            entry_dict = GeneralLedgerResponse.model_validate(
                entry, from_attributes=True
            ).model_dump()
            # Agregar información de la cuenta
            if entry.account:
                entry_dict["account_code"] = entry.account.code
                entry_dict["account_name"] = entry.account.name
            # Agregar número de asiento
            if entry.entry:
                entry_dict["entry_number"] = entry.entry.entry_number
            result.append(GeneralLedgerResponse(**entry_dict))

        return result

    # ========== Balance de Comprobación ==========

    def get_trial_balance(
        self,
        business_id: int,
        db: Session,
        period_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[TrialBalanceResponse]:
        """Obtener balance de comprobación"""
        account_repo = ChartOfAccountsRepository(db)
        ledger_repo = GeneralLedgerRepository(db)

        accounts = account_repo.find_all(business_id, active_only=True)
        result = []

        for account in accounts:
            # Obtener movimientos del período
            ledger_entries = ledger_repo.find_by_account(
                account.id, business_id, start_date, end_date, period_id
            )

            total_debit = sum(entry.debit for entry in ledger_entries)
            total_credit = sum(entry.credit for entry in ledger_entries)

            # Calcular saldo final según naturaleza
            initial = account.initial_balance or Decimal("0")

            # account.nature es ahora un string, no un Enum
            nature_value = (
                account.nature
                if isinstance(account.nature, str)
                else account.nature.value
            )

            if nature_value == "debit":
                final_balance = initial + total_debit - total_credit
                final_debit = final_balance if final_balance > 0 else Decimal("0")
                final_credit = -final_balance if final_balance < 0 else Decimal("0")
            else:  # credit
                final_balance = initial + total_credit - total_debit
                final_debit = -final_balance if final_balance < 0 else Decimal("0")
                final_credit = final_balance if final_balance > 0 else Decimal("0")

            result.append(
                TrialBalanceResponse(
                    account_id=account.id,
                    account_code=account.code,
                    account_name=account.name,
                    account_type=(
                        account.account_type
                        if isinstance(account.account_type, str)
                        else account.account_type.value
                    ),
                    initial_balance=initial,
                    debit=total_debit,
                    credit=total_credit,
                    final_balance_debit=final_debit,
                    final_balance_credit=final_credit,
                )
            )

        return result

    # ========== Estados Financieros ==========

    def get_balance_sheet(
        self, business_id: int, db: Session, as_of_date: datetime
    ) -> BalanceSheetResponse:
        """Obtener Balance General"""
        trial_balance = self.get_trial_balance(business_id, db, end_date=as_of_date)

        assets = []
        liabilities = []
        equity = []

        total_assets = Decimal("0")
        total_liabilities = Decimal("0")
        total_equity = Decimal("0")

        for item in trial_balance:
            balance = item.final_balance_debit - item.final_balance_credit

            if item.account_type == AccountType.ASSET.value:
                if balance != 0:
                    assets.append(
                        FinancialStatementLine(
                            account_code=item.account_code,
                            account_name=item.account_name,
                            amount=balance,
                            level=1,
                            is_total=False,
                        )
                    )
                    total_assets += balance
            elif item.account_type == AccountType.LIABILITY.value:
                if balance != 0:
                    liabilities.append(
                        FinancialStatementLine(
                            account_code=item.account_code,
                            account_name=item.account_name,
                            amount=balance,
                            level=1,
                            is_total=False,
                        )
                    )
                    total_liabilities += balance
            elif item.account_type == AccountType.EQUITY.value:
                if balance != 0:
                    equity.append(
                        FinancialStatementLine(
                            account_code=item.account_code,
                            account_name=item.account_name,
                            amount=balance,
                            level=1,
                            is_total=False,
                        )
                    )
                    total_equity += balance

        return BalanceSheetResponse(
            assets=assets,
            liabilities=liabilities,
            equity=equity,
            total_assets=total_assets,
            total_liabilities=total_liabilities,
            total_equity=total_equity,
            date=as_of_date,
        )

    def get_income_statement(
        self, business_id: int, db: Session, start_date: datetime, end_date: datetime
    ) -> IncomeStatementResponse:
        """Obtener Estado de Resultados"""
        trial_balance = self.get_trial_balance(
            business_id, db, start_date=start_date, end_date=end_date
        )

        revenue = []
        cost_of_sales = []
        expenses = []

        total_revenue = Decimal("0")
        total_cost_of_sales = Decimal("0")
        total_expenses = Decimal("0")

        for item in trial_balance:
            balance = item.final_balance_debit - item.final_balance_credit

            if item.account_type == AccountType.REVENUE.value:
                if balance != 0:
                    revenue.append(
                        FinancialStatementLine(
                            account_code=item.account_code,
                            account_name=item.account_name,
                            amount=balance,
                            level=1,
                            is_total=False,
                        )
                    )
                    total_revenue += balance
            elif item.account_type == AccountType.COST_OF_SALES.value:
                if balance != 0:
                    cost_of_sales.append(
                        FinancialStatementLine(
                            account_code=item.account_code,
                            account_name=item.account_name,
                            amount=balance,
                            level=1,
                            is_total=False,
                        )
                    )
                    total_cost_of_sales += balance
            elif item.account_type == AccountType.EXPENSE.value:
                if balance != 0:
                    expenses.append(
                        FinancialStatementLine(
                            account_code=item.account_code,
                            account_name=item.account_name,
                            amount=balance,
                            level=1,
                            is_total=False,
                        )
                    )
                    total_expenses += balance

        gross_profit = total_revenue - total_cost_of_sales
        net_income = gross_profit - total_expenses

        return IncomeStatementResponse(
            revenue=revenue,
            cost_of_sales=cost_of_sales,
            expenses=expenses,
            total_revenue=total_revenue,
            total_cost_of_sales=total_cost_of_sales,
            gross_profit=gross_profit,
            total_expenses=total_expenses,
            net_income=net_income,
            period_start=start_date,
            period_end=end_date,
        )
