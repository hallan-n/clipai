import httpx
from usecase.login import LoginUsecase
from db.database import get_session
from schemas.login import AccessToken, CreateLocalLoginRequest, CreateLocalLoginResponse, LocalLoginRequest, LoginDTO
from api.security import check_hash, create_access_token
from consts import CLIENT_ID, CLIENT_SECRET
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

route = APIRouter(prefix="/auth", tags=["Autenticação"])
login_service = LoginUsecase()


@route.get("/github/login")
def github_login():
    url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        "&scope=read:user user:email"
    )
    return RedirectResponse(url)


@route.get("/github")
async def github_callback(
    code: str,
    session: Session = Depends(get_session)
) -> AccessToken:

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

        email = user_data.get("email")

        if not email:
            emails_resp = await client.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {token}"},
            )

            emails = emails_resp.json()
            primary = next((e for e in emails if e["primary"]), None)

            if primary:
                email = primary["email"]

        if not email:
            raise HTTPException(400, "GitHub did not return email")


    login = login_service.get_login(
        session=session,
        email=email,
        provider="github",
        required=False
    )

    if login:
        access_token = create_access_token(
            {"sub": str(login.public_id), "email": login.email}
        )

        return AccessToken(
            access_token=access_token,
            token_type="Bearer",
        )


    created_login = login_service.add_login(
        session=session,
        data=LoginDTO(
            email=email,
            name=user_data.get("name"),
            provider="github",
            provider_id=str(user_data["id"]),
            avatar_url=user_data.get("avatar_url"),
        )
    )

    access_token = create_access_token(
        {"sub": str(created_login.public_id), "email": created_login.email}
    )

    return AccessToken(
        access_token=access_token,
        token_type="Bearer",
    )


@route.post("/local", response_model=CreateLocalLoginResponse)
def create_local_login(login: CreateLocalLoginRequest, session: Session = Depends(get_session)):
    create_login = LoginDTO(
        email=login.email,
        name=login.name,
        password=login.password,
        provider='local',
        avatar_url=login.avatar_url,
    )
    login_created = login_service.add_login(session, create_login)
    return login_created

@route.post("/local/login", response_model=AccessToken)
def local_login(login: LocalLoginRequest, session: Session = Depends(get_session)) -> AccessToken:
    has_login = login_service.get_login(session, email=login.email)

    if not check_hash(has_login.password, login.password):
        raise HTTPException(409, "Credenciais inválidas.")

    access_token = create_access_token(
        {"sub": str(has_login.public_id), "email": has_login.email}
    )
    return AccessToken(
        access_token=access_token,
        token_type="Bearer",
    )
