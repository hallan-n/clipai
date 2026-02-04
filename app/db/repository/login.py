from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models import Login


class LoginRepository:
    def insert(self, session: Session, login: Login) -> Login:
        session.add(login)
        session.flush()       # gera ID antes do commit
        session.refresh(login)
        return login

    def update(self, session: Session, login: Login) -> Login | None:
        existing = session.get(Login, login.id)
        if existing:
            merged = session.merge(login)
            session.commit()
            session.refresh(merged)
            return merged
        return None

    def select_by_id(self, session: Session, login_id: int) -> Login | None:
        stmt = select(Login).where(Login.id == login_id)
        result = session.execute(stmt).scalars().first()
        return result

    def select_by_email(self, session: Session, email: str) -> Login | None:
        stmt = select(Login).where(Login.email == email)
        result = session.execute(stmt).scalars().first()
        return result
    
    def select_by_provider(self, session: Session, provider: str) -> Login | None:
        stmt = select(Login).where(Login.provider == provider)
        result = session.execute(stmt).scalars().first()
        return result
    
    def select_by_email_and_provider(self, session: Session, email: str, provider: str) -> Login | None:
        stmt = select(Login).where(
            Login.provider == provider,
            Login.email == email
        )
        result = session.execute(stmt).scalars().first()
        return result