from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.models import Trip as TripModel, TripMember as TripMemberModel
from ..schemas.schemas import TripCreate, TripUpdate
from datetime import datetime

class TripService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_trip(self, trip: TripCreate, invite_code: str) -> TripModel:
        """Tạo chuyến đi mới"""
        db_trip = TripModel(
            name=trip.name,
            description=trip.description,
            destination=trip.destination,
            start_date=trip.start_date,
            end_date=trip.end_date,
            currency=trip.currency,
            child_factor=trip.child_factor,
            rounding_rule=trip.rounding_rule,
            invite_code=invite_code
        )
        
        self.db.add(db_trip)
        self.db.commit()
        self.db.refresh(db_trip)
        return db_trip
    
    def get_trips(self, skip: int = 0, limit: int = 100) -> List[TripModel]:
        """Lấy danh sách chuyến đi"""
        return self.db.query(TripModel).offset(skip).limit(limit).all()
    
    def get_trip(self, trip_id: int) -> Optional[TripModel]:
        """Lấy thông tin chuyến đi theo ID"""
        return self.db.query(TripModel).filter(TripModel.id == trip_id).first()
    
    def get_trip_by_invite_code(self, invite_code: str) -> Optional[TripModel]:
        """Lấy thông tin chuyến đi theo mã mời"""
        return self.db.query(TripModel).filter(TripModel.invite_code == invite_code).first()
    
    def update_trip(self, trip_id: int, trip_update: TripUpdate) -> Optional[TripModel]:
        """Cập nhật thông tin chuyến đi"""
        db_trip = self.get_trip(trip_id)
        if not db_trip:
            return None
        
        update_data = trip_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_trip, field, value)
        
        db_trip.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_trip)
        return db_trip
    
    def update_invite_code(self, trip_id: int, invite_code: str) -> Optional[TripModel]:
        """Cập nhật mã mời"""
        db_trip = self.get_trip(trip_id)
        if not db_trip:
            return None
        
        db_trip.invite_code = invite_code
        db_trip.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_trip)
        return db_trip
    
    def delete_trip(self, trip_id: int) -> bool:
        """Xóa chuyến đi"""
        db_trip = self.get_trip(trip_id)
        if not db_trip:
            return False
        
        self.db.delete(db_trip)
        self.db.commit()
        return True
    
    def validate_trip_dates(self, start_date: datetime, end_date: datetime) -> bool:
        """Kiểm tra tính hợp lệ của ngày tháng"""
        if start_date >= end_date:
            raise ValueError("Ngày kết thúc phải sau ngày bắt đầu")
        
        if start_date < datetime.now():
            raise ValueError("Ngày bắt đầu không thể trong quá khứ")
        
        return True
