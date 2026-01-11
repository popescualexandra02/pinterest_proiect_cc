from sqlalchemy import Column, Integer, String, DateTime, func, UniqueConstraint
from app.database import Base

class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BoardPin(Base):
    __tablename__ = "board_pins"

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer, index=True, nullable=False)
    pin_id = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("board_id", "pin_id", name="uq_board_pin"),
    )
