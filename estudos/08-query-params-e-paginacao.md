# 08 · Query params, filtros e paginação

## Query params

São as opções que vêm **depois do `?`** na URL, separadas por `&`:

```
GET /tasks?concluida=true&skip=0&limit=10
```

No FastAPI, **qualquer parâmetro da função que não está na rota** (como o
`{id}`) e **não é um schema** vira automaticamente um query param:

```python
@app.get("/tasks", response_model=list[TaskOut])
def listar_tarefas(
    concluida: bool | None = None,                 # filtro opcional
    skip: int = Query(default=0, ge=0),            # quantos pular
    limit: int = Query(default=10, ge=1, le=100),  # quantos trazer
    db: Session = Depends(get_db),
):
```

| Tipo de parâmetro | Onde está | Uso | Exemplo |
|---|---|---|---|
| **Path** | na rota: `/tasks/{id}` | **qual** recurso | `/tasks/3` |
| **Query** | depois do `?` | filtros e opções | `?concluida=true` |
| **Body** | corpo JSON | dados para criar/editar | `{"titulo": "..."}` |

## O filtro opcional

```python
consulta = db.query(models.Task)
if concluida is not None:
    consulta = consulta.filter(models.Task.concluida == concluida)
```

- Sem `?concluida=` → `None` → traz **todas**.
- `?concluida=true` → só as concluídas. `?concluida=false` → só as pendentes.

> ⚠️ Por que `is not None` e não `if concluida:`? Porque `False` também é um
> filtro válido. Com `if concluida:`, o `?concluida=false` seria **ignorado**,
> já que `False` é "falso" no `if`. É um bug clássico.

A consulta vai sendo **montada aos poucos**. O SQL só é executado no `.all()`.

## Paginação com `skip` e `limit`

Imagine 1.000 tarefas. Devolver todas de uma vez deixa a API lenta e pesada.
A paginação devolve **em pedaços**:

```python
consulta.order_by(models.Task.id).offset(skip).limit(limit).all()
```

SQL gerado: `SELECT * FROM tasks ORDER BY id LIMIT 10 OFFSET 0`

| Página | URL | Traz |
|---|---|---|
| 1ª | `?skip=0&limit=10` | ids 1 a 10 |
| 2ª | `?skip=10&limit=10` | ids 11 a 20 |
| 3ª | `?skip=20&limit=10` | ids 21 a 30 |

Fórmula: `skip = (pagina - 1) * limit`.

**Por que o `order_by`?** Sem ordem definida, o banco pode devolver as linhas
em qualquer ordem, e a mesma tarefa poderia aparecer em duas páginas ou
sumir. Paginação sempre precisa de uma ordem fixa.

## Validação com `Query(...)`

| Regra | Significa | Se violar |
|---|---|---|
| `ge=0` | **g**reater or **e**qual (≥ 0) | `?skip=-1` → 422 |
| `ge=1` | ≥ 1 | `?limit=0` → 422 |
| `le=100` | **l**ess or **e**qual (≤ 100) | `?limit=101` → 422 |

O `le=100` protege a API: sem ele, alguém poderia pedir `?limit=999999` e
derrubar o servidor.

## 🎯 Resposta de entrevista

> "Na listagem uso query params para filtro e paginação. O filtro de concluída
> é opcional: se vier None trago tudo, e comparo com `is not None` para o
> `false` também funcionar. A paginação usa skip e limit, que viram OFFSET e
> LIMIT no SQL, sempre com ORDER BY para a ordem ser estável entre as
> páginas. Limito o máximo a 100 itens com validação do próprio FastAPI, para
> ninguém pedir a tabela inteira de uma vez."
