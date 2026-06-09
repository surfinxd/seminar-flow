from sqlalchemy.orm import Session
from app.models.reservation import Reservation

class ReservationRepository:
    def create(self, db: Session, reservation: Reservation):
        db.add(reservation)
        db.commit()
        db.refresh(reservation)
        return reservation
