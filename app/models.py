from pydantic import BaseModel, EmailStr

class PostLogin(BaseModel):
    email: EmailStr
    password: str

class PutLogin(BaseModel):
    id: int
    email: EmailStr
    password: str
