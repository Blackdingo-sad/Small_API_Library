from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=180)
    isbn: str = Field(min_length=10, max_length=20)
    published_year: int | None = Field(default=None, ge=0)
    total_copies: int = Field(default=1, ge=1)
    available_copies: int | None = Field(default=None, ge=0)


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    author: str | None = Field(default=None, min_length=1, max_length=180)
    isbn: str | None = Field(default=None, min_length=10, max_length=20)
    published_year: int | None = Field(default=None, ge=0)
    total_copies: int | None = Field(default=None, ge=1)
    available_copies: int | None = Field(default=None, ge=0)


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    published_year: int | None
    total_copies: int
    available_copies: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)