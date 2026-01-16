from infra.database import Connection
from infra.schemas import Channel


def insert_channel(channel: Channel):
    with Connection() as conn:
        conn.add(channel)
        conn.commit()
        conn.refresh(channel)
        return channel


def select_channel(id: int):
    with Connection() as conn:
        return conn.get(Channel, id)


def update_channel(channel: Channel):
    with Connection() as conn:
        existing = conn.get(Channel, channel.id)
        if existing:
            merged = conn.merge(channel)
            conn.commit()
            conn.refresh(merged)
            return merged


def delete_channel(id: int):
    with Connection() as conn:
        channel = conn.get(Channel, id)
        if channel:
            conn.delete(channel)
            conn.commit()
