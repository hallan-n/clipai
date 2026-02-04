from db.repository.login import LoginRepository
from db.models import Login
from sqlalchemy.orm import Session


def get_current_login(session: Session, data: dict) -> Login:
    repo = LoginRepository()
    return repo.select_by_email(session, data["email"])
