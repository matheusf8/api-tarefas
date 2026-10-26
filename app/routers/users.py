from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models
from app.auth import criar_token, gerar_hash_senha, get_usuario_logado, verificar_senha
from app.database import get_db
from app.schemas import Token, UserCreate, UserOut

router = APIRouter(tags=["usuarios"])


@router.post("/register", status_code=201, response_model=UserOut)
def cadastrar(dados: UserCreate, db: Session = Depends(get_db)):
    email = dados.email.lower()
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")

    usuario = models.User(email=email, senha_hash=gerar_hash_senha(dados.senha))
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # o padrão OAuth2 chama o campo de "username"; aqui ele recebe o e-mail
    email = form.username.lower()
    usuario = db.query(models.User).filter(models.User.email == email).first()

    # mesma mensagem para e-mail inexistente e senha errada: não revela quais e-mails existem
    if usuario is None or not verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token=criar_token(usuario.id))


@router.get("/me", response_model=UserOut)
def quem_sou_eu(usuario: models.User = Depends(get_usuario_logado)):
    return usuario
