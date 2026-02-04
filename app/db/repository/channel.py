from sqlalchemy import select, or_
from sqlalchemy.orm import Session, selectinload
from db.models import Channel


class ChannelRepository:
    def insert(self, session: Session, channel: Channel) -> Channel:
        session.add(channel)
        session.flush()  # gera ID antes do commit
        session.refresh(channel)
        return channel

    def update(self, session: Session, channel: Channel) -> Channel | None:
        existing = session.get(Channel, channel.id)
        if existing:
            merged = session.merge(channel)
            session.commit()
            session.refresh(merged)
            return merged
        return None


    def select_by_login_id_with_source(
        self, session: Session, login_id: int
    ) -> list[Channel]:
        stmt = (
            select(Channel)
            .options(selectinload(Channel.sources))
            .where(Channel.login_id == login_id)
        )

        return session.execute(stmt).scalars().all()


    def select_all_by_login_id(self, session: Session, login_id: int) -> list[Channel]:
        stmt = select(Channel).where(Channel.login_id == login_id)
        return session.execute(stmt).scalars().all()


    def select_by_id_and_login_id(
        self, session: Session, login_id: int, channel_id: int
    ) -> Channel | None:
        stmt = select(Channel).where(Channel.id == channel_id, Channel.login_id == login_id)

        return session.execute(stmt).scalars().first()

    def select_by_id_and_login_id_with_source(
        self, session: Session, login_id: int, channel_id: int
    ) -> Channel | None:
        stmt = (
            select(Channel)
            .options(selectinload(Channel.sources))  # carrega os sources
            .where(Channel.id == channel_id, Channel.login_id == login_id)
        )

        result = session.execute(stmt).scalars().first()
        return result
    
    def select_by_url_and_login_id(self, session: Session, url: str, login_id: int) -> Channel:
        stmt = select(Channel).where(
            or_(
                Channel.url == url,
                Channel.custom_url == url
            ),
            Channel.login_id == login_id
        )

        result = session.execute(stmt).scalars().first()
        return result