from fastapi import APIRouter, Depends, HTTPException
from api.security import decode_token
from api.schemas.source import AddChannelResponse, RemoveChannelResponse
from db.models import Source
from crud.crud_source import SourceRepository

route = APIRouter(prefix="/source", tags=["Fontes"])
source_repo = SourceRepository()



from api.utils import get_current_user
from services.youtube import fetch_channel_info, fetch_channel_id


@route.post(
    "",
    summary="Adicionar canal do YouTube",
    description="Adiciona um canal do YouTube como fonte para o usuário autenticado.",
    response_model=AddChannelResponse,
)
def add_channel(url: str, token: dict = Depends(decode_token)):
    if not url.startswith("https://www.youtube.com"):
        return HTTPException(400, "URL inválida.")
    
    if "@" not in url or "/channel/" in url:
        return HTTPException(400, "URL inválida.")

    current_user = get_current_user(token)

    channel_data = fetch_channel_info(url)
    if not channel_data:
        return HTTPException(404, "Canal não encontrado.")

    has_source = source_repo.select_by_url_and_login_id(channel_data["url"], current_user.id)

    if has_source:
        raise HTTPException(409, "Canal já adicionado.")
    
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
    return AddChannelResponse(
        custom_id=resp.custom_id,
        name=resp.name,
        subscribe=resp.subscribe,
        thumbnail=resp.thumbnail,
        avatar=resp.avatar,
        url=resp.url,
        custom_url=resp.custom_url,
        last_video=resp.last_video,
    
    )



@route.delete(
    "",
    summary="Remover canal do YouTube",
    description="Remove um canal do YouTube como fonte para o usuário autenticado.",
    response_model=RemoveChannelResponse,
)
def remove_channel(url: str, token: dict = Depends(decode_token)):
    if not url.startswith("https://www.youtube.com"):
        return HTTPException(400, "URL inválida.")
    
    if "@" not in url or "/channel/" in url:
        return HTTPException(400, "URL inválida.")

    current_user = get_current_user(token)

    channel_id = fetch_channel_id(url)
    channel_url = f"https://www.youtube.com/channel/{channel_id}"
    has_source = source_repo.select_by_url_and_login_id(channel_url, current_user.id)

    if not has_source:
        raise HTTPException(409, "Canal não encontrado.")
    
    source_repo.delete(has_source.id)
    
    return RemoveChannelResponse(
        success=True,
        detail="Canal removido com sucesso."
    )
    
