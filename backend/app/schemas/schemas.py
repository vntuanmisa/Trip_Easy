from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from ..models.models import CurrencyEnum, ExpenseCategoryEnum

# Base schemas
class TripBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    destination: str = Field(..., min_length=1, max_length=255)
    start_date: datetime
    end_date: datetime
    currency: CurrencyEnum = CurrencyEnum.VND
    child_factor: Decimal = Field(default=Decimal("0.5"), ge=0, le=2)
    rounding_rule: int = Field(default=1000, ge=1)

class TripCreate(TripBase):
    pass

class TripUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    destination: Optional[str] = Field(None, min_length=1, max_length=255)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    currency: Optional[CurrencyEnum] = None
    child_factor: Optional[Decimal] = Field(None, ge=0, le=2)
    rounding_rule: Optional[int] = Field(None, ge=1)

class Trip(TripBase):
    id: int
    invite_code: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Trip Member schemas
class TripMemberBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    factor: Decimal = Field(default=Decimal("1.0"), ge=0, le=5)

class TripMemberCreate(TripMemberBase):
    pass

class TripMemberUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    factor: Optional[Decimal] = Field(None, ge=0, le=5)

class TripMember(TripMemberBase):
    id: int
    trip_id: int
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Activity schemas
class ActivityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    date: datetime
    location: Optional[str] = Field(None, max_length=500)
    latitude: Optional[Decimal] = Field(None, ge=-90, le=90)
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180)

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=500)
    latitude: Optional[Decimal] = Field(None, ge=-90, le=90)
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180)

class Activity(ActivityBase):
    id: int
    trip_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Expense schemas
class ExpenseBase(BaseModel):
    description: str = Field(..., min_length=1, max_length=500)
    amount: Decimal = Field(..., gt=0)
    currency: CurrencyEnum
    exchange_rate: Decimal = Field(default=Decimal("1.0"), gt=0)
    category: ExpenseCategoryEnum = ExpenseCategoryEnum.OTHER
    is_shared: bool = True
    date: datetime
    activity_id: Optional[int] = None

class ExpenseCreate(ExpenseBase):
    paid_by: int

class ExpenseUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    amount: Optional[Decimal] = Field(None, gt=0)
    currency: Optional[CurrencyEnum] = None
    exchange_rate: Optional[Decimal] = Field(None, gt=0)
    category: Optional[ExpenseCategoryEnum] = None
    is_shared: Optional[bool] = None
    date: Optional[datetime] = None
    paid_by: Optional[int] = None
    activity_id: Optional[int] = None

class Expense(ExpenseBase):
    id: int
    trip_id: int
    paid_by: int
    created_at: datetime
    updated_at: datetime
    paid_by_member: TripMember
    
    class Config:
        from_attributes = True

# Expense Category schemas
class ExpenseCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    color: str = Field(default="#6B7280", regex=r"^#[0-9A-Fa-f]{6}$")

class ExpenseCategoryCreate(ExpenseCategoryBase):
    pass

class ExpenseCategory(ExpenseCategoryBase):
    id: int
    trip_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Response schemas with related data
class TripWithDetails(Trip):
    members: List[TripMember] = []
    activities: List[Activity] = []
    expenses: List[Expense] = []

# Settlement calculation schemas
class MemberBalance(BaseModel):
    member_id: int
    member_name: str
    total_paid: Decimal
    total_owed: Decimal
    balance: Decimal  # positive = should receive, negative = should pay

class Settlement(BaseModel):
    from_member_id: int
    from_member_name: str
    to_member_id: int
    to_member_name: str
    amount: Decimal

class TripSummary(BaseModel):
    trip: Trip
    total_expenses: Decimal
    total_shared_expenses: Decimal
    member_balances: List[MemberBalance]
    settlements: List[Settlement]
    expense_by_category: dict
    expense_by_date: dict
