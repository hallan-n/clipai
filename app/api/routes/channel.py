import re

from api.schemas.channel import GetChannelResponse, GetChannelResponseWSource, RemoveChannelResponse
from api.security import decode_token
from api.utils import get_current_user
from crud.crud_channel import ChannelRepository
from db.models import Channel
from fastapi import APIRouter, Depends, HTTPException
from services.youtube import fetch_channel_info

route = APIRouter(prefix="/channel", tags=["Canais"])
channel_repo = ChannelRepository()


@route.get(
    "",
    summary="Consulta um ou mais canais",
    description="Consulta um ou mais canais para o usuário autenticado.",
    response_model=list[GetChannelResponse] | list[GetChannelResponseWSource],
)
def get_channel(id: int = None, source: bool = None, token: dict = Depends(decode_token)):
    current_user = get_current_user(token)
    breakpoint()
    return channel_repo.select_all_by_login_id_with_sources(current_user.id)
    if not id and not source:
        return channel_repo.select_all_by_login_id(current_user.id)
        # "todos os channels"
    if not id and source:
        return channel_repo.select_all_by_login_id_with_sources(current_user.id)
        "todos os channels com todos os sources"
    if id and not source:
        "apenas o channel do id"
    if id and source:
        "apenas o channel do id com source"
    

    # if id and source:
        # return channel_repo.select_all_by_login_id_with_sources(current_user.id)
    # elif id and not source:
    #     resp = channel_repo.select_by_id_and_login_id(id, current_user.id)
    # else:
    #     resp = channel_repo.select_all_by_login_id(current_user.id)

    # if not resp:
    #     raise HTTPException(404, "Canal não encontrado.")

    # return resp


@route.post(
    "",
    summary="Adiciona um canal",
    description="Adiciona um canal para o usuário autenticado.",
)
def add_channel(url: str, token: dict = Depends(decode_token)):
    if not url.startswith("https://www.youtube.com"):
        raise HTTPException(400, "URL inválida.")

    if not ("@" in url or "/channel/" in url):
        raise HTTPException(400, "URL inválida.")

    if not re.match(r"^https:\/\/www\.youtube\.com\/(@|channel\/).*$", url):
        raise HTTPException(400, "URL inválida.")

    current_user = get_current_user(token)

    if "@" in url:
        has_channel = channel_repo.select_by_custom_url_and_login_id(
            url, current_user.id
        )
    elif "/channel/" in url:
        has_channel = channel_repo.select_by_url_and_login_id(url, current_user.id)

    if has_channel:
        raise HTTPException(409, "Canal já adicionado.")

    channel_data = fetch_channel_info(url)

    if not channel_data:
        raise HTTPException(404, "Canal não encontrado.")
    resp = channel_repo.insert(
        Channel(
            custom_id=channel_data["custom_id"],
            name=channel_data["name"],
            subscribe=channel_data["subscribe"],
            thumbnail=channel_data["thumbnail"],
            avatar=channel_data["avatar"],
            url=channel_data["url"],
            custom_url=channel_data["custom_url"],
            login_id=current_user.id,
        )
    )

    return resp


@route.put(
    "",
    summary="Atualiza infomações de um canal",
    description="Atualiza infomações de um canal para o usuário autenticado.",
    response_model=Channel,
)
def update_channel(id: int, token: dict = Depends(decode_token)):
    current_user = get_current_user(token)
    has_channel = channel_repo.select_by_id_and_login_id(id, current_user.id)

    if not has_channel:
        raise HTTPException(404, "Canal não encontrado.")

    channel_data = fetch_channel_info(has_channel.url)

    if not channel_data:
        raise HTTPException(404, "Canal não encontrado.")

    resp = channel_repo.update(
        Channel(
            id=has_channel.id,
            custom_id=channel_data["custom_id"],
            name=channel_data["name"],
            subscribe=channel_data["subscribe"],
            thumbnail=channel_data["thumbnail"],
            avatar=channel_data["avatar"],
            url=channel_data["url"],
            custom_url=channel_data["custom_url"],
            login_id=current_user.id,
        )
    )

    return resp


@route.put(
    "/all",
    summary="Atualiza infomações de todos os canais",
    description="Atualiza infomações de todos os canais para o usuário autenticado.",
    response_model=list[Channel],
)
def update_all_channels(token: dict = Depends(decode_token)):
    current_user = get_current_user(token)
    channels = channel_repo.select_all_by_login_id(current_user.id)

    if not channels:
        raise HTTPException(404, "Nenhum canal encontrado.")

    response_channels = []
    for channel in channels:
        channel_data = fetch_channel_info(channel.url)
        if not channel_data:
            continue

        resp = channel_repo.update(
            Channel(
                id=channel.id,
                custom_id=channel_data["custom_id"],
                name=channel_data["name"],
                subscribe=channel_data["subscribe"],
                thumbnail=channel_data["thumbnail"],
                avatar=channel_data["avatar"],
                url=channel_data["url"],
                custom_url=channel_data["custom_url"],
                login_id=current_user.id,
            )
        )
        response_channels.append(resp)
    return response_channels


@route.delete(
    "",
    summary="Exclui um canal",
    description="Exclui um canal para o usuário autenticado.",
    response_model=RemoveChannelResponse,
)
def remove_channel(id: int, token: dict = Depends(decode_token)):
    current_user = get_current_user(token)
    has_channel = channel_repo.select_by_id_and_login_id(id, current_user.id)

    if not has_channel:
        raise HTTPException(404, "Canal não encontrado.")
    try:
        channel_repo.delete(id)
        return RemoveChannelResponse(success=True, detail="Canal excluído com sucesso.")
    except:
        return RemoveChannelResponse(success=True, detail="Erro ao excluir canal.")
