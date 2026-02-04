import uvicorn
from api.routes.login import route as login
from api.routes.channel import route as channel
from fastapi import FastAPI
from db.database import create_tables

create_tables()
app = FastAPI()


app.include_router(login)
app.include_router(channel)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


