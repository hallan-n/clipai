import re

from api.security import decode_token
from api.utils import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from crud.crud_content import ContentRepository
from crud.crud_source import SourceRepository
from services.youtube import fetch_video_infos

route = APIRouter(prefix="/content", tags=["Conteúdos"])
content_repo = ContentRepository()
source_repo = SourceRepository()

@route.get(
    "",
    summary="Listar canais do YouTube",
    description="Lista todos os canais do YouTube adicionados como fontes para o usuário autenticado."
    # response_model=list[SourceResponse],
)
def get_all_contents(token: dict = Depends(decode_token)):
    current_user = get_current_user(token)
    sources = source_repo.select_all_by_login_id(current_user.id)

    if not sources:
        raise HTTPException(404, "Nenhum canal encontrado.")
    videos = []
    for source in sources:
        video_infos = fetch_video_infos(source.url.split("/")[-1], 5)
        videos.append(video_infos)

    return videos
        # Process video_infos as needed