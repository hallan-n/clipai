from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.security import hashed
from schemas.login import LoginDTO
from db.models import Login
from db.repository.login import LoginRepository

login_repo = LoginRepository()


class LoginUsecase:
    def get_login(
        self, session: Session, login_id: int = None, email: str = None, provider: str = None, required: bool = True
    ):
        if email and provider:
            login = login_repo.select_by_email_and_provider(session, email, provider)

        elif email:
            login = login_repo.select_by_email(session, email)

        elif provider:
            raise HTTPException(400, "Provider precisa de identificador.")

        elif login_id:
            login = login_repo.select_by_id(session, login_id)

        else:
            raise HTTPException(400, "Parâmetros inválidos.")

        if required and not login:
            raise HTTPException(404, "Login não encontrado")


        return LoginDTO(
            id=login.id,
            public_id=login.public_id,
            email=login.email,
            name=login.name,
            password=login.password,
            provider=login.provider,
            provider_id=login.provider_id,
            avatar_url=login.avatar_url,
            created_at=login.created_at,
            updated_at=login.updated_at,
        )

    def add_login(self, session: Session, data: LoginDTO) -> LoginDTO:
        email_in_use = login_repo.select_by_email(session, data.email)
        if email_in_use:
            raise HTTPException(404, "Email já cadastrado.")
        
        if data.password:
            data.password = hashed(data.password)

        login = login_repo.insert(session, Login(**data.model_dump()))
        session.commit()
        
        return LoginDTO(
            id=login.id,
            public_id=login.public_id,
            email=login.email,
            name=login.name,
            password=login.password,
            provider=login.provider,
            provider_id=login.provider_id,
            avatar_url=login.avatar_url,
            created_at=login.created_at,
            updated_at=login.updated_at,
        )
