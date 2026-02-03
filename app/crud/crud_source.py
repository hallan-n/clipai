from db.database import Connection
from db.models import Source, Channel


class SourceRepository:
    def insert(self, source: Source) -> Source:
        with Connection() as conn:
            conn.add(source)
            conn.commit()
            conn.refresh(source)
            return source

    def select_by_id(self, id: int) -> Source:
        with Connection() as conn:
            return conn.get(Source, id)

    def select_by_url(self, url: str) -> Source:
        with Connection() as conn:
            return conn.query(Source).filter(Source.url == url).first()

    def select_all_by_channel_id(self, channel_id: int) -> list[Source]:
        with Connection() as conn:
            return conn.query(Source).filter(Source.channel_id == channel_id).all()

    def select_all_by_login_id(self, login_id: int) -> list[Source]:
        with Connection() as conn:
            return (
                conn.query(Source)
                .join(Channel)
                .filter(Channel.login_id == login_id)
                .all()
            )

    def select_by_id_and_login_id(
        self, source_id: int, login_id: int
    ) -> Source | None:
        with Connection() as conn:
            return (
                conn.query(Source)
                .join(Channel)
                .filter(
                    Source.id == source_id,
                    Channel.login_id == login_id,
                )
                .first()
            )


    def select_all(self) -> list[Source]:
        with Connection() as conn:
            return conn.query(Source).all()

    def select_by_url_and_login_id(self, url: str, login_id: int) -> Source:
        with Connection() as conn:
            return (
                conn.query(Source)
                .filter(Source.url == url, Source.login_id == login_id)
                .first()
            )

    def select_by_custom_url_and_login_id(
        self, custom_url: str, login_id: int
    ) -> Source | None:
        with Connection() as conn:
            return (
                conn.query(Source)
                .join(Channel)
                .filter(
                    Source.custom_url == custom_url,
                    Channel.login_id == login_id,
                )
                .first()
            )

    def update(self, source: Source) -> Source:
        with Connection() as conn:
            existing = conn.get(Source, source.id)
            if existing:
                merged = conn.merge(source)
                conn.commit()
                conn.refresh(merged)
                return merged

    def delete(self, id: int) -> None:
        with Connection() as conn:
            source = conn.get(Source, id)
            if source:
                conn.delete(source)
                conn.commit()
