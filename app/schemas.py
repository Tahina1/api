from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, computed_field

from app.config import settings

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True) #read fields from ORM

    id: int
    email: EmailStr
    create_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class LinkCreate(BaseModel):
    target_url: HttpUrl
    slug: str | None = Field(default=None, pattern=SLUG_PATTERN)
    title: str | None = Field(default=None, max_length=200)

class LinkUpdate(BaseModel):
    target_url: HttpUrl | None = None
    title: str | None = Field(default=None, max_length=200)

class LinkOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    target_url: str
    title: str | None
    created_at: datetime
    clicks: int = 0

    @computed_field
    @property
    def short_url(self) -> str:
        return f"{settings.public_base_url}/r/{self.slug}"

class TopLink(BaseModel):
    slug: str
    clicks: int 