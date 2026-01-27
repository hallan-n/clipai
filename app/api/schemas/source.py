from openai import BaseModel


class AddChannelResponse(BaseModel):
    custom_id: str
    name: str
    subscribe: str
    thumbnail: str
    avatar: str
    url: str
    custom_url: str
    last_video: str


class RemoveChannelResponse(BaseModel):
    success: bool
    detail: str
