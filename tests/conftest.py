import os

# precisa vir antes de importar o app: o auth.py lê a chave na importação.
# assim os testes não dependem do .env de ninguém.
os.environ.setdefault("SECRET_KEY", "chave-so-para-testes-0123456789abcdef0123456789abcdef")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db, ligar_chaves_estrangeiras
from app.main import app


@pytest.fixture
def client():
    # banco novo, só em memória, para cada teste: um teste nunca vê os dados de outro
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # uma conexão só; sem isso cada conexão teria um banco vazio
    )
    event.listen(engine, "connect", ligar_chaves_estrangeiras)
    Base.metadata.create_all(bind=engine)
    SessaoTeste = sessionmaker(bind=engine)

    def get_db_teste():
        db = SessaoTeste()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_db_teste
    yield TestClient(app)
    app.dependency_overrides.clear()
    engine.dispose()


@pytest.fixture
def criar_usuario(client):
    """Cadastra, faz login e devolve o header de autorização pronto."""

    def _criar(email="ana@teste.com", senha="senha1234"):
        resposta = client.post("/register", json={"email": email, "senha": senha})
        assert resposta.status_code == 201
        resposta = client.post("/login", data={"username": email, "password": senha})
        assert resposta.status_code == 200
        return {"Authorization": f"Bearer {resposta.json()['access_token']}"}

    return _criar
