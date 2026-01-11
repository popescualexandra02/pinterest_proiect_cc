from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    name = Column(String(200), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
