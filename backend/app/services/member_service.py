from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.models import TripMember as TripMemberModel, Trip as TripModel
from ..schemas.schemas import TripMemberCreate, TripMemberUpdate

class MemberService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_member(self, trip_id: int, member: TripMemberCreate) -> TripMemberModel:
        """Tạo thành viên mới cho chuyến đi"""
        # Kiểm tra chuyến đi có tồn tại không
        trip = self.db.query(TripModel).filter(TripModel.id == trip_id).first()
        if not trip:
            raise ValueError("Chuyến đi không tồn tại")
        
        # Kiểm tra tên thành viên đã tồn tại chưa
        existing_member = self.db.query(TripMemberModel).filter(
            TripMemberModel.trip_id == trip_id,
            TripMemberModel.name == member.name
        ).first()
        if existing_member:
            raise ValueError("Tên thành viên đã tồn tại trong chuyến đi này")
        
        # Kiểm tra email đã tồn tại chưa (nếu có)
        if member.email:
            existing_email = self.db.query(TripMemberModel).filter(
                TripMemberModel.trip_id == trip_id,
                TripMemberModel.email == member.email
            ).first()
            if existing_email:
                raise ValueError("Email đã được sử dụng trong chuyến đi này")
        
        # Kiểm tra xem đã có admin chưa, nếu chưa thì thành viên đầu tiên sẽ là admin
        member_count = self.db.query(TripMemberModel).filter(TripMemberModel.trip_id == trip_id).count()
        is_admin = member_count == 0
        
        db_member = TripMemberModel(
            trip_id=trip_id,
            name=member.name,
            email=member.email,
            factor=member.factor,
            is_admin=is_admin
        )
        
        self.db.add(db_member)
        self.db.commit()
        self.db.refresh(db_member)
        return db_member
    
    def get_members_by_trip(self, trip_id: int) -> List[TripMemberModel]:
        """Lấy danh sách thành viên của chuyến đi"""
        return self.db.query(TripMemberModel).filter(TripMemberModel.trip_id == trip_id).all()
    
    def get_member(self, member_id: int) -> Optional[TripMemberModel]:
        """Lấy thông tin thành viên theo ID"""
        return self.db.query(TripMemberModel).filter(TripMemberModel.id == member_id).first()
    
    def update_member(self, member_id: int, member_update: TripMemberUpdate) -> Optional[TripMemberModel]:
        """Cập nhật thông tin thành viên"""
        db_member = self.get_member(member_id)
        if not db_member:
            return None
        
        update_data = member_update.dict(exclude_unset=True)
        
        # Kiểm tra tên không trùng với thành viên khác
        if 'name' in update_data:
            existing_member = self.db.query(TripMemberModel).filter(
                TripMemberModel.trip_id == db_member.trip_id,
                TripMemberModel.name == update_data['name'],
                TripMemberModel.id != member_id
            ).first()
            if existing_member:
                raise ValueError("Tên thành viên đã tồn tại trong chuyến đi này")
        
        # Kiểm tra email không trùng với thành viên khác
        if 'email' in update_data and update_data['email']:
            existing_email = self.db.query(TripMemberModel).filter(
                TripMemberModel.trip_id == db_member.trip_id,
                TripMemberModel.email == update_data['email'],
                TripMemberModel.id != member_id
            ).first()
            if existing_email:
                raise ValueError("Email đã được sử dụng trong chuyến đi này")
        
        for field, value in update_data.items():
            setattr(db_member, field, value)
        
        self.db.commit()
        self.db.refresh(db_member)
        return db_member
    
    def delete_member(self, member_id: int, trip_id: int) -> bool:
        """Xóa thành viên khỏi chuyến đi"""
        db_member = self.db.query(TripMemberModel).filter(
            TripMemberModel.id == member_id,
            TripMemberModel.trip_id == trip_id
        ).first()
        
        if not db_member:
            return False
        
        # Không cho phép xóa admin duy nhất
        if db_member.is_admin:
            admin_count = self.db.query(TripMemberModel).filter(
                TripMemberModel.trip_id == trip_id,
                TripMemberModel.is_admin == True
            ).count()
            if admin_count == 1:
                raise ValueError("Không thể xóa admin duy nhất của chuyến đi")
        
        self.db.delete(db_member)
        self.db.commit()
        return True
    
    def join_trip(self, trip_id: int, member: TripMemberCreate) -> TripMemberModel:
        """Tham gia chuyến đi"""
        return self.create_member(trip_id, member)
    
    def set_admin(self, member_id: int, is_admin: bool) -> Optional[TripMemberModel]:
        """Thiết lập quyền admin cho thành viên"""
        db_member = self.get_member(member_id)
        if not db_member:
            return None
        
        db_member.is_admin = is_admin
        self.db.commit()
        self.db.refresh(db_member)
        return db_member
