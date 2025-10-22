from fastapi import APIRouter, Depends
from models import User
from dependencies import capture_session
from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """
    Essa é uma rota padrão de autenticação do nosso sistema
    """
    return {"mensagem": "Você acessou a rota padrão autentição", "autenticado":False}

@auth_router.post("/create_account")
async def create_account(email: str, password: str, name: str, session = Depends(capture_session)):
    user = session.query(User).filter(User.email==email).first()
    if user:
        return{"mensagem":"Já existe um usuário com esse email"}
    
    else:
        encrypted_password = bcrypt_context.hash(password[:72])
        new_user = User(name=name, email=email, password=encrypted_password)
        session.add(new_user)
        session.commit()
        return{"mensagem": "Usuáio cadastrado com sucesso"}