"""
Modelos contables para el sistema de gestión
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text, Boolean, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base


class AccountType(str, enum.Enum):
    """Tipos de cuentas contables"""
    ASSET = "asset"  # Activo
    LIABILITY = "liability"  # Pasivo
    EQUITY = "equity"  # Patrimonio
    REVENUE = "revenue"  # Ingreso
    EXPENSE = "expense"  # Gasto
    COST_OF_SALES = "cost_of_sales"  # Costo de ventas


class AccountNature(str, enum.Enum):
    """Naturaleza de las cuentas"""
    DEBIT = "debit"  # Deudora
    CREDIT = "credit"  # Acreedora


class JournalEntryStatus(str, enum.Enum):
    """Estado de los asientos contables"""
    DRAFT = "draft"  # Borrador
    POSTED = "posted"  # Contabilizado
    REVERSED = "reversed"  # Revertido


class ChartOfAccounts(Base):
    """Plan de Cuentas Contables"""
    __tablename__ = "chart_of_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_configuration.id", ondelete='CASCADE'), nullable=False, index=True)
    
    # Código y nombre de la cuenta
    code = Column(String, nullable=False, index=True)  # Ej: "1.01.01.001"
    name = Column(String, nullable=False)
    description = Column(Text)
    
    # Clasificación contable
    account_type = Column(Enum(AccountType), nullable=False)
    nature = Column(Enum(AccountNature), nullable=False)  # Deudora o Acreedora
    
    # Estructura jerárquica
    parent_id = Column(Integer, ForeignKey("chart_of_accounts.id"), nullable=True, index=True)
    level = Column(Integer, default=1)  # Nivel en la jerarquía (1, 2, 3, etc.)
    
    # Configuración
    allows_manual_entries = Column(Boolean, default=True)  # Permite asientos manuales
    is_active = Column(Boolean, default=True)
    is_system = Column(Boolean, default=False)  # Cuenta del sistema (no se puede eliminar)
    
    # Saldos iniciales
    initial_balance = Column(Numeric(15, 2), default=0)
    initial_balance_date = Column(DateTime(timezone=True), nullable=True)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relaciones
    business = relationship("BusinessConfiguration", backref="chart_of_accounts")
    parent = relationship("ChartOfAccounts", remote_side=[id], backref="children")
    journal_entries = relationship("JournalEntryLine", back_populates="account")


class JournalEntry(Base):
    """Asientos Contables"""
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_configuration.id", ondelete='CASCADE'), nullable=False, index=True)
    
    # Información del asiento
    entry_number = Column(String, unique=True, nullable=False, index=True)  # Número de asiento único
    entry_date = Column(DateTime(timezone=True), nullable=False, index=True)
    reference = Column(String, index=True)  # Referencia externa (factura, orden, etc.)
    description = Column(Text, nullable=False)
    
    # Estado
    status = Column(Enum(JournalEntryStatus), default=JournalEntryStatus.DRAFT, nullable=False)
    posted_at = Column(DateTime(timezone=True), nullable=True)
    posted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Reversión
    reversed_entry_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=True)
    is_reversal = Column(Boolean, default=False)
    
    # Período contable
    period_id = Column(Integer, ForeignKey("accounting_periods.id"), nullable=True, index=True)
    
    # Auditoría
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relaciones
    business = relationship("BusinessConfiguration", backref="journal_entries")
    lines = relationship("JournalEntryLine", back_populates="entry", cascade="all, delete-orphan")
    period = relationship("AccountingPeriod", back_populates="entries")
    creator = relationship("User", foreign_keys=[created_by], backref="created_journal_entries")
    poster = relationship("User", foreign_keys=[posted_by], backref="posted_journal_entries")
    reversed_entry = relationship("JournalEntry", remote_side=[id], backref="reversals")


class JournalEntryLine(Base):
    """Líneas de Asientos Contables"""
    __tablename__ = "journal_entry_lines"
    
    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("journal_entries.id", ondelete='CASCADE'), nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("chart_of_accounts.id"), nullable=False, index=True)
    
    # Movimientos
    debit = Column(Numeric(15, 2), default=0)  # Débito
    credit = Column(Numeric(15, 2), default=0)  # Crédito
    
    # Información adicional
    description = Column(Text)
    reference = Column(String)  # Referencia adicional
    
    # Centro de costo (opcional)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=True)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    entry = relationship("JournalEntry", back_populates="lines")
    account = relationship("ChartOfAccounts", back_populates="journal_entries")
    cost_center = relationship("CostCenter", back_populates="entry_lines")


class AccountingPeriod(Base):
    """Períodos Contables"""
    __tablename__ = "accounting_periods"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_configuration.id", ondelete='CASCADE'), nullable=False, index=True)
    
    # Información del período
    name = Column(String, nullable=False)  # Ej: "Enero 2024"
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    
    # Estado
    is_closed = Column(Boolean, default=False)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    closed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    business = relationship("BusinessConfiguration", backref="accounting_periods")
    entries = relationship("JournalEntry", back_populates="period")
    closer = relationship("User", foreign_keys=[closed_by], backref="closed_periods")


class CostCenter(Base):
    """Centros de Costo"""
    __tablename__ = "cost_centers"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_configuration.id", ondelete='CASCADE'), nullable=False, index=True)
    
    # Información
    code = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    
    # Estructura jerárquica
    parent_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=True, index=True)
    
    # Configuración
    is_active = Column(Boolean, default=True)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relaciones
    business = relationship("BusinessConfiguration", backref="cost_centers")
    parent = relationship("CostCenter", remote_side=[id], backref="children")
    entry_lines = relationship("JournalEntryLine", back_populates="cost_center")


class GeneralLedger(Base):
    """Libro Mayor - Vista materializada o tabla de resumen"""
    __tablename__ = "general_ledger"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_configuration.id", ondelete='CASCADE'), nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("chart_of_accounts.id"), nullable=False, index=True)
    period_id = Column(Integer, ForeignKey("accounting_periods.id"), nullable=True, index=True)
    
    # Fecha y referencia
    entry_date = Column(DateTime(timezone=True), nullable=False, index=True)
    entry_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=False)
    entry_line_id = Column(Integer, ForeignKey("journal_entry_lines.id"), nullable=False)
    
    # Movimientos
    debit = Column(Numeric(15, 2), default=0)
    credit = Column(Numeric(15, 2), default=0)
    
    # Saldos acumulados
    balance_debit = Column(Numeric(15, 2), default=0)  # Saldo deudor acumulado
    balance_credit = Column(Numeric(15, 2), default=0)  # Saldo acreedor acumulado
    
    # Información adicional
    description = Column(Text)
    reference = Column(String)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    business = relationship("BusinessConfiguration", backref="general_ledger")
    account = relationship("ChartOfAccounts", backref="ledger_entries")
    entry = relationship("JournalEntry", backref="ledger_entries")
    period = relationship("AccountingPeriod", backref="ledger_entries")

