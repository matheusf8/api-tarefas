# 14 · Routers: organizando as rotas

## O problema

Com todas as rotas no `main.py`, o arquivo cresce sem parar e mistura
assuntos: usuário, tarefa, login...

## A solução: `APIRouter`

Cada assunto ganha seu arquivo. O `main.py` só **junta** tudo:

```
app/
├── main.py              # cria o app e registra os routers
└── routers/
    ├── users.py         # /register, /login, /me
    └── tasks.py         # /tasks, /tasks/{id}
```

```python
# app/routers/tasks.py
router = APIRouter(prefix="/tasks", tags=["tarefas"])

@router.get("")          # vira GET /tasks
@router.get("/{id}")     # vira GET /tasks/{id}
```

```python
# app/main.py
app.include_router(users.router)
app.include_router(tasks.router)
```

| Parâmetro | Faz o quê |
|---|---|
| `prefix="/tasks"` | põe `/tasks` na frente de todas as rotas do arquivo |
| `tags=["tarefas"]` | agrupa as rotas no `/docs` |

## Por que `@router.get("")` e não `@router.get("/")`?

Com `"/"` a rota seria `/tasks/`, com barra no final. Quem chamasse `/tasks`
seria redirecionado (307). Com `""` fica exatamente `/tasks`.

## 🎯 Resposta de entrevista

> "Organizo as rotas por domínio com APIRouter: um arquivo para usuários e
> outro para tarefas, cada um com seu prefixo e tag. O main.py só cria o app e
> inclui os routers. Fica mais fácil de achar as coisas e de crescer o projeto
> sem um arquivo gigante."
