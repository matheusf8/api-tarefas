from datetime import datetime, timedelta, timezone

import jwt

from app.auth import ALGORITHM, SECRET_KEY


def test_cadastro_devolve_usuario_sem_senha(client):
    resposta = client.post("/register", json={"email": "Ana@Teste.com", "senha": "senha1234"})

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["email"] == "ana@teste.com"  # salvo em minúsculas
    assert "senha" not in corpo
    assert "senha_hash" not in corpo


def test_cadastro_com_email_repetido_da_409(client):
    client.post("/register", json={"email": "ana@teste.com", "senha": "senha1234"})

    resposta = client.post("/register", json={"email": "ANA@teste.com", "senha": "outra1234"})

    assert resposta.status_code == 409


def test_cadastro_com_email_invalido_da_422(client):
    resposta = client.post("/register", json={"email": "nao-e-email", "senha": "senha1234"})

    assert resposta.status_code == 422


def test_cadastro_com_senha_curta_da_422(client):
    resposta = client.post("/register", json={"email": "ana@teste.com", "senha": "123"})

    assert resposta.status_code == 422


def test_cadastro_com_senha_acima_de_72_bytes_da_422(client):
    resposta = client.post("/register", json={"email": "ana@teste.com", "senha": "é" * 40})

    assert resposta.status_code == 422


def test_login_devolve_token(client):
    client.post("/register", json={"email": "ana@teste.com", "senha": "senha1234"})

    resposta = client.post("/login", data={"username": "ana@teste.com", "password": "senha1234"})

    assert resposta.status_code == 200
    assert resposta.json()["token_type"] == "bearer"
    assert resposta.json()["access_token"]


def test_login_com_senha_errada_e_email_inexistente_dao_a_mesma_resposta(client):
    client.post("/register", json={"email": "ana@teste.com", "senha": "senha1234"})

    senha_errada = client.post("/login", data={"username": "ana@teste.com", "password": "errada123"})
    sem_conta = client.post("/login", data={"username": "ninguem@teste.com", "password": "senha1234"})

    assert senha_errada.status_code == 401
    assert sem_conta.status_code == 401
    assert senha_errada.json() == sem_conta.json()


def test_me_devolve_o_dono_do_token(client, criar_usuario):
    headers = criar_usuario("ana@teste.com")

    resposta = client.get("/me", headers=headers)

    assert resposta.status_code == 200
    assert resposta.json()["email"] == "ana@teste.com"


def test_me_sem_token_da_401(client):
    assert client.get("/me").status_code == 401


def test_token_vencido_da_401(client, criar_usuario):
    criar_usuario()
    vencido = jwt.encode(
        {"sub": "1", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    resposta = client.get("/me", headers={"Authorization": f"Bearer {vencido}"})

    assert resposta.status_code == 401


def test_token_assinado_com_outra_chave_da_401(client, criar_usuario):
    criar_usuario()
    falso = jwt.encode(
        {"sub": "1", "exp": datetime.now(timezone.utc) + timedelta(minutes=5)},
        "chave-de-quem-quer-invadir-0123456789abcdef",
        algorithm=ALGORITHM,
    )

    resposta = client.get("/me", headers={"Authorization": f"Bearer {falso}"})

    assert resposta.status_code == 401
