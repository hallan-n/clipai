import re

from api.schemas.content import Content, GetContentsResponse
from api.schemas.source import SourceResponse
from api.security import decode_token
from api.utils import get_current_user
from crud.crud_content import ContentRepository
from crud.crud_source import SourceRepository
from fastapi import APIRouter, Depends, HTTPException
from services.youtube import fetch_transcribe, fetch_video_info, fetch_video_infos

route = APIRouter(prefix="/content", tags=["Conteúdos"])
content_repo = ContentRepository()
source_repo = SourceRepository()


@route.get(
    "",
    summary="Listar os conteúdos dos canais do YouTube",
    description="Lista todos os conteúdos dos canais do YouTube adicionados como fontes para o usuário autenticado.",
    response_model=GetContentsResponse | list[GetContentsResponse],
)
def get_contents(
    source_id: int = None, content_limit: int = 5, token: dict = Depends(decode_token)
):
    current_user = get_current_user(token)
    if source_id:
        source = source_repo.select_by_id(source_id)
        if not source or source.login_id != current_user.id:
            raise HTTPException(404, "Canal não encontrado.")

        video_infos = fetch_video_infos(source.url.split("/")[-1], content_limit)
        return GetContentsResponse(
            source=SourceResponse(**source.model_dump()),
            contents=[Content(**video_info) for video_info in video_infos],
        )

    sources = source_repo.select_all_by_login_id(current_user.id)

    if not sources:
        raise HTTPException(404, "Nenhum canal encontrado.")
    videos = []
    for source in sources:
        video_infos = fetch_video_infos(source.url.split("/")[-1], content_limit)
        videos.append(
            GetContentsResponse(
                source=SourceResponse(**source.model_dump()),
                contents=[Content(**video_info) for video_info in video_infos],
            )
        )

    return videos


@route.get(
    "/process",
    summary="Processa um vídeo do YouTube",
    description="Processa um vídeo do YouTube e retorna as informações do conteúdo.",
)
def process_content(video_url: str, token: dict = Depends(decode_token)):
    if not video_url.startswith("https://www.youtube.com"):
        raise HTTPException(400, "URL inválida.")

    if not "watch?v" in video_url:
        raise HTTPException(400, "URL inválida.")

    if not re.match(r"^^https:\/\/www\.youtube\.com\/watch\?v=.*$", video_url):
        raise HTTPException(400, "URL inválida.")

    current_user = get_current_user(token)

    # Aqui faz select nos cuts e retorna ao invez do erro
    is_processed = content_repo.select_by_url_and_login_id(video_url, current_user.id)
    if is_processed:
        raise HTTPException(400, "Vídeo já processado.")

    video_info = fetch_video_info(video_url)

    transcribe = fetch_transcribe(video_info["video_id"])
