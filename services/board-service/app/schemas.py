from pydantic import BaseModel, Field
from typing import Optional


class BoardCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class BoardOut(BaseModel):
    id: int
    user_id: int
    name: str

    class Config:
        from_attributes = True
