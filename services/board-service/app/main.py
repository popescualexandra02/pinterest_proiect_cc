from fastapi import FastAPI, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import Base, engine, SessionLocal
from app.models import Board
from app.schemas import BoardCreate, BoardOut
from app.config import settings

app = FastAPI(title=settings.service_name)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_id(x_user_id: Optional[str] = Header(default=None)) -> int:
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing X-User-Id")
    return int(x_user_id)


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.service_name}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.post("/boards", response_model=BoardOut)
def create_board(
    payload: BoardCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
):
    board = Board(user_id=user_id, name=payload.name)
    db.add(board)
    db.commit()
    db.refresh(board)
    return board


@app.get("/boards", response_model=list[BoardOut])
def list_boards(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
):
    return db.query(Board).filter(Board.user_id == user_id).all()
