from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Seminar(Base):
    __tablename__ = "seminars"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    max_capacity = Column(Integer, nullable=False)
    current_registered = Column(Integer, default=0)
