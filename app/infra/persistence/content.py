from infra.database import Connection
from infra.schemas import Content


def create_content(content: Content):
    with Connection() as conn:
        conn.add(content)
        conn.commit()
        conn.refresh(content)
        return content


def get_content(id: int):
    with Connection() as conn:
        return conn.get(Content, id)


def update_content(content: Content):
    with Connection() as conn:
        existing = conn.get(Content, content.id)
        if existing:
            merged = conn.merge(content)
            conn.commit()
            conn.refresh(merged)
            return merged


def delete_content(id: int):
    with Connection() as conn:
        content = conn.get(Content, id)
        if content:
            conn.delete(content)
            conn.commit()
