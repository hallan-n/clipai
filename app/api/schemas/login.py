from datetime import datetime
from pydantic import BaseModel, EmailStr


class CreateLocalLoginRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    avatar_url: str


class CreateLocalLoginResponse(BaseModel):
    public_id: str
    email: EmailStr
    name: str
    password: str
    avatar_url: str
    created_at: datetime
    updated_at: datetime


class LocalLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str
