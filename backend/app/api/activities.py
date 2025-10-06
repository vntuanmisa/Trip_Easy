from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from ..core.database import get_db
from ..schemas.schemas import Activity, ActivityCreate, ActivityUpdate
from ..services.activity_service import ActivityService

router = APIRouter()

@router.post("/{trip_id}/activities", response_model=Activity, status_code=status.HTTP_201_CREATED)
async def create_activity(trip_id: int, activity: ActivityCreate, db: Session = Depends(get_db)):
    """Tạo hoạt động mới cho chuyến đi"""
    try:
        activity_service = ActivityService(db)
        return activity_service.create_activity(trip_id, activity)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Không thể tạo hoạt động: {str(e)}"
        )

@router.get("/{trip_id}/activities", response_model=List[Activity])
async def get_activities(trip_id: int, date_filter: date = None, db: Session = Depends(get_db)):
    """Lấy danh sách hoạt động của chuyến đi"""
    activity_service = ActivityService(db)
    return activity_service.get_activities_by_trip(trip_id, date_filter)

@router.get("/{trip_id}/activities/{activity_id}", response_model=Activity)
async def get_activity(trip_id: int, activity_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin hoạt động"""
    activity_service = ActivityService(db)
    activity = activity_service.get_activity(activity_id)
    if not activity or activity.trip_id != trip_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hoạt động"
        )
    return activity

@router.put("/{trip_id}/activities/{activity_id}", response_model=Activity)
async def update_activity(trip_id: int, activity_id: int, activity_update: ActivityUpdate, db: Session = Depends(get_db)):
    """Cập nhật thông tin hoạt động"""
    activity_service = ActivityService(db)
    activity = activity_service.update_activity(activity_id, activity_update)
    if not activity or activity.trip_id != trip_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hoạt động"
        )
    return activity

@router.delete("/{trip_id}/activities/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(trip_id: int, activity_id: int, db: Session = Depends(get_db)):
    """Xóa hoạt động"""
    activity_service = ActivityService(db)
    success = activity_service.delete_activity(activity_id, trip_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hoạt động"
        )

@router.get("/{trip_id}/activities/by-date", response_model=dict)
async def get_activities_by_date(trip_id: int, db: Session = Depends(get_db)):
    """Lấy hoạt động nhóm theo ngày"""
    activity_service = ActivityService(db)
    return activity_service.get_activities_grouped_by_date(trip_id)
