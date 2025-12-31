from dotenv import load_dotenv
from os import environ


load_dotenv(override=True)

OPENAI_API_KEY=environ.get("OPENAI_API_KEY")
MONGO_CONN=environ.get("MONGO_CONN")