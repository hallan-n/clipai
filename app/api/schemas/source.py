from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class SourceRequest(BaseModel):
    url: str
    channel_id: int
    content_focus: str
    content_format: str
    upload_frequency: str


class SourceResponse(BaseModel):
    id: int | None
    custom_id: str | None
    name: str | None
    subscribe: str | None
    thumbnail: str | None
    avatar: str | None
    url: str | None
    custom_url: str | None
    last_video: str | None
    main_topics: str | None
    content_focus: str | None
    content_format: str | None
    target_audience: str | None
    upload_frequency: str | None
    viewer_benefit: str | None

    created_at: datetime | None
    updated_at: datetime | None


class RemoveSourceResponse(BaseModel):
    success: bool | None
    detail: str | None
