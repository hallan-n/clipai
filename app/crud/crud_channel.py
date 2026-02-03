from sqlmodel import select
from sqlalchemy.orm import selectinload

from db.database import Connection
from db.models import Channel


class ChannelRepository:
    def insert(self, channel: Channel) -> Channel:
        with Connection() as conn:
            conn.add(channel)
            conn.commit()
            conn.refresh(channel)
            return channel
        

    def select_by_url(self, url: str) -> Channel:
        with Connection() as conn:
            return conn.query(Channel).filter(Channel.url == url).first()
        

    def select_by_custom_url(self, custom_url: str) -> Channel:
        with Connection() as conn:
            return conn.query(Channel).filter(Channel.custom_url == custom_url).first()

    def select_all_by_login_id(self, login_id: int) -> list[Channel]:
        with Connection() as conn:
            return conn.query(Channel).filter(Channel.login_id == login_id).all()

    def select_by_custom_url_and_login_id(
        self, custom_url: str, login_id: int
    ) -> Channel:
        with Connection() as conn:
            return (
                conn.query(Channel)
                .filter(Channel.custom_url == custom_url, Channel.login_id == login_id)
                .first()
            )
    def select_by_id_and_login_id(self, id: str, login_id: int) -> Channel:
        with Connection() as conn:
            return (
                conn.query(Channel)
                .filter(Channel.id == id, Channel.login_id == login_id)
                .first()
            )
        

    # def select_by_id_and_login_id_w_all_sources(self, id: str, login_id: int) -> Channel:
    #     with Connection() as conn:
    #         return (
    #             conn.query(Channel)
    #             .options(joinedload(Channel.sources)) # Carrega os sources junto
    #             .filter(Channel.id == id, Channel.login_id == login_id)
    #             .first()
    #         )
        
    def select_all_by_login_id_with_sources(self, login_id: int) -> list[Channel]:
        with Connection() as conn:
            stmt = (
                select(Channel)
                .where(Channel.login_id == login_id)
                .options(selectinload(Channel.sources))
            )

            return conn.exec(stmt).all()
        

    def select_by_url_and_login_id(
        self, url: str, login_id: int
    ) -> Channel:
        with Connection() as conn:
            return (
                conn.query(Channel)
                .filter(Channel.url == url, Channel.login_id == login_id)
                .first()
            )



    def select_by_id(self, id: int) -> Channel:
        with Connection() as conn:
            return conn.get(Channel, id)

    def update(self, channel: Channel) -> Channel:
        with Connection() as conn:
            existing = conn.get(Channel, channel.id)
            if existing:
                merged = conn.merge(channel)
                conn.commit()
                conn.refresh(merged)
                return merged

    def delete(self, id: int) -> None:
        with Connection() as conn:
            channel = conn.get(Channel, id)
            if channel:
                conn.delete(channel)
                conn.commit()
