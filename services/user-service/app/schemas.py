from pydantic import BaseModel, Field, HttpUrl
from typing import Optional


class ProfileCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    bio: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None


class ProfileOut(BaseModel):
    id: int
    user_id: int
    username: str
    bio: Optional[str]
    avatar_url: Optional[str]

    class Config:
        from_attributes = True
