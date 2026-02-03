from pydantic import BaseModel

class RemoveChannelResponse(BaseModel):
    success: bool | None
    detail: str | None



from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class GetSourceResponse(BaseModel):
    id: int
    custom_id: str
    name: str
    subscribe: str
    thumbnail: str
    avatar: str
    url: str
    custom_url: str
    last_video: str
    content_focus: str
    content_format: str
    upload_frequency: str
    channel_id: int
    created_at: datetime
    updated_at: datetime

class GetChannelResponse(BaseModel):
    id: int | None
    custom_id: str | None
    name: str | None
    subscribe: str | None
    thumbnail: str | None
    avatar: str | None
    url: str | None
    custom_url: str | None
    created_at: datetime
    updated_at: datetime
    login_id: int | None


class GetChannelResponseWSource(GetChannelResponse):
    sources: list[GetSourceResponse]
