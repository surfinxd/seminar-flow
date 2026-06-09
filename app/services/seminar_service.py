from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.seminar_repository import SeminarRepository
from app.schemas.seminar import SeminarCreate
from app.models.seminar import Seminar

seminar_repo = SeminarRepository()

class SeminarService:
    def create_seminar(self, db: Session, seminar_in: SeminarCreate):
        new_seminar = Seminar(
            title=seminar_in.title,
            description=seminar_in.description,
            max_capacity=seminar_in.max_capacity,
            current_registered=0
        )
        return seminar_repo.create(db, new_seminar)

    def list_seminars(self, db: Session):
        return seminar_repo.get_all(db)

    def get_seminar(self, db: Session, seminar_id: int):
        seminar = seminar_repo.get_by_id(db, seminar_id)
        if not seminar:
            raise HTTPException(status_code=404, detail="Seminar not found")
        return seminar
