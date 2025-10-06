from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
from decimal import Decimal, ROUND_HALF_UP
from ..models.models import (
    Trip as TripModel,
    TripMember as TripMemberModel,
    Expense as ExpenseModel
)
from ..schemas.schemas import TripSummary, MemberBalance, Settlement

class SettlementService:
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_trip_summary(self, trip_id: int) -> TripSummary:
        """Tính toán báo cáo tổng hợp và chia tiền cho chuyến đi"""
        # Lấy thông tin chuyến đi
        trip = self.db.query(TripModel).filter(TripModel.id == trip_id).first()
        if not trip:
            raise ValueError("Chuyến đi không tồn tại")
        
        # Lấy danh sách thành viên
        members = self.db.query(TripMemberModel).filter(TripMemberModel.trip_id == trip_id).all()
        if not members:
            raise ValueError("Chuyến đi chưa có thành viên")
        
        # Tính tổng chi phí
        total_expenses = self._calculate_total_expenses(trip_id)
        total_shared_expenses = self._calculate_total_shared_expenses(trip_id)
        
        # Tính số dư cho từng thành viên
        member_balances = self._calculate_member_balances(trip_id, trip, members, total_shared_expenses)
        
        # Tính cách giải quyết nợ
        settlements = self._calculate_settlements(member_balances, trip.rounding_rule)
        
        # Thống kê chi phí theo danh mục và ngày
        expense_by_category = self._get_expense_by_category(trip_id)
        expense_by_date = self._get_expense_by_date(trip_id)
        
        return TripSummary(
            trip=trip,
            total_expenses=total_expenses,
            total_shared_expenses=total_shared_expenses,
            member_balances=member_balances,
            settlements=settlements,
            expense_by_category=expense_by_category,
            expense_by_date=expense_by_date
        )
    
    def _calculate_total_expenses(self, trip_id: int) -> Decimal:
        """Tính tổng chi phí của chuyến đi"""
        result = self.db.query(
            func.sum(ExpenseModel.amount * ExpenseModel.exchange_rate)
        ).filter(ExpenseModel.trip_id == trip_id).scalar()
        
        return Decimal(str(result)) if result else Decimal('0')
    
    def _calculate_total_shared_expenses(self, trip_id: int) -> Decimal:
        """Tính tổng chi phí chung của chuyến đi"""
        result = self.db.query(
            func.sum(ExpenseModel.amount * ExpenseModel.exchange_rate)
        ).filter(
            ExpenseModel.trip_id == trip_id,
            ExpenseModel.is_shared == True
        ).scalar()
        
        return Decimal(str(result)) if result else Decimal('0')
    
    def _calculate_member_balances(
        self, 
        trip_id: int, 
        trip: TripModel, 
        members: List[TripMemberModel], 
        total_shared_expenses: Decimal
    ) -> List[MemberBalance]:
        """Tính số dư cho từng thành viên theo thuật toán chia tiền thông minh"""
        
        # Tính tổng hệ số (Total Factor)
        total_factor = sum(Decimal(str(member.factor)) for member in members)
        
        if total_factor == 0:
            raise ValueError("Tổng hệ số thành viên không thể bằng 0")
        
        # Tính chi phí trên một đơn vị (Cost Per Factor)
        cost_per_factor = total_shared_expenses / total_factor if total_factor > 0 else Decimal('0')
        
        member_balances = []
        
        for member in members:
            # Tính số tiền đã trả
            total_paid_result = self.db.query(
                func.sum(ExpenseModel.amount * ExpenseModel.exchange_rate)
            ).filter(
                ExpenseModel.trip_id == trip_id,
                ExpenseModel.paid_by == member.id,
                ExpenseModel.is_shared == True
            ).scalar()
            
            total_paid = Decimal(str(total_paid_result)) if total_paid_result else Decimal('0')
            
            # Tính số tiền phải trả (Member Owes)
            member_factor = Decimal(str(member.factor))
            total_owed = cost_per_factor * member_factor
            
            # Làm tròn theo quy tắc của chuyến đi
            total_owed = self._round_amount(total_owed, trip.rounding_rule)
            
            # Tính số dư (Balance)
            balance = total_paid - total_owed
            balance = self._round_amount(balance, trip.rounding_rule)
            
            member_balances.append(MemberBalance(
                member_id=member.id,
                member_name=member.name,
                total_paid=total_paid,
                total_owed=total_owed,
                balance=balance
            ))
        
        return member_balances
    
    def _calculate_settlements(self, member_balances: List[MemberBalance], rounding_rule: int) -> List[Settlement]:
        """Tính cách giải quyết nợ tối ưu"""
        # Tách thành 2 nhóm: người nợ và người được nợ
        debtors = [mb for mb in member_balances if mb.balance < 0]  # Người phải trả
        creditors = [mb for mb in member_balances if mb.balance > 0]  # Người được nhận
        
        # Sắp xếp để tối ưu hóa số lượng giao dịch
        debtors.sort(key=lambda x: x.balance)  # Từ âm nhất đến ít âm nhất
        creditors.sort(key=lambda x: x.balance, reverse=True)  # Từ dương nhất đến ít dương nhất
        
        settlements = []
        debtor_idx = 0
        creditor_idx = 0
        
        while debtor_idx < len(debtors) and creditor_idx < len(creditors):
            debtor = debtors[debtor_idx]
            creditor = creditors[creditor_idx]
            
            # Tính số tiền giao dịch
            debt_amount = abs(debtor.balance)
            credit_amount = creditor.balance
            
            transfer_amount = min(debt_amount, credit_amount)
            transfer_amount = self._round_amount(transfer_amount, rounding_rule)
            
            if transfer_amount > 0:
                settlements.append(Settlement(
                    from_member_id=debtor.member_id,
                    from_member_name=debtor.member_name,
                    to_member_id=creditor.member_id,
                    to_member_name=creditor.member_name,
                    amount=transfer_amount
                ))
            
            # Cập nhật số dư
            debtor.balance += transfer_amount
            creditor.balance -= transfer_amount
            
            # Chuyển đến người tiếp theo nếu đã giải quyết xong
            if abs(debtor.balance) < Decimal('0.01'):  # Gần bằng 0
                debtor_idx += 1
            if abs(creditor.balance) < Decimal('0.01'):  # Gần bằng 0
                creditor_idx += 1
        
        return settlements
    
    def _round_amount(self, amount: Decimal, rounding_rule: int) -> Decimal:
        """Làm tròn số tiền theo quy tắc"""
        if rounding_rule <= 1:
            return amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Làm tròn đến bội số của rounding_rule
        rounded = (amount / rounding_rule).quantize(Decimal('1'), rounding=ROUND_HALF_UP) * rounding_rule
        return rounded
    
    def _get_expense_by_category(self, trip_id: int) -> Dict[str, float]:
        """Lấy chi phí theo danh mục"""
        result = self.db.query(
            ExpenseModel.category,
            func.sum(ExpenseModel.amount * ExpenseModel.exchange_rate).label('total')
        ).filter(
            ExpenseModel.trip_id == trip_id,
            ExpenseModel.is_shared == True
        ).group_by(ExpenseModel.category).all()
        
        return {str(category): float(total) for category, total in result}
    
    def _get_expense_by_date(self, trip_id: int) -> Dict[str, float]:
        """Lấy chi phí theo ngày"""
        result = self.db.query(
            func.date(ExpenseModel.date).label('date'),
            func.sum(ExpenseModel.amount * ExpenseModel.exchange_rate).label('total')
        ).filter(
            ExpenseModel.trip_id == trip_id,
            ExpenseModel.is_shared == True
        ).group_by(func.date(ExpenseModel.date)).all()
        
        return {str(date): float(total) for date, total in result}
    
    def get_member_debt_summary(self, trip_id: int, member_id: int) -> Dict:
        """Lấy tóm tắt nợ của một thành viên cụ thể"""
        trip_summary = self.calculate_trip_summary(trip_id)
        
        member_balance = next(
            (mb for mb in trip_summary.member_balances if mb.member_id == member_id),
            None
        )
        
        if not member_balance:
            raise ValueError("Thành viên không tồn tại trong chuyến đi")
        
        # Lấy các giao dịch liên quan đến thành viên này
        related_settlements = [
            s for s in trip_summary.settlements 
            if s.from_member_id == member_id or s.to_member_id == member_id
        ]
        
        return {
            'member_balance': member_balance,
            'related_settlements': related_settlements,
            'summary': {
                'should_pay': sum(s.amount for s in related_settlements if s.from_member_id == member_id),
                'should_receive': sum(s.amount for s in related_settlements if s.to_member_id == member_id)
            }
        }
