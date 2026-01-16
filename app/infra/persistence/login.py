from infra.database import Connection
from infra.schemas import Login


def add(login: Login) -> Login:
    with Connection() as conn:
        conn.add(login)
        conn.commit()
        conn.refresh(login)
        return login


def get(id: int) -> Login:
    with Connection() as conn:
        return conn.get(Login, id)


def get_by_email(email: str) -> Login:
    with Connection() as conn:
        return conn.query(Login).filter(Login.email == email).first()


def update(login: Login) -> Login:
    with Connection() as conn:
        existing = conn.get(Login, login.id)
        if existing:
            merged = conn.merge(login)
            conn.commit()
            conn.refresh(merged)
            return merged


def delete(id: int):
    with Connection() as conn:
        login = conn.get(Login, id)
        if login:
            conn.delete(login)
            conn.commit()
