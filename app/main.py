import uvicorn
from api.routes.login import route as login
from api.routes.source import route as source
from api.routes.content import route as content

from fastapi import FastAPI

app = FastAPI()


app.include_router(login)
app.include_router(source)
app.include_router(content)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
