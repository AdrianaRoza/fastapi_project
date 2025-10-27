from fastapi import Depends, HTTPException
from main import SECRET_KEY,ALGORITHM,oauth2_schemas
from models import db
from sqlalchemy.orm import sessionmaker,Session
from models import User
from jose import jwt, JWTError

def capture_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verify_token(token: str = Depends(oauth2_schemas), session: Session = Depends(capture_session)):
    try:
        dic_inf = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_user = int(dic_inf.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")

    user = session.query(User).filter(User.id==id_user).first()
    if not user:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return user