from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)

    username = Column(String(50), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    avatar_url = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
