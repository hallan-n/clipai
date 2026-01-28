from datetime import datetime

from api.schemas.source import SourceResponse
from pydantic import BaseModel


class Content(BaseModel):
    url: str | None
    title: str | None
    description: str | None
    published_at: datetime | None
    thumbnail: str | None
    duration: int | None


class GetContentsResponse(BaseModel):
    source: SourceResponse
    contents: list[Content]
