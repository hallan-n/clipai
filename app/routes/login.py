from fastapi import APIRouter, Depends, HTTPException
from infra.persistence.login import add, get, get_by_email, update
from infra.schemas import Login
from infra.security import (check_hash, create_access_token, decode_token,
                            hashed)
from models import PostLogin, PutLogin

login = APIRouter(tags=["Login"], prefix="/login")


@login.post("/signin")
def sign_in(login: PostLogin):
    login_auth = get_by_email(login.email)
    if not login_auth:
        raise HTTPException(404, "Login não encontrado!")

    if not check_hash(login_auth.password, login.password):
        raise HTTPException(404, "Senha incorreta!")

    data = {"sub": login_auth.email, "id": login_auth.id}
    access_token = create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}


@login.post("/create")
def create_login(login: PostLogin):
    """Cria um login"""
    has_login = get_by_email(login.email)
    if has_login:
        raise HTTPException(403, "Email em uso!")

    login.password = hashed(login.password)
    try:
        schema = Login(email=login.email, password=login.password)
        success_login = add(schema)
        return success_login
    except Exception as e:
        raise HTTPException(400, f"Erro ao criar login: {e}")


@login.get("/get")
def get_login(token: dict = Depends(decode_token)):
    login = get(token["id"])
    return login


@login.put("/update")
def update_login(login: PutLogin, token: dict = Depends(decode_token)):
    login.password = hashed(login.password)
    try:
        schema = Login(id=token["id"], email=login.email, password=login.password)
        success_login = update(schema)
        return success_login
    except Exception as e:
        raise HTTPException(400, f"Erro ao atualizar login: {e}")
