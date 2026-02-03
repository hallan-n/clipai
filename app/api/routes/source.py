import re

from api.schemas.source import RemoveSourceResponse, SourceRequest, SourceResponse
from api.security import decode_token
from api.utils import get_current_user
from crud.crud_source import SourceRepository
from crud.crud_channel import ChannelRepository
from db.models import Source
from fastapi import APIRouter, Depends, HTTPException
from services.youtube import fetch_channel_info

route = APIRouter(prefix="/source", tags=["Fontes"])
source_repo = SourceRepository()
channel_repo = ChannelRepository()



@route.get(
    "",
    summary="Selecionar uma ou mais fontes.",
    description="Selecionar uma ou mais fontes o usuário autenticado.",
    response_model=Source | list[Source],
)
def get_source(id: int = None, token: dict = Depends(decode_token)):
    current_user = get_current_user(token)
    if id:
        resp = source_repo.select_by_id_and_login_id(id, current_user.id)
    else:
        resp = source_repo.select_all_by_login_id(current_user.id)

    if not resp:
        raise HTTPException(404, "Nenhum canal encontrado.")

    return resp


@route.post(
    "",
    summary="Adicionar canal do YouTube",
    description="Adiciona um canal do YouTube como fonte para o usuário autenticado.",
    response_model=Source,
)
def add_source(source: SourceRequest, token: dict = Depends(decode_token)):
    if not source.url.startswith("https://www.youtube.com"):
        raise HTTPException(400, "URL inválida.")

    if not ("@" in source.url or "/channel/" in source.url):
        raise HTTPException(400, "URL inválida.")

    if not re.match(r"^https:\/\/www\.youtube\.com\/(@|channel\/).*$", source.url):
        raise HTTPException(400, "URL inválida.")

    current_user = get_current_user(token)
    
    current_channel = channel_repo.select_by_id_and_login_id(source.channel_id, current_user.id)
    if not current_channel:
        raise HTTPException(404, "Canal não encontrado")


    if "@" in source.url:
        has_source = source_repo.select_by_custom_url_and_login_id(
            source.url, current_user.id
        )
    elif "/channel/" in source.url:
        has_source = source_repo.select_by_url_and_login_id(source.url, current_user.id)

    if has_source:
        raise HTTPException(409, "Canal já adicionado.")

    channel_data = fetch_channel_info(source.url)
    if not channel_data:
        raise HTTPException(404, "Canal não encontrado.")

    return source_repo.insert(
        Source(
            custom_id=channel_data["custom_id"],
            name=channel_data["name"],
            subscribe=channel_data["subscribe"],
            thumbnail=channel_data["thumbnail"],
            avatar=channel_data["avatar"],
            url=channel_data["url"],
            custom_url=channel_data["custom_url"],
            last_video=channel_data["last_video"],
            content_focus=source.content_focus,
            content_format=source.content_format,
            upload_frequency=source.upload_frequency,
            
            channel_id=current_channel.id,
        )
    )


@route.delete(
    "",
    summary="Remover canal do YouTube",
    description="Remove um canal do YouTube como fonte para o usuário autenticado.",
    response_model=RemoveSourceResponse,
)
def remove_source(id: int, token: dict = Depends(decode_token)):
    current_user = get_current_user(token)
    has_source = source_repo.select_by_id_and_login_id(id, current_user.id)

    if not has_source:
        raise HTTPException(409, "Canal não encontrado.")
    
    source_repo.delete(has_source.id)

    return RemoveSourceResponse(success=True, detail="Canal removido com sucesso.")


@route.put(
    "",
    summary="Atualizar canal do YouTube",
    description="Atualiza um canal do YouTube como fonte para o usuário autenticado.",
    response_model=Source
)
def update_source(source: SourceRequest, token: dict = Depends(decode_token)):
    if not source.url.startswith("https://www.youtube.com"):
        raise HTTPException(400, "URL inválida.")

    if not ("@" in source.url or "/channel/" in source.url):
        raise HTTPException(400, "URL inválida.")

    if not re.match(r"^https:\/\/www\.youtube\.com\/(@|channel\/).*$", source.url):
        raise HTTPException(400, "URL inválida.")

    current_user = get_current_user(token)
    
    current_channel = channel_repo.select_by_id_and_login_id(source.channel_id, current_user.id)
    if not current_channel:
        raise HTTPException(404, "Canal não encontrado")


    if "@" in source.url:
        has_source = source_repo.select_by_custom_url_and_login_id(
            source.url, current_user.id
        )
    elif "/channel/" in source.url:
        has_source = source_repo.select_by_url_and_login_id(source.url, current_user.id)

    if not has_source:
        raise HTTPException(404, "Fonte não encontrado.")

    channel_data = fetch_channel_info(source.url)
    if not channel_data:
        raise HTTPException(404, "Fonte não encontrado.")

    return source_repo.update(
        Source(
            id=has_source.id,
            custom_id=channel_data["custom_id"],
            name=channel_data["name"],
            subscribe=channel_data["subscribe"],
            thumbnail=channel_data["thumbnail"],
            avatar=channel_data["avatar"],
            url=channel_data["url"],
            custom_url=channel_data["custom_url"],
            last_video=channel_data["last_video"],
            content_focus=source.content_focus,
            content_format=source.content_format,
            upload_frequency=source.upload_frequency,
            
            channel_id=current_channel.id,
        )
    )
