from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token

user_repo = UserRepository()

class AuthService:
    def signup(self, db: Session, user_in: UserCreate):
        if user_repo.get_by_username(db, user_in.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        hashed_password = get_password_hash(user_in.password)
        new_user = User(username=user_in.username, hashed_password=hashed_password)
        return user_repo.create(db, new_user)

    def login(self, db: Session, username: str, password: str):
        user = user_repo.get_by_username(db, username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
