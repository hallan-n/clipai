from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import httpx
from api.security import create_access_token, hashed, check_hash
from api.schemas.login import (
    CreateLocalLoginRequest,
    CreateLocalLoginResponse,
    AccessToken,
    LocalLoginRequest,
)
from db.models import Login
from crud.crud_login import LoginRepository
from consts import CLIENT_ID, CLIENT_SECRET

route = APIRouter(prefix="/auth", tags=["Autenticação"])
login_repo = LoginRepository()


@route.get(
    "/github/login",
    summary="Pegar a URL de login do GitHub",
    description="Obtém a URL para redirecionamento ao login do GitHub.",
)
def github_login():

    url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        "&scope=read:user user:email"
    )
    return RedirectResponse(url)


@route.get(
    "/github",
    summary="Callback do login do GitHub",
    description="Callback para processar o login do GitHub e gerar um token de acesso.",
    response_model=AccessToken,
)
async def github_callback(code: str) -> AccessToken:
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
            },
        )
        token = token_resp.json()["access_token"]

        user_resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {token}"},
        )
        user_data = user_resp.json()
        login = login_repo.select_by_provider("Github", user_data["id"])
        if login:
            access_token = create_access_token(
                {"sub": str(login.public_id), "email": login.email}
            )
            return AccessToken(
                access_token=access_token,
                token_type="Bearer",
            )

        created_login = login_repo.insert(
            Login(
                email=user_data["email"],
                name=user_data["email"],
                provider="Github",
                provider_id=user_data["id"],
                avatar_url=user_data["avatar_url"],
            )
        )

        access_token = create_access_token(
            {"sub": str(created_login.public_id), "email": created_login.email}
        )
        return AccessToken(
            access_token=access_token,
            token_type="Bearer",
        )


@route.post(
    "/local",
    summary="Criar login local",
    description="Cria um novo login local com email e senha.",
    response_model=CreateLocalLoginResponse,
)
def create_local_login(login: CreateLocalLoginRequest) -> CreateLocalLoginResponse:
    email_is_user = login_repo.select_by_email(login.email)
    if email_is_user:
        raise HTTPException(409, "Email em uso.")

    login.password = hashed(login.password)

    created_login = login_repo.insert(
        Login(
            email=login.email,
            password=login.password,
            name=login.name,
            provider="Local",
            avatar_url=login.avatar_url,
        )
    )

    return CreateLocalLoginResponse(
        public_id=str(created_login.public_id),
        email=created_login.email,
        name=created_login.name,
        password=created_login.password,
        avatar_url=created_login.avatar_url,
        created_at=created_login.created_at,
        updated_at=created_login.updated_at,
    )


@route.post(
    "/local/login",
    summary="Login local",
    description="Realiza o login local com email e senha.",
    response_model=AccessToken,
)
def local_login(login: LocalLoginRequest) -> AccessToken:
    has_login = login_repo.select_by_email(login.email)
    if has_login is None:
        raise HTTPException(409, "Credenciais inválidas.")

    if not check_hash(has_login.password, login.password):
        raise HTTPException(409, "Credenciais inválidas.")

    access_token = create_access_token(
        {"sub": str(has_login.public_id), "email": has_login.email}
    )
    return AccessToken(
        access_token=access_token,
        token_type="Bearer",
    )
