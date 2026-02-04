from pydantic import BaseModel, ConfigDict, HttpUrl, validator
from datetime import datetime
import re


class AddChannelRequest(BaseModel):
    url: HttpUrl
    model_config = ConfigDict(from_attributes=True)

    @validator("url")
    def validate_youtube(cls, v):
        if not re.match(r"^https:\/\/www\.youtube\.com\/(@|channel\/).*$", str(v)):
            raise ValueError(400, "URL inválida.")
        return v
    


class AddChannelResponse(BaseModel):
    id: int
    custom_id: str | None
    name: str | None
    subscribe: str | int | None
    thumbnail: str | None
    avatar: str | None
    url: str | None
    custom_url: str | None
    login_id: int
    created_at: datetime | None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class GetSourceResponse(BaseModel):
    custom_id: str | None
    name: str | None
    subscribe: str | int | None
    thumbnail: str | None
    avatar: str | None
    url: str | None
    custom_url: str | None
    last_video: str | None
    content_focus: str | None
    content_format: str | None
    upload_frequency: str | None
    channel_id: int | None
    created_at: datetime | None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class GetChannelWSourceResponse(AddChannelResponse):
    sources: list[GetSourceResponse] = []

    model_config = ConfigDict(from_attributes=True)
