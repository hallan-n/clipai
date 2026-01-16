from fastapi import APIRouter, HTTPException
from models import PostLogin, PutLogin
from infra.schemas import Login
from infra.persistence.login import get_login_by_email, create_login
from infra.security import hashed

login = APIRouter(tags=["Login"], prefix="/login")

# @login.get('/{id}')
# def get_login(id: int):
#     """Recupera um Login por ID"""
#     return "Logado"


# @login.post('')
# def post_login(login: PostLogin):
#     return login


# @login.put('')
# def put_login(login: PutLogin):
#     return login



# @login.post("/sign_in")
# def sign_in(login: Login):
#     login_auth = get_by_user(login.user)
#     if not bool(login_auth):
#         raise HTTPException(404, "Login não encontrado!")

#     if not check_hash(login_auth.password, login.password):
#         raise HTTPException(404, "Senha incorreta!")

#     data = {"sub": login_auth.user, "id": login_auth.id}
#     access_token = create_access_token(data=data)
#     return {"access_token": access_token, "token_type": "bearer"}


@login.post("")
def create_login(login: PostLogin):
    """Cria um login"""
    has_login = get_login_by_email(login.email)
    if has_login:
        raise HTTPException(403, "Email em uso!")

    login.password = hashed(login.password)
    try:
        schema = Login(email=login.email, password=login.password)
        success_login =  create_login(schema)
        return success_login
    except Exception as e:
        raise HTTPException(400, f"Erro ao criar login: {e}")


# @login.get("/get")
# async def get_login(token: dict = Depends(decode_token)):
#     login = get_login_by_id(token["id"])
#     return login


# @login.put("/update")
# async def update(login: Login, token: dict = Depends(decode_token)):
#     login.id = token["id"]
#     return update_login(login)
