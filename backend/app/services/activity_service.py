from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import date, datetime
from ..models.models import Activity as ActivityModel, Trip as TripModel
from ..schemas.schemas import ActivityCreate, ActivityUpdate

class ActivityService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_activity(self, trip_id: int, activity: ActivityCreate) -> ActivityModel:
        """Tạo hoạt động mới cho chuyến đi"""
        # Kiểm tra chuyến đi có tồn tại không
        trip = self.db.query(TripModel).filter(TripModel.id == trip_id).first()
        if not trip:
            raise ValueError("Chuyến đi không tồn tại")
        
        # Kiểm tra ngày hoạt động có trong thời gian chuyến đi không
        if activity.date.date() < trip.start_date.date() or activity.date.date() > trip.end_date.date():
            raise ValueError("Ngày hoạt động phải trong thời gian chuyến đi")
        
        db_activity = ActivityModel(
            trip_id=trip_id,
            name=activity.name,
            description=activity.description,
            date=activity.date,
            location=activity.location,
            latitude=activity.latitude,
            longitude=activity.longitude
        )
        
        self.db.add(db_activity)
        self.db.commit()
        self.db.refresh(db_activity)
        return db_activity
    
    def get_activities_by_trip(self, trip_id: int, date_filter: Optional[date] = None) -> List[ActivityModel]:
        """Lấy danh sách hoạt động của chuyến đi"""
        query = self.db.query(ActivityModel).filter(ActivityModel.trip_id == trip_id)
        
        if date_filter:
            query = query.filter(ActivityModel.date.date() == date_filter)
        
        return query.order_by(ActivityModel.date.asc()).all()
    
    def get_activity(self, activity_id: int) -> Optional[ActivityModel]:
        """Lấy thông tin hoạt động theo ID"""
        return self.db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()
    
    def update_activity(self, activity_id: int, activity_update: ActivityUpdate) -> Optional[ActivityModel]:
        """Cập nhật thông tin hoạt động"""
        db_activity = self.get_activity(activity_id)
        if not db_activity:
            return None
        
        update_data = activity_update.dict(exclude_unset=True)
        
        # Kiểm tra ngày hoạt động nếu có cập nhật
        if 'date' in update_data:
            trip = self.db.query(TripModel).filter(TripModel.id == db_activity.trip_id).first()
            if update_data['date'].date() < trip.start_date.date() or update_data['date'].date() > trip.end_date.date():
                raise ValueError("Ngày hoạt động phải trong thời gian chuyến đi")
        
        for field, value in update_data.items():
            setattr(db_activity, field, value)
        
        db_activity.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_activity)
        return db_activity
    
    def delete_activity(self, activity_id: int, trip_id: int) -> bool:
        """Xóa hoạt động"""
        db_activity = self.db.query(ActivityModel).filter(
            ActivityModel.id == activity_id,
            ActivityModel.trip_id == trip_id
        ).first()
        
        if not db_activity:
            return False
        
        self.db.delete(db_activity)
        self.db.commit()
        return True
    
    def get_activities_grouped_by_date(self, trip_id: int) -> Dict[str, List[ActivityModel]]:
        """Lấy hoạt động nhóm theo ngày"""
        activities = self.get_activities_by_trip(trip_id)
        grouped = {}
        
        for activity in activities:
            date_key = activity.date.strftime("%Y-%m-%d")
            if date_key not in grouped:
                grouped[date_key] = []
            grouped[date_key].append(activity)
        
        return grouped
    
    def get_activities_by_location(self, trip_id: int, latitude: float, longitude: float, radius_km: float = 1.0) -> List[ActivityModel]:
        """Lấy hoạt động gần một vị trí cụ thể"""
        # Sử dụng công thức Haversine để tính khoảng cách
        # Đây là implementation đơn giản, có thể cải thiện bằng PostGIS nếu cần
        activities = self.get_activities_by_trip(trip_id)
        nearby_activities = []
        
        for activity in activities:
            if activity.latitude and activity.longitude:
                distance = self._calculate_distance(
                    float(activity.latitude), float(activity.longitude),
                    latitude, longitude
                )
                if distance <= radius_km:
                    nearby_activities.append(activity)
        
        return nearby_activities
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Tính khoảng cách giữa 2 điểm bằng công thức Haversine (km)"""
        import math
        
        R = 6371  # Bán kính trái đất (km)
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
