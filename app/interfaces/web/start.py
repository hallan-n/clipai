from fastapi import FastAPI
from nicegui import ui
import interfaces.web.pages

def init(fastapi_app: FastAPI) -> None:
    ui.run_with(
        fastapi_app,
        mount_path="/",
        title="ClipAI",
        language='pt-BR',
    )