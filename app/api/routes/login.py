from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import httpx
import uvicorn
from crud.crud_login import LoginRepository
from consts import CLIENT_ID, CLIENT_SECRET


route = APIRouter()


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

        login_usecase.sele
        return user_resp.json()
        return {
            "email": user_resp.json()["email"],
            "name": user_resp.json()["name"],
            "provider": "Github",
            "avatar_url": user_resp.json()["avatar_url"],
        }
