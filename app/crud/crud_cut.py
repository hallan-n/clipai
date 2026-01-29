from db.database import Connection
from db.models import Cut


class CutRepository:
    def insert(self, cut: Cut) -> Cut:
        with Connection() as conn:
            conn.add(cut)
            conn.commit()
            conn.refresh(cut)
            return cut

    def select_by_id(self, id: int) -> Cut:
        with Connection() as conn:
            return conn.get(Cut, id)

    def select_all_by_content_id(self, content: int) -> list[Cut]:
        with Connection() as conn:
            return conn.query(Cut).filter(Cut.content_id == content).all()


    def update(self, cut: Cut) -> Cut:
        with Connection() as conn:
            existing = conn.get(Cut, cut.id)
            if existing:
                merged = conn.merge(cut)
                conn.commit()
                conn.refresh(merged)
                return merged

    def delete(self, id: int) -> None:
        with Connection() as conn:
            cut = conn.get(Cut, id)
            if cut:
                conn.delete(cut)
                conn.commit()
