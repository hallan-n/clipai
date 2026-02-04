from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Login(Base):
    __tablename__ = "login"

    id: Mapped[int] = mapped_column(primary_key=True)

    public_id: Mapped[UUID] = mapped_column(
        sa.Uuid, default=uuid4, unique=True, index=True, nullable=False
    )

    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[Optional[str]]
    password: Mapped[Optional[str]]
    provider: Mapped[str] = mapped_column(default="local")
    provider_id: Mapped[Optional[str]]
    avatar_url: Mapped[Optional[str]]

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    channels: Mapped[List["Channel"]] = relationship(
        back_populates="login", cascade="all, delete-orphan"
    )


class Channel(Base):
    __tablename__ = "channel"

    id: Mapped[int] = mapped_column(primary_key=True)

    custom_id: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
    subscribe: Mapped[Optional[str]]
    thumbnail: Mapped[Optional[str]]
    avatar: Mapped[Optional[str]]
    url: Mapped[Optional[str]]
    custom_url: Mapped[Optional[str]]

    login_id: Mapped[int] = mapped_column(ForeignKey("login.id"), nullable=False)

    login: Mapped["Login"] = relationship(back_populates="channels")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    sources: Mapped[List["Source"]] = relationship(
        back_populates="channel", cascade="all, delete-orphan"
    )


class Source(Base):
    __tablename__ = "source"

    id: Mapped[int] = mapped_column(primary_key=True)

    custom_id: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
    subscribe: Mapped[Optional[str]]
    thumbnail: Mapped[Optional[str]]
    avatar: Mapped[Optional[str]]
    url: Mapped[Optional[str]]
    custom_url: Mapped[Optional[str]]
    last_video: Mapped[Optional[str]]
    content_focus: Mapped[Optional[str]]
    content_format: Mapped[Optional[str]]
    upload_frequency: Mapped[Optional[str]]

    channel_id: Mapped[int] = mapped_column(ForeignKey("channel.id"), nullable=False)

    channel: Mapped["Channel"] = relationship(back_populates="sources")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    contents: Mapped[List["Content"]] = relationship(
        back_populates="source", cascade="all, delete-orphan"
    )


class Content(Base):
    __tablename__ = "content"

    id: Mapped[int] = mapped_column(primary_key=True)

    url: Mapped[Optional[str]]
    title: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    published_at: Mapped[Optional[datetime]]
    thumbnail: Mapped[Optional[str]]
    duration: Mapped[Optional[int]]

    source_id: Mapped[int] = mapped_column(ForeignKey("source.id"), nullable=False)

    source: Mapped["Source"] = relationship(back_populates="contents")

    cuts: Mapped[List["Cut"]] = relationship(
        back_populates="content", cascade="all, delete-orphan"
    )


class Cut(Base):
    __tablename__ = "cut"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[Optional[str]]
    start: Mapped[Optional[str]]
    end: Mapped[Optional[str]]
    total_duration: Mapped[Optional[str]]
    describe: Mapped[Optional[str]]

    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"), nullable=False)

    content: Mapped["Content"] = relationship(back_populates="cuts")
