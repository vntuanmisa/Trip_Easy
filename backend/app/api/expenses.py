from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from ..core.database import get_db
from ..schemas.schemas import Expense, ExpenseCreate, ExpenseUpdate, ExpenseCategory, ExpenseCategoryCreate
from ..services.expense_service import ExpenseService
from ..models.models import ExpenseCategoryEnum

router = APIRouter()

@router.post("/{trip_id}/expenses", response_model=Expense, status_code=status.HTTP_201_CREATED)
async def create_expense(trip_id: int, expense: ExpenseCreate, db: Session = Depends(get_db)):
    """Tạo chi phí mới cho chuyến đi"""
    try:
        expense_service = ExpenseService(db)
        return expense_service.create_expense(trip_id, expense)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Không thể tạo chi phí: {str(e)}"
        )

@router.get("/{trip_id}/expenses", response_model=List[Expense])
async def get_expenses(
    trip_id: int, 
    skip: int = 0, 
    limit: int = 100,
    category: Optional[ExpenseCategoryEnum] = None,
    paid_by: Optional[int] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    is_shared: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Lấy danh sách chi phí của chuyến đi với bộ lọc"""
    expense_service = ExpenseService(db)
    return expense_service.get_expenses_by_trip(
        trip_id=trip_id,
        skip=skip,
        limit=limit,
        category=category,
        paid_by=paid_by,
        date_from=date_from,
        date_to=date_to,
        is_shared=is_shared
    )

@router.get("/{trip_id}/expenses/{expense_id}", response_model=Expense)
async def get_expense(trip_id: int, expense_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin chi phí"""
    expense_service = ExpenseService(db)
    expense = expense_service.get_expense(expense_id)
    if not expense or expense.trip_id != trip_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chi phí"
        )
    return expense

@router.put("/{trip_id}/expenses/{expense_id}", response_model=Expense)
async def update_expense(trip_id: int, expense_id: int, expense_update: ExpenseUpdate, db: Session = Depends(get_db)):
    """Cập nhật thông tin chi phí"""
    expense_service = ExpenseService(db)
    expense = expense_service.update_expense(expense_id, expense_update)
    if not expense or expense.trip_id != trip_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chi phí"
        )
    return expense

@router.delete("/{trip_id}/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(trip_id: int, expense_id: int, db: Session = Depends(get_db)):
    """Xóa chi phí"""
    expense_service = ExpenseService(db)
    success = expense_service.delete_expense(expense_id, trip_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chi phí"
        )

@router.get("/{trip_id}/expenses/summary", response_model=dict)
async def get_expense_summary(trip_id: int, db: Session = Depends(get_db)):
    """Lấy tóm tắt chi phí theo danh mục và ngày"""
    expense_service = ExpenseService(db)
    return expense_service.get_expense_summary(trip_id)

@router.get("/{trip_id}/expenses/by-member", response_model=dict)
async def get_expenses_by_member(trip_id: int, db: Session = Depends(get_db)):
    """Lấy chi phí theo từng thành viên"""
    expense_service = ExpenseService(db)
    return expense_service.get_expenses_by_member(trip_id)

# Expense Categories
@router.post("/{trip_id}/categories", response_model=ExpenseCategory, status_code=status.HTTP_201_CREATED)
async def create_expense_category(trip_id: int, category: ExpenseCategoryCreate, db: Session = Depends(get_db)):
    """Tạo danh mục chi phí tùy chỉnh"""
    try:
        expense_service = ExpenseService(db)
        return expense_service.create_expense_category(trip_id, category)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Không thể tạo danh mục: {str(e)}"
        )

@router.get("/{trip_id}/categories", response_model=List[ExpenseCategory])
async def get_expense_categories(trip_id: int, db: Session = Depends(get_db)):
    """Lấy danh sách danh mục chi phí tùy chỉnh"""
    expense_service = ExpenseService(db)
    return expense_service.get_expense_categories(trip_id)

@router.delete("/{trip_id}/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense_category(trip_id: int, category_id: int, db: Session = Depends(get_db)):
    """Xóa danh mục chi phí tùy chỉnh"""
    expense_service = ExpenseService(db)
    success = expense_service.delete_expense_category(category_id, trip_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy danh mục"
        )
