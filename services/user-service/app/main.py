from fastapi import FastAPI, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.config import settings
from app.database import Base, engine, SessionLocal
from app.models import UserProfile
from app.schemas import ProfileCreate, ProfileOut

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
    try:
        return int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="X-User-Id must be an integer")


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.service_name}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.post("/profiles/me", response_model=ProfileOut)
def create_or_update_my_profile(
    payload: ProfileCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    if profile is None:
        profile = UserProfile(
            user_id=user_id,
            username=payload.username,
            bio=payload.bio,
            avatar_url=str(payload.avatar_url) if payload.avatar_url else None,
        )
        db.add(profile)
    else:
        profile.username = payload.username
        profile.bio = payload.bio
        profile.avatar_url = str(payload.avatar_url) if payload.avatar_url else None

    db.commit()
    db.refresh(profile)
    return profile


@app.get("/profiles/{user_id}", response_model=ProfileOut)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
