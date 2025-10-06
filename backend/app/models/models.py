from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum

class CurrencyEnum(str, enum.Enum):
    VND = "VND"
    USD = "USD"
    EUR = "EUR"
    JPY = "JPY"
    KRW = "KRW"
    THB = "THB"

class ExpenseCategoryEnum(str, enum.Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ACCOMMODATION = "accommodation"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    OTHER = "other"

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    destination = Column(String(255), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    currency = Column(Enum(CurrencyEnum), default=CurrencyEnum.VND)
    child_factor = Column(DECIMAL(3, 2), default=0.5)  # Hệ số cho trẻ em
    rounding_rule = Column(Integer, default=1000)  # Làm tròn đến hàng nghìn
    invite_code = Column(String(10), unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    members = relationship("TripMember", back_populates="trip", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="trip", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="trip", cascade="all, delete-orphan")

class TripMember(Base):
    __tablename__ = "trip_members"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    factor = Column(DECIMAL(3, 2), default=1.0)  # Hệ số chia tiền
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    trip = relationship("Trip", back_populates="members")
    expenses_paid = relationship("Expense", back_populates="paid_by_member")

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False)
    location = Column(String(500), nullable=True)
    latitude = Column(DECIMAL(10, 8), nullable=True)
    longitude = Column(DECIMAL(11, 8), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    trip = relationship("Trip", back_populates="activities")
    expenses = relationship("Expense", back_populates="activity")

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    paid_by = Column(Integer, ForeignKey("trip_members.id"), nullable=False)
    description = Column(String(500), nullable=False)
    amount = Column(DECIMAL(15, 2), nullable=False)
    currency = Column(Enum(CurrencyEnum), nullable=False)
    exchange_rate = Column(DECIMAL(10, 4), default=1.0)  # Tỷ giá quy đổi về tiền tệ chính
    category = Column(Enum(ExpenseCategoryEnum), default=ExpenseCategoryEnum.OTHER)
    is_shared = Column(Boolean, default=True)  # Chi phí chung hay riêng
    date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    trip = relationship("Trip", back_populates="expenses")
    activity = relationship("Activity", back_populates="expenses")
    paid_by_member = relationship("TripMember", back_populates="expenses_paid")

class ExpenseCategory(Base):
    __tablename__ = "expense_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    name = Column(String(255), nullable=False)
    color = Column(String(7), default="#6B7280")  # Hex color code
    created_at = Column(DateTime, server_default=func.now())
