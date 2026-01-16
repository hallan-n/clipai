from pydantic import BaseModel, EmailStr


class Login(BaseModel):
    id: int
    email: EmailStr
    password: str


class PostLogin(BaseModel):
    email: EmailStr
    password: str


class PutLogin(BaseModel):
    email: EmailStr
    password: str


class Session(BaseModel):
    state: dict
    cookies: dict
    local_storage: dict
    session_storage: dict
    expire_at: str
    login_id: int
