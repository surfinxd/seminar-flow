from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.reservation import ReservationResponse
from app.services.reservation_service import ReservationService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()
reservation_service = ReservationService()

@router.post("/{seminar_id}/reservations", response_model=ReservationResponse)
def create_reservation(
    seminar_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return reservation_service.create_reservation(db, seminar_id, current_user.id)
