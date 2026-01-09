from fastapi import FastAPI, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from typing import Optional


from app.config import settings
from app.database import Base, engine, SessionLocal
from app.models import Pin
from app.schemas import PinCreate, PinOut

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
        raise HTTPException(status_code=401, detail="Missing X-User-Id header")
    try:
        return int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="X-User-Id must be an integer")


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.service_name}


@app.get("/ready")
def ready():
    # minimal readiness: if app is up
    return {"status": "ready"}


@app.post("/pins", response_model=PinOut)
def create_pin(payload: PinCreate, db: Session = Depends(get_db), user_id: int = Depends(get_user_id)):
    pin = Pin(
        user_id=user_id,
        title=payload.title,
        description=payload.description,
        image_url=str(payload.image_url),
    )
    db.add(pin)
    db.commit()
    db.refresh(pin)
    return pin


@app.get("/pins", response_model=list[PinOut])
def list_pins(db: Session = Depends(get_db), user_id: int = Depends(get_user_id)):
    return db.query(Pin).filter(Pin.user_id == user_id).order_by(Pin.id.desc()).all()
