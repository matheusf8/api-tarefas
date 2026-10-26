import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# lê o header "Authorization: Bearer <token>"; o tokenUrl liga o botão Authorize do /docs
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def gerar_hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))


def criar_token(user_id: int) -> str:
    expira_em = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados = {"sub": str(user_id), "exp": expira_em}
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)


def get_usuario_logado(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    erro = HTTPException(
        status_code=401,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # confere a assinatura e a validade (exp); token adulterado ou vencido cai no except
        dados = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(dados["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise erro

    usuario = db.get(models.User, user_id)
    if usuario is None:
        raise erro
    return usuario
