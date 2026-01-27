from db.database import Connection
from db.models import Content


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
