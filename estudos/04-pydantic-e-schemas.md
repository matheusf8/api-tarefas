# 04 · Pydantic e schemas

## O que é

O Pydantic **valida e converte dados** usando os type hints do Python. No
FastAPI, os **schemas** (classes que herdam de `BaseModel`) definem **o formato
do que entra e do que sai** da API.

## Os três schemas do projeto ([app/schemas.py](../app/schemas.py))

| Schema | Direção | Tem `id`? | Por quê |
|---|---|---|---|
| `TaskCreate` | entra (POST) | ❌ | quem gera o id é o servidor |
| `TaskUpdate` | entra (PUT)  | ❌ | o id já vem na URL |
| `TaskOut`    | sai          | ✅ | o cliente precisa saber o id |

```python
class TaskCreate(BaseModel):
    titulo: str                     # obrigatório, tem que ser texto
    descricao: str | None = None    # opcional, padrão None
```

## O que ele faz sozinho

- Falta o `titulo` → **422** com `"msg": "Field required"`.
- Mandaram `"titulo": 123` → **422**.
- `/tasks/abc` com `id: int` → **422** com `int_parsing`.

Tudo isso sem escrever nenhum `if`.

## `response_model` filtra a saída

```python
@app.post("/tasks", response_model=TaskOut)
```

Só os campos do `TaskOut` vão para a resposta. Isso vai ser importante na
Etapa 4: o model `User` vai ter `senha_hash`, mas o `UserOut` não. Assim **o
hash da senha nunca vaza** na resposta.

## `from_attributes=True`

Por padrão o Pydantic lê **dicionários**. Desde a Etapa 2 as rotas devolvem
**objetos do SQLAlchemy**, e essa configuração permite ler os atributos
(`tarefa.titulo`) em vez de chaves (`tarefa["titulo"]`).

```python
class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
```

## Schema (Pydantic) × Model (SQLAlchemy)

| | Schema (`schemas.py`) | Model (`models.py`) |
|---|---|---|
| Representa | O **contrato da API** (JSON) | A **tabela do banco** |
| Biblioteca | Pydantic | SQLAlchemy |
| Exemplo | `TaskCreate`, `TaskOut` | `Task` |

São separados de propósito: o que fica guardado no banco nem sempre é o que a
API deve mostrar.

## 🎯 Resposta de entrevista

> "Uso o Pydantic para definir schemas de entrada e saída. Ele valida os dados
> pelos tipos e o FastAPI devolve 422 sozinho quando algo vem errado. Separo
> os schemas de criação e de resposta: o de criação não tem id, porque o
> servidor gera, e o response_model garante que campos sensíveis não saiam na
> resposta. Também mantenho os schemas separados dos models do SQLAlchemy,
> porque um é o contrato da API e o outro é a estrutura do banco."
