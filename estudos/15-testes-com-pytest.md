# 15 · Testes automatizados com Pytest

## Por que testar

Até a Etapa 5, todo teste era manual (curl ou `/docs`). A cada mudança, era
preciso refazer tudo na mão. Com testes automatizados:

```powershell
pytest
```

Em ~10 segundos, **24 cenários** conferidos. Se uma mudança quebrar algo que
funcionava (uma **regressão**), você descobre na hora, e não pelo usuário.

## Anatomia de um teste: AAA

```python
def test_apagar_tarefa(client, criar_usuario):
    # Arrange (preparar): monta o cenário
    headers = criar_usuario()
    client.post("/tasks", json={"titulo": "Estudar"}, headers=headers)

    # Act (agir): faz a ação que está sendo testada
    resposta = client.delete("/tasks/1", headers=headers)

    # Assert (conferir): confere o resultado
    assert resposta.status_code == 204
    assert client.get("/tasks/1", headers=headers).status_code == 404
```

- O nome do arquivo começa com `test_` e o da função também. É assim que o
  pytest os encontra.
- O nome diz **o que** está sendo testado: `test_token_vencido_da_401`.
- `assert` é "garanta que isso é verdade". Se não for, o teste falha.

## TestClient

```python
client.post("/tasks", json={...}, headers=headers)
```

Ele chama a API **direto em memória**, sem subir o uvicorn e sem rede. Por
isso é rápido. Precisa da biblioteca `httpx` instalada.

## Fixtures (`tests/conftest.py`)

Fixtures são **preparações reutilizáveis**. O teste só **pede pelo nome** e o
pytest entrega pronta. É **injeção de dependência**, igual ao `Depends`!

```python
@pytest.fixture
def client():
    ...                # prepara (antes do teste)
    yield TestClient(app)
    ...                # limpa (depois do teste)
```

| Fixture | Entrega |
|---|---|
| `client` | um TestClient com **banco novo e vazio** |
| `criar_usuario` | uma função que cadastra, faz login e devolve o header `Authorization` |

O `conftest.py` é especial: o pytest carrega sozinho as fixtures dele para
todos os testes da pasta.

## Banco de teste separado

```python
engine = create_engine("sqlite://", poolclass=StaticPool, ...)   # em memória
app.dependency_overrides[get_db] = get_db_teste                   # troca o banco
```

1. **`sqlite://`** (sem nome de arquivo) é um banco **só na memória**, que some
   no fim do teste.
2. **Um banco novo por teste:** um teste nunca vê os dados de outro, então a
   ordem não importa. Isso se chama **isolamento**.
3. **`dependency_overrides`:** as rotas pedem `get_db`, e nos testes o FastAPI
   entrega o `get_db_teste`. **Nenhuma rota foi alterada para isso.** É a
   vantagem da injeção de dependência prometida no estudo 07.
4. **`StaticPool`:** cada conexão nova com `sqlite://` abriria um banco
   **vazio e diferente**. O StaticPool usa sempre a mesma conexão.

> Por que nunca testar no banco de verdade? Os testes apagam e criam dados à
> vontade. Rodar no banco real destruiria dados de usuários.

## Por que o `create_all` foi para o `lifespan`?

Antes, `Base.metadata.create_all(...)` rodava **ao importar** o `main.py`. Como
os testes importam o app, eles criariam um `tarefas.db` de verdade na pasta.
Agora ele roda no **`lifespan`**, que só executa quando o **servidor sobe**:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)   # quando o servidor sobe
    yield                                    # servidor rodando
                                             # (depois do yield: quando desliga)
```

## Os testes testam de verdade?

Um teste que nunca falha não serve para nada. Na Etapa 6 o código foi
**sabotado de propósito** para conferir:

| Bug introduzido | Teste que pegou |
|---|---|
| Tirar a checagem de dono no buscar/editar/apagar | `test_usuario_nao_mexe_na_tarefa_de_outro` ❌ |
| Tirar o filtro de dono na listagem | `test_cada_usuario_ve_so_as_proprias_tarefas` ❌ |

Depois o código foi restaurado e os 24 voltaram a passar ✅

## Comandos úteis

```powershell
pytest                       # roda tudo
pytest -v                    # mostra o nome de cada teste
pytest tests/test_users.py   # um arquivo só
pytest -k paginacao          # só os testes com "paginacao" no nome
pytest -x                    # para no primeiro que falhar
```

## 🎯 Resposta de entrevista

> "Tenho 24 testes com pytest e TestClient cobrindo cadastro, login, token
> inválido ou vencido, CRUD, filtros, paginação e o isolamento entre usuários.
> Cada teste usa um SQLite em memória novo, trocado via dependency_overrides,
> então os testes são isolados e nunca tocam o banco real. Uso fixtures para
> o cliente e para criar um usuário logado. Também validei os testes
> introduzindo bugs de propósito, para garantir que eles realmente falham
> quando algo quebra."
