from datetime import datetime
from pydantic import BaseModel, EmailStr

class PostLoginRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    avatar_url: str


class PostLoginResponse(BaseModel):
    public_id: str
    email: str
    name: str
    password: str
    avatar_url: str
    created_at: datetime
    updated_at: datetime

