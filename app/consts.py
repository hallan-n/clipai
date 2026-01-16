from dotenv import load_dotenv
from os import environ

load_dotenv(override=True)


import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
OPENAI_API_KEY=environ.get("OPENAI_API_KEY")
MONGO_CONN=environ.get("MONGO_CONN")