from sqlalchemy.orm import Session
from app.models.seminar import Seminar

class SeminarRepository:
    def create(self, db: Session, seminar: Seminar):
        db.add(seminar)
        db.commit()
        db.refresh(seminar)
        return seminar

    def get_all(self, db: Session):
        return db.query(Seminar).all()

    def get_by_id(self, db: Session, seminar_id: int):
        return db.query(Seminar).filter(Seminar.id == seminar_id).first()
