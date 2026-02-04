from sqlalchemy.orm import Session
from db.models import Channel, Login
from schemas.channel import AddChannelRequest
from db.repository.channel import ChannelRepository
from fastapi import HTTPException
from services.youtube import fetch_channel_info

channel_repo = ChannelRepository()


class ChannelUsecase:
    def add_channel(self, session: Session, login: Login, data: AddChannelRequest):
        has_channel = channel_repo.select_by_url_and_login_id(session, str(data.url), login.id)
        if has_channel:
            return has_channel
        
        channel_data = fetch_channel_info(str(data.url))

        channel = Channel(
            custom_id=channel_data["custom_id"],
            name=channel_data["name"],
            subscribe=channel_data["subscribe"],
            thumbnail=channel_data["thumbnail"],
            avatar=channel_data["avatar"],
            url=channel_data["url"],
            custom_url=channel_data["custom_url"],
            login_id=login.id
        )

        channel = channel_repo.insert(session, channel)
        session.commit()
        return channel
    

    def update_channel(self, session: Session, login: Login, data: AddChannelRequest):
        has_channel = channel_repo.select_by_url_and_login_id(session, str(data.url), login.id)
        if not has_channel:
            raise HTTPException(404, 'Canal não encontrado')
        
        channel_data = fetch_channel_info(str(data.url))

        channel = Channel(
            id=has_channel.id,
            custom_id=channel_data["custom_id"],
            name=channel_data["name"],
            subscribe=channel_data["subscribe"],
            thumbnail=channel_data["thumbnail"],
            avatar=channel_data["avatar"],
            url=channel_data["url"],
            custom_url=channel_data["custom_url"],
            login_id=login.id
        )

        channel = channel_repo.update(session, channel)
        session.commit()
        return channel
    


    def get_channel(
        self,
        session: Session,
        login: Login,
        channel_id: int | None = None,
    ):
        if channel_id:
            return channel_repo.select_by_id_and_login_id_with_source(session, login.id, channel_id)

        return channel_repo.select_by_login_id_with_source(session, login.id)
