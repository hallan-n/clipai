from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


def setup_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def error_handler_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException:
            raise
        except Exception:
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )
