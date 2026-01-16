from infra.database import Connection
from infra.schemas import Login


def create_login(login: Login):
    with Connection() as conn:
        conn.add(login)
        conn.commit()
        conn.refresh(login)
        return login


def get_login(id: int):
    with Connection() as conn:
        return conn.get(Login, id)

def get_login_by_email(email: str):
    with Connection() as conn:
        return conn.query(Login).filter(Login.email == email).first()

def update_login(login: Login):
    with Connection() as conn:
        existing = conn.get(Login, login.id)
        if existing:
            merged = conn.merge(login)
            conn.commit()
            conn.refresh(merged)
            return merged


def delete_login(id: int):
    with Connection() as conn:
        login = conn.get(Login, id)
        if login:
            conn.delete(login)
            conn.commit()
