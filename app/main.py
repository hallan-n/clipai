from fastapi import FastAPI
import uvicorn

from api.routes.login import route as login
from api.routes.source import route as source

app = FastAPI()


app.include_router(login)
app.include_router(source)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
