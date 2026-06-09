from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    seminar_id = Column(Integer, ForeignKey("seminars.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
