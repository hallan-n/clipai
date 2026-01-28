from db.database import Connection
from db.models import Content, Source


class ContentRepository:
    def insert(self, content: Content) -> Content:
        with Connection() as conn:
            conn.add(content)
            conn.commit()
            conn.refresh(content)
            return content

    def select_by_id(self, id: int) -> Content:
        with Connection() as conn:
            return conn.get(Content, id)

    def select_by_url_and_login_id(
        self, content_url: str, login_id: int
    ) -> Content | None:
        with Connection() as conn:
            return (
                conn.query(Content)
                .join(Source, Source.id == Content.source_id)
                .filter(
                    Content.url == content_url,
                    Source.login_id == login_id,
                )
                .first()
            )

    def select_all(self) -> list[Content]:
        with Connection() as conn:
            return conn.query(Content).all()

    def update(self, content: Content) -> Content:
        with Connection() as conn:
            existing = conn.get(Content, content.id)
            if existing:
                merged = conn.merge(content)
                conn.commit()
                conn.refresh(merged)
                return merged

    def delete(self, id: int) -> None:
        with Connection() as conn:
            content = conn.get(Content, id)
            if content:
                conn.delete(content)
                conn.commit()
