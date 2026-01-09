from pydantic import BaseModel, Field, HttpUrl
from typing import Optional


class PinCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    image_url: HttpUrl


class PinOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    image_url: str

    class Config:
        from_attributes = True
