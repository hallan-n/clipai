import re

from api.schemas.source import RemoveSourceResponse, SourceResponse
from api.security import decode_token
from api.utils import get_current_user
from crud.crud_source import SourceRepository
from db.models import Source
from fastapi import APIRouter, Depends, HTTPException
from services.youtube import fetch_channel_info

route = APIRouter(prefix="/source", tags=["Fontes"])
source_repo = SourceRepository()


@route.get(
    "",
    summary="Listar canais do YouTube",
    description="Lista todos os canais do YouTube adicionados como fontes para o usuário autenticado.",
    response_model=list[SourceResponse],
)
def get_all_sources(token: dict = Depends(decode_token)):
    current_user = get_current_user(token)
    sources = source_repo.select_all_by_login_id(current_user.id)

    if not sources:
        raise HTTPException(404, "Nenhum canal encontrado.")

    return [
        SourceResponse(
            custom_id=source.custom_id,
            name=source.name,
            subscribe=source.subscribe,
            thumbnail=source.thumbnail,
            avatar=source.avatar,
            url=source.url,
            custom_url=source.custom_url,
            last_video=source.last_video,
            created_at=source.created_at,
            updated_at=source.updated_at,
        )
        for source in sources
    ]


@route.post(
    "",
    summary="Adicionar canal do YouTube",
    description="Adiciona um canal do YouTube como fonte para o usuário autenticado.",
    response_model=SourceResponse,
)
def add_source(url: str, token: dict = Depends(decode_token)):

    if not url.startswith("https://www.youtube.com"):
        raise HTTPException(400, "URL inválida.")

    if not ("@" in url or "/channel/" in url):
        raise HTTPException(400, "URL inválida.")

    if not re.match(r"^https:\/\/www\.youtube\.com\/(@|channel\/).*$", url):
        raise HTTPException(400, "URL inválida.")

    current_user = get_current_user(token)

    if "@" in url:
        has_source = source_repo.select_by_custom_url_and_login_id(url, current_user.id)
    elif "/channel/" in url:
        has_source = source_repo.select_by_url_and_login_id(url, current_user.id)

    if has_source:
        raise HTTPException(409, "Canal já adicionado.")

    channel_data = fetch_channel_info(url)
    if not channel_data:
        raise HTTPException(404, "Canal não encontrado.")

    resp = source_repo.insert(
        Source(
            custom_id=channel_data["custom_id"],
            name=channel_data["name"],
            subscribe=channel_data["subscribe"],
            thumbnail=channel_data["thumbnail"],
            avatar=channel_data["avatar"],
            url=channel_data["url"],
            custom_url=channel_data["custom_url"],
            last_video=channel_data["last_video"],
            login_id=current_user.id,
        )
    )
    return SourceResponse(
        custom_id=resp.custom_id,
        name=resp.name,
        subscribe=resp.subscribe,
        thumbnail=resp.thumbnail,
        avatar=resp.avatar,
        url=resp.url,
        custom_url=resp.custom_url,
        last_video=resp.last_video,
        created_at=resp.created_at,
        updated_at=resp.updated_at,
    )


@route.delete(
    "",
    summary="Remover canal do YouTube",
    description="Remove um canal do YouTube como fonte para o usuário autenticado.",
    response_model=RemoveSourceResponse,
)
def remove_source(url: str, token: dict = Depends(decode_token)):
    if not url.startswith("https://www.youtube.com"):
        raise HTTPException(400, "URL inválida.")

    if not ("@" in url or "/channel/" in url):
        raise HTTPException(400, "URL inválida.")

    if not re.match(r"^https:\/\/www\.youtube\.com\/(@|channel\/).*$", url):
        raise HTTPException(400, "URL inválida.")

    current_user = get_current_user(token)

    if "@" in url:
        has_source = source_repo.select_by_custom_url_and_login_id(url, current_user.id)
    elif "/channel/" in url:
        has_source = source_repo.select_by_url_and_login_id(url, current_user.id)

    if not has_source:
        raise HTTPException(409, "Canal não encontrado.")

    source_repo.delete(has_source.id)

    return RemoveSourceResponse(success=True, detail="Canal removido com sucesso.")


@route.put(
    "",
    summary="Atualizar canal do YouTube",
    description="Atualiza um canal do YouTube como fonte para o usuário autenticado.",
    response_model=SourceResponse,
)
def update_source(url: str, token: dict = Depends(decode_token)):
    if not url.startswith("https://www.youtube.com"):
        raise HTTPException(400, "URL inválida.")

    if not ("@" in url or "/channel/" in url):
        raise HTTPException(400, "URL inválida.")

    if not re.match(r"^https:\/\/www\.youtube\.com\/(@|channel\/).*$", url):
        raise HTTPException(400, "URL inválida.")

    current_user = get_current_user(token)

    if "@" in url:
        has_source = source_repo.select_by_custom_url_and_login_id(url, current_user.id)
    elif "/channel/" in url:
        has_source = source_repo.select_by_url_and_login_id(url, current_user.id)

    if not has_source:
        raise HTTPException(409, "Canal não encontrado.")

    channel_data = fetch_channel_info(url)

    if not channel_data:
        raise HTTPException(404, "Canal não encontrado.")

    resp = source_repo.update(
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
            login_id=current_user.id,
        )
    )
    return SourceResponse(
        custom_id=resp.custom_id,
        name=resp.name,
        subscribe=resp.subscribe,
        thumbnail=resp.thumbnail,
        avatar=resp.avatar,
        url=resp.url,
        custom_url=resp.custom_url,
        last_video=resp.last_video,
        created_at=resp.created_at,
        updated_at=resp.updated_at,
    )


@route.put(
    "/all",
    summary="Atualiza todos os canais do YouTube",
    description="Atualiza todos os canais do YouTube como fontes para o usuário autenticado.",
    response_model=list[SourceResponse],
)
def update_all_sources(token: dict = Depends(decode_token)):
    current_user = get_current_user(token)
    sources = source_repo.select_all_by_login_id(current_user.id)

    if not sources:
        raise HTTPException(404, "Nenhum canal encontrado.")

    updated_sources = []
    for source in sources:
        channel_data = fetch_channel_info(source.url)

        resp = source_repo.update(
            Source(
                id=source.id,
                custom_id=channel_data["custom_id"],
                name=channel_data["name"],
                subscribe=channel_data["subscribe"],
                thumbnail=channel_data["thumbnail"],
                avatar=channel_data["avatar"],
                url=channel_data["url"],
                custom_url=channel_data["custom_url"],
                last_video=channel_data["last_video"],
                login_id=current_user.id,
            )
        )
        updated_sources.append(
            SourceResponse(
                custom_id=resp.custom_id,
                name=resp.name,
                subscribe=resp.subscribe,
                thumbnail=resp.thumbnail,
                avatar=resp.avatar,
                url=resp.url,
                custom_url=resp.custom_url,
                last_video=resp.last_video,
                created_at=resp.created_at,
                updated_at=resp.updated_at,
            )
        )
    return updated_sources
