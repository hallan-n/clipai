from os import environ

from dotenv import load_dotenv

load_dotenv(override=True)


import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
OPENAI_API_KEY = environ.get("OPENAI_API_KEY")
MONGO_CONN = environ.get("MONGO_CONN")
CLIENT_ID = environ.get("CLIENT_ID")
CLIENT_SECRET = environ.get("CLIENT_SECRET")
SECRET_KEY = environ.get("SECRET_KEY")
ALGORITHM = environ.get("ALGORITHM")
EXPIRE = environ.get("EXPIRE")
