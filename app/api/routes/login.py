from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import httpx
from api.security import create_access_token, hashed, check_hash, decode_token
from api.schemas import PostLoginRequest, PostLoginResponse
from db.models import Login
from crud.crud_login import LoginRepository
from consts import CLIENT_ID, CLIENT_SECRET


route = APIRouter()
login_repo = LoginRepository()

@route.get("/auth/github/login")
def github_login():

    url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        "&scope=read:user user:email"
    )
    return RedirectResponse(url)


@route.get("/auth/github")
async def github_callback(code: str):
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
        login = login_repo.select_by_provider('Github', user_data['id'])
        if login:
            access_token = create_access_token(
                {"sub": str(login.public_id), "email": login.email}
            )
            return {
                "access_token": access_token,
                "token_type": "Bearer",
            }
        
        created_login = login_repo.insert(Login(
            email=user_data['email'],
            name=user_data['email'],
            provider="Github",
            provider_id=user_data['id'],
            avatar_url=user_data['avatar_url']
        ))
        
        access_token = create_access_token(
            {"sub": str(created_login.public_id), "email": created_login.email}
        )
        return {
            "access_token": access_token,
            "token_type": "Bearer",
        }
    



@route.post("/auth/local")
async def create_local_login(login: PostLoginRequest) -> PostLoginResponse:

    email_is_user = login_repo.select_by_email(login.email)
    if email_is_user:
        raise HTTPException(409, "Email em uso.")
    
    login.password = hashed(login.password)

    created_login = login_repo.insert(Login(
        email=login.email,
        password=login.password,
        name=login.name,
        provider='Local',
        avatar_url=login.avatar_url
    ))
    
    return PostLoginResponse(
        public_id=str(created_login.public_id),
        email=created_login.email,
        name=created_login.name,
        password=created_login.password,
        avatar_url=created_login.avatar_url,
        created_at=created_login.created_at,
        updated_at=created_login.updated_at,
    )

    # async with httpx.AsyncClient() as client:
    #     token_resp = await client.post(
    #         "https://github.com/login/oauth/access_token",
    #         headers={"Accept": "application/json"},
    #         data={
    #             "client_id": CLIENT_ID,
    #             "client_secret": CLIENT_SECRET,
    #             "code": code,
    #         },
    #     )
    #     token = token_resp.json()["access_token"]

    #     user_resp = await client.get(
    #         "https://api.github.com/user",
    #         headers={"Authorization": f"Bearer {token}"},
    #     )
    #     user_data = user_resp.json()
    #     login = login_repo.select_by_provider('Github', user_data['id'])
    #     if login:
    #         access_token = create_access_token(
    #             {"sub": str(login.public_id), "email": login.email}
    #         )
    #         return {
    #             "access_token": access_token,
    #             "token_type": "Bearer",
    #         }
        
    #     created_login = login_repo.insert(Login(
    #         email=user_data['email'],
    #         name=user_data['email'],
    #         provider="Github",
    #         provider_id=user_data['id'],
    #         avatar_url=user_data['avatar_url']
    #     ))
        
    #     access_token = create_access_token(
    #         {"sub": str(created_login.public_id), "email": created_login.email}
    #     )
    #     return {
    #         "access_token": access_token,
    #         "token_type": "Bearer",
    #     }