"""
Repositorio de contabilidad - Operaciones de base de datos
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from ...models.accounting import (
    ChartOfAccounts, JournalEntry, JournalEntryLine,
    AccountingPeriod, CostCenter, GeneralLedger,
    AccountType, JournalEntryStatus
)


class ChartOfAccountsRepository:
    """Repositorio para Plan de Cuentas"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self, business_id: int, active_only: bool = True) -> List[ChartOfAccounts]:
        """Obtener todas las cuentas"""
        query = self.db.query(ChartOfAccounts).filter(
            ChartOfAccounts.business_id == business_id,
            ChartOfAccounts.deleted_at.is_(None)
        )
        if active_only:
            query = query.filter(ChartOfAccounts.is_active == True)
        return query.order_by(ChartOfAccounts.code).all()
    
    def find_by_id(self, account_id: int, business_id: int) -> Optional[ChartOfAccounts]:
        """Buscar cuenta por ID"""
        return self.db.query(ChartOfAccounts).filter(
            ChartOfAccounts.id == account_id,
            ChartOfAccounts.business_id == business_id,
            ChartOfAccounts.deleted_at.is_(None)
        ).first()
    
    def find_by_code(self, code: str, business_id: int) -> Optional[ChartOfAccounts]:
        """Buscar cuenta por código"""
        return self.db.query(ChartOfAccounts).filter(
            ChartOfAccounts.code == code,
            ChartOfAccounts.business_id == business_id,
            ChartOfAccounts.deleted_at.is_(None)
        ).first()
    
    def create(self, account_data: dict) -> ChartOfAccounts:
        """Crear nueva cuenta"""
        account = ChartOfAccounts(**account_data)
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account
    
    def update(self, account: ChartOfAccounts, update_data: dict) -> ChartOfAccounts:
        """Actualizar cuenta"""
        for field, value in update_data.items():
            setattr(account, field, value)
        self.db.commit()
        self.db.refresh(account)
        return account
    
    def soft_delete(self, account: ChartOfAccounts) -> None:
        """Eliminar cuenta (soft delete)"""
        account.deleted_at = datetime.now()
        account.is_active = False
        self.db.commit()


class JournalEntryRepository:
    """Repositorio para Asientos Contables"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self, business_id: int, skip: int = 0, limit: int = 100) -> List[JournalEntry]:
        """Obtener todos los asientos"""
        return self.db.query(JournalEntry).filter(
            JournalEntry.business_id == business_id,
            JournalEntry.deleted_at.is_(None)
        ).order_by(JournalEntry.entry_date.desc(), JournalEntry.id.desc()).offset(skip).limit(limit).all()
    
    def find_by_id(self, entry_id: int, business_id: int) -> Optional[JournalEntry]:
        """Buscar asiento por ID"""
        return self.db.query(JournalEntry).filter(
            JournalEntry.id == entry_id,
            JournalEntry.business_id == business_id,
            JournalEntry.deleted_at.is_(None)
        ).first()
    
    def find_by_period(self, period_id: int, business_id: int) -> List[JournalEntry]:
        """Buscar asientos por período"""
        return self.db.query(JournalEntry).filter(
            JournalEntry.period_id == period_id,
            JournalEntry.business_id == business_id,
            JournalEntry.deleted_at.is_(None)
        ).order_by(JournalEntry.entry_date).all()
    
    def generate_entry_number(self, business_id: int) -> str:
        """Generar número de asiento único"""
        year = datetime.now().year
        last_entry = self.db.query(JournalEntry).filter(
            JournalEntry.business_id == business_id,
            JournalEntry.entry_number.like(f"AS-{year}-%")
        ).order_by(JournalEntry.id.desc()).first()
        
        if last_entry:
            last_number = int(last_entry.entry_number.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f"AS-{year}-{new_number:06d}"
    
    def create(self, entry_data: dict) -> JournalEntry:
        """Crear nuevo asiento"""
        entry = JournalEntry(**entry_data)
        self.db.add(entry)
        self.db.flush()
        return entry
    
    def create_line(self, line_data: dict) -> JournalEntryLine:
        """Crear línea de asiento"""
        line = JournalEntryLine(**line_data)
        self.db.add(line)
        self.db.flush()
        return line
    
    def update(self, entry: JournalEntry, update_data: dict) -> JournalEntry:
        """Actualizar asiento"""
        for field, value in update_data.items():
            setattr(entry, field, value)
        self.db.commit()
        self.db.refresh(entry)
        return entry
    
    def delete_lines(self, entry_id: int) -> None:
        """Eliminar todas las líneas de un asiento"""
        self.db.query(JournalEntryLine).filter(
            JournalEntryLine.entry_id == entry_id
        ).delete()
        self.db.flush()
    
    def post_entry(self, entry: JournalEntry, user_id: int) -> None:
        """Contabilizar un asiento"""
        entry.status = "posted"
        entry.posted_at = datetime.now()
        entry.posted_by = user_id
        self.db.commit()
        self.db.refresh(entry)
    
    def soft_delete(self, entry: JournalEntry) -> None:
        """Eliminar asiento (soft delete)"""
        entry.deleted_at = datetime.now()
        self.db.commit()


class AccountingPeriodRepository:
    """Repositorio para Períodos Contables"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self, business_id: int) -> List[AccountingPeriod]:
        """Obtener todos los períodos"""
        return self.db.query(AccountingPeriod).filter(
            AccountingPeriod.business_id == business_id
        ).order_by(AccountingPeriod.start_date.desc()).all()
    
    def find_by_id(self, period_id: int, business_id: int) -> Optional[AccountingPeriod]:
        """Buscar período por ID"""
        return self.db.query(AccountingPeriod).filter(
            AccountingPeriod.id == period_id,
            AccountingPeriod.business_id == business_id
        ).first()
    
    def find_current(self, business_id: int) -> Optional[AccountingPeriod]:
        """Buscar período contable actual (abierto)"""
        from datetime import datetime
        now = datetime.now()
        return self.db.query(AccountingPeriod).filter(
            AccountingPeriod.business_id == business_id,
            AccountingPeriod.start_date <= now,
            AccountingPeriod.end_date >= now,
            AccountingPeriod.is_closed == False
        ).first()
    
    def create(self, period_data: dict) -> AccountingPeriod:
        """Crear nuevo período"""
        period = AccountingPeriod(**period_data)
        self.db.add(period)
        self.db.commit()
        self.db.refresh(period)
        return period
    
    def update(self, period: AccountingPeriod, update_data: dict) -> AccountingPeriod:
        """Actualizar período"""
        for field, value in update_data.items():
            setattr(period, field, value)
        self.db.commit()
        self.db.refresh(period)
        return period
    
    def close_period(self, period: AccountingPeriod, user_id: int) -> None:
        """Cerrar período contable"""
        period.is_closed = True
        period.closed_at = datetime.now()
        period.closed_by = user_id
        self.db.commit()
        self.db.refresh(period)


class CostCenterRepository:
    """Repositorio para Centros de Costo"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self, business_id: int, active_only: bool = True) -> List[CostCenter]:
        """Obtener todos los centros de costo"""
        query = self.db.query(CostCenter).filter(
            CostCenter.business_id == business_id,
            CostCenter.deleted_at.is_(None)
        )
        if active_only:
            query = query.filter(CostCenter.is_active == True)
        return query.order_by(CostCenter.code).all()
    
    def find_by_id(self, center_id: int, business_id: int) -> Optional[CostCenter]:
        """Buscar centro de costo por ID"""
        return self.db.query(CostCenter).filter(
            CostCenter.id == center_id,
            CostCenter.business_id == business_id,
            CostCenter.deleted_at.is_(None)
        ).first()
    
    def create(self, center_data: dict) -> CostCenter:
        """Crear nuevo centro de costo"""
        center = CostCenter(**center_data)
        self.db.add(center)
        self.db.commit()
        self.db.refresh(center)
        return center
    
    def update(self, center: CostCenter, update_data: dict) -> CostCenter:
        """Actualizar centro de costo"""
        for field, value in update_data.items():
            setattr(center, field, value)
        self.db.commit()
        self.db.refresh(center)
        return center
    
    def soft_delete(self, center: CostCenter) -> None:
        """Eliminar centro de costo (soft delete)"""
        center.deleted_at = datetime.now()
        center.is_active = False
        self.db.commit()


class GeneralLedgerRepository:
    """Repositorio para Libro Mayor"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_account(
        self,
        account_id: int,
        business_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        period_id: Optional[int] = None
    ) -> List[GeneralLedger]:
        """Obtener movimientos de una cuenta"""
        query = self.db.query(GeneralLedger).filter(
            GeneralLedger.account_id == account_id,
            GeneralLedger.business_id == business_id
        )
        
        if start_date:
            query = query.filter(GeneralLedger.entry_date >= start_date)
        if end_date:
            query = query.filter(GeneralLedger.entry_date <= end_date)
        if period_id:
            query = query.filter(GeneralLedger.period_id == period_id)
        
        return query.order_by(GeneralLedger.entry_date, GeneralLedger.id).all()
    
    def create_ledger_entry(self, entry_data: dict) -> GeneralLedger:
        """Crear entrada en libro mayor"""
        entry = GeneralLedger(**entry_data)
        self.db.add(entry)
        self.db.flush()
        return entry
    
    def rebuild_ledger(self, business_id: int, period_id: Optional[int] = None) -> None:
        """Reconstruir libro mayor desde asientos contabilizados"""
        # Eliminar entradas existentes del período
        query = self.db.query(GeneralLedger).filter(
            GeneralLedger.business_id == business_id
        )
        if period_id:
            query = query.filter(GeneralLedger.period_id == period_id)
        query.delete()
        
        # Obtener asientos contabilizados
        entries_query = self.db.query(JournalEntry).filter(
            JournalEntry.business_id == business_id,
            JournalEntry.status == "posted",
            JournalEntry.deleted_at.is_(None)
        )
        if period_id:
            entries_query = entries_query.filter(JournalEntry.period_id == period_id)
        
        entries = entries_query.order_by(JournalEntry.entry_date, JournalEntry.id).all()
        
        # Reconstruir libro mayor
        account_balances = {}  # {account_id: {'debit': 0, 'credit': 0}}
        
        for entry in entries:
            for line in entry.lines:
                account_id = line.account_id
                
                if account_id not in account_balances:
                    account_balances[account_id] = {'debit': Decimal('0'), 'credit': Decimal('0')}
                
                # Actualizar saldos
                account_balances[account_id]['debit'] += line.debit
                account_balances[account_id]['credit'] += line.credit
                
                # Crear entrada en libro mayor
                ledger_entry = GeneralLedger(
                    business_id=business_id,
                    account_id=account_id,
                    period_id=entry.period_id,
                    entry_date=entry.entry_date,
                    entry_id=entry.id,
                    entry_line_id=line.id,
                    debit=line.debit,
                    credit=line.credit,
                    balance_debit=account_balances[account_id]['debit'],
                    balance_credit=account_balances[account_id]['credit'],
                    description=line.description or entry.description,
                    reference=line.reference or entry.reference
                )
                self.db.add(ledger_entry)
        
        self.db.commit()

