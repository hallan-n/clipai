from os import environ

from dotenv import load_dotenv

load_dotenv(override=True)


OPENAI_API_KEY = environ.get("OPENAI_API_KEY")
YOUTUBE_API_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
YOUTUBE_API_CLIENT_SECRET_FILE = "client_secret.json"
YOUTUBE_API_TOKEN_FILE = "token.pkl"
