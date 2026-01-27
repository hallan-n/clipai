from datetime import datetime

from openai import BaseModel


class Cont(BaseModel):
    custom_id: str | None
    name: str | None
    subscribe: str | None
    thumbnail: str | None
    avatar: str | None
    url: str | None
    custom_url: str | None
    last_video: str | None

    created_at: datetime | None
    updated_at: datetime | None


class RemoveSourceResponse(BaseModel):
    success: bool | None
    detail: str | None
