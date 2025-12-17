from fastapi import FastAPI
from nicegui import ui
import interfaces.web.home

def init(fastapi_app: FastAPI) -> None:
    ui.run_with(
        fastapi_app,
        mount_path="/web",
        title="Casamento",
        language='pt-BR',
        favicon="app/web/assets/favicon.svg",
    )