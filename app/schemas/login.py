from datetime import datetime

from pydantic import BaseModel, EmailStr, UUID4

class CreateLocalLoginRequest(BaseModel):
    email: EmailStr
    name: str
    password: str | None = None
    avatar_url: str

class CreateLocalLoginResponse(BaseModel):
    id: int
    public_id: UUID4
    email: EmailStr
    name: str
    provider: str
    avatar_url: str
    created_at: datetime
    updated_at: datetime

class LocalLoginRequest(BaseModel):
    email: EmailStr
    password: str


 
class LoginDTO(BaseModel):
    id: int | None = None
    public_id: UUID4 | None = None
    email: EmailStr | None = None
    name: str | None = None
    password: str | None = None
    provider: str | None = None
    provider_id: str | None = None
    avatar_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None




# class LocalLoginRequest(BaseModel):
#     email: EmailStr
#     password: str


# class CreateLocalLoginRequest(BaseModel):
#     email: EmailStr
#     name: str
#     password: str | None = None
#     avatar_url: str




# class CreateLoginResponse(BaseModel):
#     id: int
#     public_id: UUID4
#     email: EmailStr
#     name: str
#     avatar_url: str
#     created_at: datetime
#     updated_at: datetime

class AccessToken(BaseModel):
    access_token: str
    token_type: str
