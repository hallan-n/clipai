
from db.models import Login
from db.database import Connection


class LoginRepository:
    def insert(self, login: Login) -> Login:
        with Connection() as conn:
            conn.add(login)
            conn.commit()
            conn.refresh(login)
            return login
        
    def select_by_id(self, id: int) -> Login:
        with Connection() as conn:
            return conn.get(Login, id)
        
    def select_by_provider_id(self, id: int) -> Login:
        with Connection() as conn:
            return conn.get(Login, id)
        
    def select_by_email(self, email: str) -> Login:
        with Connection() as conn:
            return conn.query(Login).filter(Login.email == email).first()

    def update(self, login: Login) -> Login:
        with Connection() as conn:
            existing = conn.get(Login, login.id)
            if existing:
                merged = conn.merge(login)
                conn.commit()
                conn.refresh(merged)
                return merged
