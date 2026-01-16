from pydantic import BaseModel, EmailStr


class PostLogin(BaseModel):
    email: EmailStr
    password: str


class PutLogin(BaseModel):
    email: EmailStr
    password: str
