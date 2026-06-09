from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.seminar import SeminarCreate, SeminarResponse
from app.services.seminar_service import SeminarService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()
seminar_service = SeminarService()

@router.post("", response_model=SeminarResponse)
def create_seminar(
    seminar_in: SeminarCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return seminar_service.create_seminar(db, seminar_in)

@router.get("", response_model=List[SeminarResponse])
def list_seminars(db: Session = Depends(get_db)):
    return seminar_service.list_seminars(db)

@router.get("/{seminar_id}", response_model=SeminarResponse)
def get_seminar(seminar_id: int, db: Session = Depends(get_db)):
    return seminar_service.get_seminar(db, seminar_id)
