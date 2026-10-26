def test_criar_tarefa(client, criar_usuario):
    headers = criar_usuario()

    resposta = client.post("/tasks", json={"titulo": "Estudar"}, headers=headers)

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["id"] == 1
    assert corpo["titulo"] == "Estudar"
    assert corpo["concluida"] is False


def test_criar_tarefa_sem_titulo_da_422(client, criar_usuario):
    headers = criar_usuario()

    resposta = client.post("/tasks", json={"descricao": "sem título"}, headers=headers)

    assert resposta.status_code == 422


def test_rotas_de_tarefas_sem_token_dao_401(client):
    assert client.get("/tasks").status_code == 401
    assert client.post("/tasks", json={"titulo": "x"}).status_code == 401
    assert client.get("/tasks/1").status_code == 401
    assert client.put("/tasks/1", json={"titulo": "x", "concluida": True}).status_code == 401
    assert client.delete("/tasks/1").status_code == 401


def test_listar_e_buscar_tarefa(client, criar_usuario):
    headers = criar_usuario()
    client.post("/tasks", json={"titulo": "A"}, headers=headers)
    client.post("/tasks", json={"titulo": "B"}, headers=headers)

    lista = client.get("/tasks", headers=headers)
    uma = client.get("/tasks/2", headers=headers)

    assert [t["titulo"] for t in lista.json()] == ["A", "B"]
    assert uma.json()["titulo"] == "B"


def test_editar_tarefa(client, criar_usuario):
    headers = criar_usuario()
    client.post("/tasks", json={"titulo": "Estudar"}, headers=headers)

    resposta = client.put(
        "/tasks/1",
        json={"titulo": "Estudar FastAPI", "descricao": "etapa 6", "concluida": True},
        headers=headers,
    )

    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Estudar FastAPI"
    assert resposta.json()["concluida"] is True


def test_apagar_tarefa(client, criar_usuario):
    headers = criar_usuario()
    client.post("/tasks", json={"titulo": "Estudar"}, headers=headers)

    resposta = client.delete("/tasks/1", headers=headers)

    assert resposta.status_code == 204
    assert client.get("/tasks/1", headers=headers).status_code == 404


def test_tarefa_inexistente_da_404(client, criar_usuario):
    headers = criar_usuario()

    assert client.get("/tasks/99", headers=headers).status_code == 404
    assert client.put("/tasks/99", json={"titulo": "x", "concluida": True}, headers=headers).status_code == 404
    assert client.delete("/tasks/99", headers=headers).status_code == 404


def test_id_apagado_nao_e_reaproveitado(client, criar_usuario):
    headers = criar_usuario()
    client.post("/tasks", json={"titulo": "A"}, headers=headers)
    client.post("/tasks", json={"titulo": "B"}, headers=headers)
    client.delete("/tasks/2", headers=headers)

    resposta = client.post("/tasks", json={"titulo": "C"}, headers=headers)

    assert resposta.json()["id"] == 3


def test_filtrar_por_concluida(client, criar_usuario):
    headers = criar_usuario()
    client.post("/tasks", json={"titulo": "Pendente"}, headers=headers)
    client.post("/tasks", json={"titulo": "Feita"}, headers=headers)
    client.put("/tasks/2", json={"titulo": "Feita", "concluida": True}, headers=headers)

    feitas = client.get("/tasks?concluida=true", headers=headers).json()
    pendentes = client.get("/tasks?concluida=false", headers=headers).json()

    assert [t["titulo"] for t in feitas] == ["Feita"]
    assert [t["titulo"] for t in pendentes] == ["Pendente"]


def test_paginacao(client, criar_usuario):
    headers = criar_usuario()
    for n in range(1, 13):
        client.post("/tasks", json={"titulo": f"T{n}"}, headers=headers)

    padrao = client.get("/tasks", headers=headers).json()
    segunda_pagina = client.get("/tasks?skip=10&limit=10", headers=headers).json()

    assert len(padrao) == 10
    assert [t["id"] for t in segunda_pagina] == [11, 12]


def test_paginacao_com_valores_invalidos_da_422(client, criar_usuario):
    headers = criar_usuario()

    assert client.get("/tasks?limit=0", headers=headers).status_code == 422
    assert client.get("/tasks?limit=101", headers=headers).status_code == 422
    assert client.get("/tasks?skip=-1", headers=headers).status_code == 422


def test_cada_usuario_ve_so_as_proprias_tarefas(client, criar_usuario):
    ana = criar_usuario("ana@teste.com")
    beto = criar_usuario("beto@teste.com")
    client.post("/tasks", json={"titulo": "Da Ana"}, headers=ana)
    client.post("/tasks", json={"titulo": "Do Beto"}, headers=beto)

    assert [t["titulo"] for t in client.get("/tasks", headers=ana).json()] == ["Da Ana"]
    assert [t["titulo"] for t in client.get("/tasks", headers=beto).json()] == ["Do Beto"]


def test_usuario_nao_mexe_na_tarefa_de_outro(client, criar_usuario):
    ana = criar_usuario("ana@teste.com")
    beto = criar_usuario("beto@teste.com")
    client.post("/tasks", json={"titulo": "Da Ana"}, headers=ana)

    # 404 e não 403: para o Beto, a tarefa da Ana simplesmente não existe
    assert client.get("/tasks/1", headers=beto).status_code == 404
    assert client.put("/tasks/1", json={"titulo": "hackeado", "concluida": True}, headers=beto).status_code == 404
    assert client.delete("/tasks/1", headers=beto).status_code == 404

    intacta = client.get("/tasks/1", headers=ana).json()
    assert intacta["titulo"] == "Da Ana"
    assert intacta["concluida"] is False
