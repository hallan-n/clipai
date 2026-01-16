from infra.database import Connection
from infra.models import Source


def create_source(source: Source):
    with Connection() as conn:
        conn.add(source)
        conn.commit()
        conn.refresh(source)
        return source


def get_source(id: int):
    with Connection() as conn:
        return conn.get(Source, id)


def update_source(source: Source):
    with Connection() as conn:
        existing = conn.get(Source, source.id)
        if existing:
            merged = conn.merge(source)
            conn.commit()
            conn.refresh(merged)
            return merged


def delete_source(id: int):
    with Connection() as conn:
        source = conn.get(Source, id)
        if source:
            conn.delete(source)
            conn.commit()
