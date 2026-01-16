from infra.database import Connection
from infra.schemas import Cut


def insert_cut(cut: Cut):
    with Connection() as conn:
        conn.add(cut)
        conn.commit()
        conn.refresh(cut)
        return cut


def select_cut(id: int):
    with Connection() as conn:
        return conn.get(Cut, id)


def update_cut(cut: Cut):
    with Connection() as conn:
        existing = conn.get(Cut, cut.id)
        if existing:
            merged = conn.merge(cut)
            conn.commit()
            conn.refresh(merged)
            return merged


def delete_cut(id: int):
    with Connection() as conn:
        cut = conn.get(Cut, id)
        if cut:
            conn.delete(cut)
            conn.commit()
