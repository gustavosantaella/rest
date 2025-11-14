from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"         # Pendiente - recién creada
    PREPARING = "preparing"     # Preparando - en cocina
    COMPLETED = "completed"     # Completada - lista para servir/entregar
    CANCELLED = "cancelled"     # Cancelada


class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    CARD = "card"
    TRANSFER = "transfer"
    MIXED = "mixed"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"  # Sin pagos
    PARTIAL = "partial"  # Pagado parcialmente
    PAID = "paid"        # Completamente pagado


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_configuration.id"), nullable=False, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Mesero que atiende
    
    status = Column(String, default=OrderStatus.PENDING.value, nullable=False)  # Use string to store enum value
    payment_method = Column(String, nullable=True)  # Deprecated, usar payments
    payment_status = Column(String, default="pending", nullable=False)  # pending, partial, paid
    
    subtotal = Column(Float, default=0)
    tax = Column(Float, default=0)
    discount = Column(Float, default=0)
    total = Column(Float, default=0)
    
    # Información del cliente (opcional)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True, index=True)
    customer_name = Column(String, nullable=True)  # Deprecated - usar customer_id
    customer_email = Column(String, nullable=True)  # Deprecated - usar customer_id
    customer_phone = Column(String, nullable=True)  # Deprecated - usar customer_id
    
    # Relación con cliente
    customer = relationship("Customer", back_populates="orders")
    
    notes = Column(Text)  # Notas especiales del pedido
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    paid_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("OrderPayment", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    
    # Puede ser producto directo O item del menú (al menos uno debe existir)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=True)
    source_type = Column(String, default="product")  # 'product' o 'menu'
    
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)  # Precio al momento de la orden
    subtotal = Column(Float, nullable=False)
    
    notes = Column(Text)  # Notas especiales del item (sin cebolla, etc.)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    
    order = relationship("Order", back_populates="items")

