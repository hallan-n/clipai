from typing import List

from sqlmodel import Field, Relationship, SQLModel


class Login(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    password: str

    channel: List["Channel"] = Relationship(back_populates="login")


class Channel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    login: str
    password: str
    channel_url: str
    channel_name: str
    subscribes: str
    create_at: str
    update_at: str
    last_published: str

    login_id: int = Field(foreign_key="login.id")
    login: "Login" = Relationship(back_populates="channel")
    sources: List["Source"] = Relationship(back_populates="channel")


class Source(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    login: str
    password: str
    source_url: str
    source_name: str
    has_new_content: str

    channel_id: int = Field(foreign_key="channel.id")
    channel: "Channel" = Relationship(back_populates="sources")
    contents: List["Content"] = Relationship(back_populates="source")


class Content(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str
    title: str
    duration: str

    source_id: int = Field(foreign_key="source.id")
    source: "Source" = Relationship(back_populates="contents")
    cuts: List["Cut"] = Relationship(back_populates="content")


class Cut(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    duration: str
    describe: str

    content_id: int = Field(foreign_key="content.id")
    content: "Content" = Relationship(back_populates="cuts")
