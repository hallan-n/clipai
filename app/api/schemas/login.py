from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateLocalLoginRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    avatar_url: str


class CreateLocalLoginResponse(BaseModel):
    public_id: str | None
    email: EmailStr | None
    name: str | None
    password: str | None
    avatar_url: str | None
    created_at: datetime | None
    updated_at: datetime | None


class LocalLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str
