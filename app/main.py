from fastapi import FastAPI
import uvicorn

from api.routes.login import route as login

app = FastAPI()


app.include_router(login)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
