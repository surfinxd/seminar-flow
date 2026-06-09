from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.seminar import Seminar
from app.models.reservation import Reservation
from app.repositories.reservation_repository import ReservationRepository

reservation_repo = ReservationRepository()

class ReservationService:
    def create_reservation(self, db: Session, seminar_id: int, user_id: int):
        # Pessimistic Locking
        seminar = db.query(Seminar).filter(Seminar.id == seminar_id).with_for_update().first()
        if not seminar:
            raise HTTPException(status_code=404, detail="Seminar not found")
        
        if seminar.current_registered >= seminar.max_capacity:
            db.rollback()
            raise HTTPException(status_code=400, detail="Seminar is at full capacity")
            
        seminar.current_registered += 1
        
        new_reservation = Reservation(seminar_id=seminar_id, user_id=user_id)
        db.add(seminar)
        return reservation_repo.create(db, new_reservation)
