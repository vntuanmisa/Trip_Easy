from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..schemas.schemas import TripMember, TripMemberCreate, TripMemberUpdate
from ..services.member_service import MemberService

router = APIRouter()

@router.post("/{trip_id}/members", response_model=TripMember, status_code=status.HTTP_201_CREATED)
async def create_member(trip_id: int, member: TripMemberCreate, db: Session = Depends(get_db)):
    """Thêm thành viên vào chuyến đi"""
    try:
        member_service = MemberService(db)
        return member_service.create_member(trip_id, member)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Không thể thêm thành viên: {str(e)}"
        )

@router.get("/{trip_id}/members", response_model=List[TripMember])
async def get_members(trip_id: int, db: Session = Depends(get_db)):
    """Lấy danh sách thành viên của chuyến đi"""
    member_service = MemberService(db)
    return member_service.get_members_by_trip(trip_id)

@router.get("/{trip_id}/members/{member_id}", response_model=TripMember)
async def get_member(trip_id: int, member_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin thành viên"""
    member_service = MemberService(db)
    member = member_service.get_member(member_id)
    if not member or member.trip_id != trip_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy thành viên"
        )
    return member

@router.put("/{trip_id}/members/{member_id}", response_model=TripMember)
async def update_member(trip_id: int, member_id: int, member_update: TripMemberUpdate, db: Session = Depends(get_db)):
    """Cập nhật thông tin thành viên"""
    member_service = MemberService(db)
    member = member_service.update_member(member_id, member_update)
    if not member or member.trip_id != trip_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy thành viên"
        )
    return member

@router.delete("/{trip_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member(trip_id: int, member_id: int, db: Session = Depends(get_db)):
    """Xóa thành viên khỏi chuyến đi"""
    member_service = MemberService(db)
    success = member_service.delete_member(member_id, trip_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy thành viên"
        )

@router.post("/{trip_id}/join", response_model=TripMember)
async def join_trip(trip_id: int, member: TripMemberCreate, db: Session = Depends(get_db)):
    """Tham gia chuyến đi bằng mã mời"""
    try:
        member_service = MemberService(db)
        return member_service.join_trip(trip_id, member)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Không thể tham gia chuyến đi: {str(e)}"
        )
