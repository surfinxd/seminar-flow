from pydantic import BaseModel

class ReservationResponse(BaseModel):
    id: int
    seminar_id: int
    user_id: int

    class Config:
        from_attributes = True
