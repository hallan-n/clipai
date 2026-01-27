from crud.crud_login import LoginRepository
from db.models import Login


def get_current_user(data: str) -> Login:
    repo = LoginRepository()
    return repo.select_by_email(data["email"])
