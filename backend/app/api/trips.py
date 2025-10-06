from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.models import Trip as TripModel, TripMember as TripMemberModel
from ..schemas.schemas import Trip, TripCreate, TripUpdate, TripWithDetails, TripSummary
from ..services.trip_service import TripService
from ..services.settlement_service import SettlementService
import random
import string

router = APIRouter()

def generate_invite_code() -> str:
    """Tạo mã mời ngẫu nhiên"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@router.post("/", response_model=Trip, status_code=status.HTTP_201_CREATED)
async def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    """Tạo chuyến đi mới"""
    try:
        trip_service = TripService(db)
        
        # Tạo mã mời duy nhất
        invite_code = generate_invite_code()
        while trip_service.get_trip_by_invite_code(invite_code):
            invite_code = generate_invite_code()
        
        return trip_service.create_trip(trip, invite_code)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Không thể tạo chuyến đi: {str(e)}"
        )

@router.get("/", response_model=List[Trip])
async def get_trips(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lấy danh sách chuyến đi"""
    trip_service = TripService(db)
    return trip_service.get_trips(skip=skip, limit=limit)

@router.get("/{trip_id}", response_model=TripWithDetails)
async def get_trip(trip_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin chi tiết chuyến đi"""
    trip_service = TripService(db)
    trip = trip_service.get_trip(trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chuyến đi"
        )
    return trip

@router.get("/invite/{invite_code}", response_model=Trip)
async def get_trip_by_invite_code(invite_code: str, db: Session = Depends(get_db)):
    """Lấy thông tin chuyến đi bằng mã mời"""
    trip_service = TripService(db)
    trip = trip_service.get_trip_by_invite_code(invite_code)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mã mời không hợp lệ"
        )
    return trip

@router.put("/{trip_id}", response_model=Trip)
async def update_trip(trip_id: int, trip_update: TripUpdate, db: Session = Depends(get_db)):
    """Cập nhật thông tin chuyến đi"""
    trip_service = TripService(db)
    trip = trip_service.update_trip(trip_id, trip_update)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chuyến đi"
        )
    return trip

@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    """Xóa chuyến đi"""
    trip_service = TripService(db)
    success = trip_service.delete_trip(trip_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chuyến đi"
        )

@router.get("/{trip_id}/summary", response_model=TripSummary)
async def get_trip_summary(trip_id: int, db: Session = Depends(get_db)):
    """Lấy báo cáo tổng hợp chuyến đi"""
    trip_service = TripService(db)
    settlement_service = SettlementService(db)
    
    trip = trip_service.get_trip(trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chuyến đi"
        )
    
    return settlement_service.calculate_trip_summary(trip_id)

@router.post("/{trip_id}/regenerate-invite", response_model=Trip)
async def regenerate_invite_code(trip_id: int, db: Session = Depends(get_db)):
    """Tạo lại mã mời cho chuyến đi"""
    trip_service = TripService(db)
    
    # Tạo mã mời mới
    invite_code = generate_invite_code()
    while trip_service.get_trip_by_invite_code(invite_code):
        invite_code = generate_invite_code()
    
    trip = trip_service.update_invite_code(trip_id, invite_code)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chuyến đi"
        )
    return trip
