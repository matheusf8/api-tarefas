# 07 · Injeção de dependência (`Depends`)

## A ideia em uma frase

Em vez de a função **criar** o que precisa, ela **declara** o que precisa, e o
framework **entrega pronto**.

## No projeto

```python
@app.get("/tasks", response_model=list[TaskOut])
def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(models.Task).all()
```

A rota diz: *"preciso de uma sessão do banco"*. O FastAPI então:

1. Chama `get_db()`, que abre a sessão.
2. Entrega a sessão no parâmetro `db`.
3. Executa a rota.
4. Volta no `get_db()` e roda o `finally: db.close()`.

Por isso o `get_db` usa **`yield`** em vez de `return`: o `yield` "pausa" a
função, deixa a rota trabalhar e depois continua de onde parou para fechar a
sessão.

## Sem injeção de dependência (pior)

```python
def listar_tarefas():
    db = SessionLocal()
    try:
        return db.query(models.Task).all()
    finally:
        db.close()
```

Esse `try/finally` se repetiria nas 5 rotas, e bastaria esquecer o `close` em
uma delas para vazar conexão.

## Por que é tão útil: testes

Na Etapa 6 vamos **trocar o banco real por um banco de teste** sem mexer em
nenhuma rota:

```python
app.dependency_overrides[get_db] = get_db_de_teste
```

É possível porque as rotas **não sabem de onde vem** a sessão. Elas só pedem
uma.

## Onde mais vamos usar

Na Etapa 5: `usuario = Depends(get_usuario_logado)`. A rota declara que precisa
do usuário logado, e o FastAPI lê o token, valida e entrega o usuário.

## 🎯 Resposta de entrevista

> "Injeção de dependência é quando a função recebe o que precisa de fora, em
> vez de criar sozinha. No FastAPI uso o `Depends`: por exemplo,
> `Depends(get_db)` abre uma sessão por requisição e garante que ela seja
> fechada. Isso evita código repetido e facilita os testes, porque consigo
> trocar a dependência real por uma de teste com `dependency_overrides`."
