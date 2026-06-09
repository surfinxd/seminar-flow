from pydantic import BaseModel

class SeminarCreate(BaseModel):
    title: str
    description: str
    max_capacity: int

class SeminarResponse(BaseModel):
    id: int
    title: str
    description: str
    max_capacity: int
    current_registered: int

    class Config:
        from_attributes = True
