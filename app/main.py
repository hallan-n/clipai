from fastapi import FastAPI
from interfaces.web.start import init
from interfaces.api.trancrible import route

app = FastAPI()

app.include_router(route)
init(app)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)
