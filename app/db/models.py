from typing import List
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime


class Login(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    public_id: UUID = Field(
        default_factory=uuid4, index=True, unique=True, nullable=False
    )

    email: str = Field(index=True, unique=True)
    name: str | None = None
    password: str | None = None
    provider: str = Field(default="local")
    provider_id: str | None = None
    avatar_url: str | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )


# class Source(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     custom_id: str | None = None
#     name: str | None = None
#     subscribe: str | None = None
#     thumbnail: str | None = None
#     avatar: str | None = None
#     url: str | None = None
#     custom_url: str | None = None
#     last_video: str | None = None


# class Content(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     url: str | None = None
#     title: str | None = None
#     duration: str | None = None
#     likes: str | None = None
#     comments: str | None = None
#     thumbnail: str | None = None


# class Cut(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     title: str | None = None
#     start: str | None = None
#     end: str | None = None
#     total_duration: str | None = None
#     describe: str | None = None
