from datetime import datetime
from typing import List
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import DateTime, func
from sqlmodel import Field, Relationship, SQLModel


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

    created_at: datetime = Field(
        sa_column=sa.Column(
            DateTime,
            nullable=False,
            server_default=func.now(),
        )
    )

    updated_at: datetime = Field(
        sa_column=sa.Column(
            DateTime,
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        )
    )
    sources: List["Source"] = Relationship(
        back_populates="login", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class Source(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    custom_id: str | None = None
    name: str | None = None
    subscribe: str | None = None
    thumbnail: str | None = None
    avatar: str | None = None
    url: str | None = None
    custom_url: str | None = None
    last_video: str | None = None

    created_at: datetime = Field(
        sa_column=sa.Column(
            DateTime,
            nullable=False,
            server_default=func.now(),
        )
    )

    updated_at: datetime = Field(
        sa_column=sa.Column(
            DateTime,
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        )
    )

    login_id: int = Field(foreign_key="login.id", nullable=False)
    login: Login | None = Relationship(back_populates="sources")

    contents: List["Content"] = Relationship(
        back_populates="source",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

class Content(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str | None
    title: str | None
    description: str | None
    published_at: datetime | None
    thumbnail: str | None
    duration: int | None 

    source_id: int = Field(foreign_key="source.id", nullable=False)
    source: Source | None = Relationship(back_populates="contents")


# class Cut(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     title: str | None = None
#     start: str | None = None
#     end: str | None = None
#     total_duration: str | None = None
#     describe: str | None = None
