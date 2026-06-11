from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.endpoints import auth, seminars, reservations
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    engine.dispose()

app = FastAPI(title="SeminarFlow v2.0", lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(seminars.router, prefix="/seminars", tags=["seminars"])
app.include_router(reservations.router, prefix="/seminars", tags=["reservations"])

from fastapi.responses import HTMLResponse
import os

@app.get("/")
def read_root():
    return {"message": "Welcome to SeminarFlow v2.0"}

@app.get("/web", response_class=HTMLResponse)
def serve_web():
    file_path = os.path.join(os.path.dirname(__file__), "static/index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
