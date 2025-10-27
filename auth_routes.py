from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import capture_session, verify_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UserSchemas,LoginSchemas
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def create_token(id_user, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + token_duration
    dic_inf = {"sub": str(id_user), "exp": expiration_date}
    jwt_encoded = jwt.encode(dic_inf, SECRET_KEY, ALGORITHM)

    return  jwt_encoded



def authenticate_user(email, password, session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user
    


@auth_router.get("/")
async def home():
    """
    Essa é uma rota padrão de autenticação do nosso sistema
    """
    return {"mensagem": "Você acessou a rota padrão autentição", "autenticado":False}

@auth_router.post("/create_account")
async def create_account(user_Schemas: UserSchemas, session: Session = Depends(capture_session)):
    user = session.query(User).filter(User.email==user_Schemas.email).first()
    if user:
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    
    else:
        encrypted_password = bcrypt_context.hash(user_Schemas.password[:72])
        new_user = User(user_Schemas.name, user_Schemas.email, encrypted_password, user_Schemas.active, user_Schemas.admin)
        session.add(new_user)
        session.commit()
        return{"mensagem": f"Usuáio cadastrado com sucesso {user_Schemas.email}"}
    

@auth_router.post("/login")
async def login(login_schemas: LoginSchemas, session: Session = Depends(capture_session)):   
    user = authenticate_user(login_schemas.email, login_schemas.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, token_duration=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token":refresh_token,
            "token_type": "Bearer"
            }
    


@auth_router.post("/login-form")
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(capture_session)):   
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = create_token(user.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
            }


    


@ auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(verify_token)):
    access_token = create_token(user.id)
    return {
            "access_token": access_token,
            "token_type": "Bearer"
            }