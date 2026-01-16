from datetime import datetime, timedelta
import bcrypt
from jose import jwt
from fastapi import Header

SECRET_KEY = "2aOBIPoNcdlKv3pj6zZ6Rvj_cW7pb-78eTk48zDN6Sg"
ALGORITHM = "HS256"
EXPIRE = 30


def hashed(password: str):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hash.decode("utf-8")


def check_hash(hashed: str, password: str):
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=EXPIRE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str = Header(...)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload