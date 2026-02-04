from api.security import decode_token
from usecase.channel import ChannelUsecase
from db.database import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.channel import AddChannelRequest, AddChannelResponse, GetChannelWSourceResponse
from api.utils import get_current_login

route = APIRouter(prefix="/channel", tags=["Canal"])
channel_service = ChannelUsecase()


@route.post("", response_model=AddChannelResponse)
def add_channel(channel_url: AddChannelRequest, session: Session = Depends(get_session), token: dict = Depends(decode_token)):
    login = get_current_login(session, token)
    return channel_service.add_channel(session, login, channel_url)

@route.put("", response_model=AddChannelResponse)
def update_channel(channel_url: AddChannelRequest, session: Session = Depends(get_session), token: dict = Depends(decode_token)):
    login = get_current_login(session, token)
    return channel_service.update_channel(session, login, channel_url)

@route.get("", response_model=GetChannelWSourceResponse | list[GetChannelWSourceResponse])
def get_channel(channel_id: int = None, session: Session = Depends(get_session), token: dict = Depends(decode_token)):
    login = get_current_login(session, token)
    return channel_service.get_channel(session, login, channel_id)

