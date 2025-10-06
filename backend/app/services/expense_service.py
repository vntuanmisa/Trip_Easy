from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict
from datetime import date, datetime
from decimal import Decimal
from ..models.models import (
    Expense as ExpenseModel, 
    Trip as TripModel, 
    TripMember as TripMemberModel,
    ExpenseCategory as ExpenseCategoryModel,
    ExpenseCategoryEnum
)
from ..schemas.schemas import ExpenseCreate, ExpenseUpdate, ExpenseCategoryCreate

class ExpenseService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_expense(self, trip_id: int, expense: ExpenseCreate) -> ExpenseModel:
        """Tạo chi phí mới cho chuyến đi"""
        # Kiểm tra chuyến đi có tồn tại không
        trip = self.db.query(TripModel).filter(TripModel.id == trip_id).first()
        if not trip:
            raise ValueError("Chuyến đi không tồn tại")
        
        # Kiểm tra thành viên trả tiền có tồn tại không
        member = self.db.query(TripMemberModel).filter(
            TripMemberModel.id == expense.paid_by,
            TripMemberModel.trip_id == trip_id
        ).first()
        if not member:
            raise ValueError("Thành viên trả tiền không tồn tại trong chuyến đi này")
        
        # Kiểm tra ngày chi phí có trong thời gian chuyến đi không
        if expense.date.date() < trip.start_date.date() or expense.date.date() > trip.end_date.date():
            raise ValueError("Ngày chi phí phải trong thời gian chuyến đi")
        
        # Tính tỷ giá quy đổi nếu khác tiền tệ chính
        exchange_rate = expense.exchange_rate
        if expense.currency != trip.currency:
            # Ở đây có thể tích hợp API tỷ giá thực tế
            # Hiện tại sử dụng tỷ giá người dùng nhập
            pass
        
        db_expense = ExpenseModel(
            trip_id=trip_id,
            activity_id=expense.activity_id,
            paid_by=expense.paid_by,
            description=expense.description,
            amount=expense.amount,
            currency=expense.currency,
            exchange_rate=exchange_rate,
            category=expense.category,
            is_shared=expense.is_shared,
            date=expense.date
        )
        
        self.db.add(db_expense)
        self.db.commit()
        self.db.refresh(db_expense)
        return db_expense
    
    def get_expenses_by_trip(
        self, 
        trip_id: int, 
        skip: int = 0, 
        limit: int = 100,
        category: Optional[ExpenseCategoryEnum] = None,
        paid_by: Optional[int] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        is_shared: Optional[bool] = None
    ) -> List[ExpenseModel]:
        """Lấy danh sách chi phí với bộ lọc"""
        query = self.db.query(ExpenseModel).filter(ExpenseModel.trip_id == trip_id)
        
        if category:
            query = query.filter(ExpenseModel.category == category)
        
        if paid_by:
            query = query.filter(ExpenseModel.paid_by == paid_by)
        
        if date_from:
            query = query.filter(ExpenseModel.date >= datetime.combine(date_from, datetime.min.time()))
        
        if date_to:
            query = query.filter(ExpenseModel.date <= datetime.combine(date_to, datetime.max.time()))
        
        if is_shared is not None:
            query = query.filter(ExpenseModel.is_shared == is_shared)
        
        return query.order_by(ExpenseModel.date.desc()).offset(skip).limit(limit).all()
    
    def get_expense(self, expense_id: int) -> Optional[ExpenseModel]:
        """Lấy thông tin chi phí theo ID"""
        return self.db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    
    def update_expense(self, expense_id: int, expense_update: ExpenseUpdate) -> Optional[ExpenseModel]:
        """Cập nhật thông tin chi phí"""
        db_expense = self.get_expense(expense_id)
        if not db_expense:
            return None
        
        update_data = expense_update.dict(exclude_unset=True)
        
        # Kiểm tra thành viên trả tiền nếu có cập nhật
        if 'paid_by' in update_data:
            member = self.db.query(TripMemberModel).filter(
                TripMemberModel.id == update_data['paid_by'],
                TripMemberModel.trip_id == db_expense.trip_id
            ).first()
            if not member:
                raise ValueError("Thành viên trả tiền không tồn tại trong chuyến đi này")
        
        # Kiểm tra ngày chi phí nếu có cập nhật
        if 'date' in update_data:
            trip = self.db.query(TripModel).filter(TripModel.id == db_expense.trip_id).first()
            if update_data['date'].date() < trip.start_date.date() or update_data['date'].date() > trip.end_date.date():
                raise ValueError("Ngày chi phí phải trong thời gian chuyến đi")
        
        for field, value in update_data.items():
            setattr(db_expense, field, value)
        
        db_expense.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_expense)
        return db_expense
    
    def delete_expense(self, expense_id: int, trip_id: int) -> bool:
        """Xóa chi phí"""
        db_expense = self.db.query(ExpenseModel).filter(
            ExpenseModel.id == expense_id,
            ExpenseModel.trip_id == trip_id
        ).first()
        
        if not db_expense:
            return False
        
        self.db.delete(db_expense)
        self.db.commit()
        return True
    
    def get_expense_summary(self, trip_id: int) -> Dict:
        """Lấy tóm tắt chi phí theo danh mục và ngày"""
        # Chi phí theo danh mục
        category_expenses = self.db.query(
            ExpenseModel.category,
            func.sum(ExpenseModel.amount * ExpenseModel.exchange_rate).label('total')
        ).filter(
            ExpenseModel.trip_id == trip_id,
            ExpenseModel.is_shared == True
        ).group_by(ExpenseModel.category).all()
        
        # Chi phí theo ngày
        date_expenses = self.db.query(
            func.date(ExpenseModel.date).label('date'),
            func.sum(ExpenseModel.amount * ExpenseModel.exchange_rate).label('total')
        ).filter(
            ExpenseModel.trip_id == trip_id,
            ExpenseModel.is_shared == True
        ).group_by(func.date(ExpenseModel.date)).all()
        
        return {
            'by_category': {str(cat): float(total) for cat, total in category_expenses},
            'by_date': {str(date): float(total) for date, total in date_expenses}
        }
    
    def get_expenses_by_member(self, trip_id: int) -> Dict:
        """Lấy chi phí theo từng thành viên"""
        member_expenses = self.db.query(
            TripMemberModel.id,
            TripMemberModel.name,
            func.sum(ExpenseModel.amount * ExpenseModel.exchange_rate).label('total_paid')
        ).join(
            ExpenseModel, TripMemberModel.id == ExpenseModel.paid_by
        ).filter(
            TripMemberModel.trip_id == trip_id
        ).group_by(TripMemberModel.id, TripMemberModel.name).all()
        
        return {
            member_id: {
                'name': name,
                'total_paid': float(total_paid)
            }
            for member_id, name, total_paid in member_expenses
        }
    
    # Expense Categories
    def create_expense_category(self, trip_id: int, category: ExpenseCategoryCreate) -> ExpenseCategoryModel:
        """Tạo danh mục chi phí tùy chỉnh"""
        db_category = ExpenseCategoryModel(
            trip_id=trip_id,
            name=category.name,
            color=category.color
        )
        
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category
    
    def get_expense_categories(self, trip_id: int) -> List[ExpenseCategoryModel]:
        """Lấy danh sách danh mục chi phí tùy chỉnh"""
        return self.db.query(ExpenseCategoryModel).filter(ExpenseCategoryModel.trip_id == trip_id).all()
    
    def delete_expense_category(self, category_id: int, trip_id: int) -> bool:
        """Xóa danh mục chi phí tùy chỉnh"""
        db_category = self.db.query(ExpenseCategoryModel).filter(
            ExpenseCategoryModel.id == category_id,
            ExpenseCategoryModel.trip_id == trip_id
        ).first()
        
        if not db_category:
            return False
        
        self.db.delete(db_category)
        self.db.commit()
        return True
