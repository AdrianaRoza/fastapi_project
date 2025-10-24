from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import capture_session
from main import bcrypt_context
from schemas import UserSchemas,LoginSchemas
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def create_token(id_user):
    token = f"fnsyubf7sbfs9 {id_user}"
    return  token



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
    user = session.query(User).filter(User.email==login_schemas.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    else:
        access_token = create_token(user.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
            }
    