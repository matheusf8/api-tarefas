# 06 · Sessão, commit e refresh

## Analogia: o carrinho de compras

| Banco de dados | Supermercado |
|---|---|
| **Sessão** | Você entra na loja com um carrinho |
| **`db.add(obj)`** | Coloca um produto no carrinho (ainda não é seu) |
| **`db.commit()`** | Passa no caixa e paga: agora é definitivo |
| **`db.rollback()`** | Desiste e devolve tudo o que estava no carrinho |
| **`db.refresh(obj)`** | Confere a nota fiscal para ver o que o caixa registrou |
| **`db.close()`** | Sai da loja e devolve o carrinho |

## Sessão

É uma **conversa com o banco**. Tudo o que você faz (adicionar, alterar,
apagar) fica guardado na sessão **até você confirmar**.

No projeto ([app/database.py](../app/database.py)):

```python
SessionLocal = sessionmaker(bind=engine)   # "fábrica" de sessões

def get_db():
    db = SessionLocal()   # abre uma sessão nova
    try:
        yield db          # entrega para a rota usar
    finally:
        db.close()        # SEMPRE fecha, mesmo se der erro
```

**Cada requisição ganha a sua própria sessão**, e ela é fechada quando a
requisição termina. Assim um usuário não mistura as mudanças com as de outro,
e as conexões não ficam abertas para sempre.

## Commit

É o **"salvar de verdade"**. Antes do commit, as mudanças existem só na
sessão, dentro da memória. O commit grava no arquivo `tarefas.db`.

```python
db.add(nova)     # só no carrinho
db.commit()      # agora está no banco
```

Esqueceu o commit? A rota até responde 201, mas **nada é salvo**. Quando a
sessão fecha, a mudança some. Esse é um dos erros mais comuns de quem está
começando.

> Commit é uma **transação**: ou entra tudo, ou não entra nada. Se você muda 3
> coisas e o commit falha, nenhuma das 3 é salva. É o "A" de **ACID**
> (Atomicidade).

## Refresh

**Recarrega o objeto com os dados que estão no banco.**

Por que precisamos dele? Porque **quem gera o `id` e o `criada_em` é o
banco**, não o seu código:

```python
nova = models.Task(titulo="Estudar")
print(nova.id)       # None → o banco ainda não sabe dessa tarefa

db.add(nova)
db.commit()          # o banco grava e gera id = 1
db.refresh(nova)     # busca de volta os valores gerados

print(nova.id)       # 1 ✅
```

Sem o refresh, a resposta da API poderia sair com dados desatualizados.

> 💡 Curiosidade: depois do commit, o SQLAlchemy muitas vezes recarrega o
> objeto sozinho na primeira vez que você acessa um atributo. O `refresh`
> deixa isso **explícito**. É boa prática e deixa claro o que o código faz.

## O fluxo completo no POST

```python
@app.post("/tasks", status_code=201, response_model=TaskOut)
def criar_tarefa(tarefa: TaskCreate, db: Session = Depends(get_db)):
    nova = models.Task(titulo=tarefa.titulo, descricao=tarefa.descricao)  # 1. cria o objeto
    db.add(nova)       # 2. coloca na sessão
    db.commit()        # 3. grava no banco (gera o id)
    db.refresh(nova)   # 4. recarrega com o id e o criada_em
    return nova        # 5. devolve; o Pydantic converte para JSON
```

## 🎯 Resposta de entrevista

> "A sessão é a unidade de trabalho com o banco: ela acumula as mudanças. O
> commit confirma essas mudanças numa transação, então ou entra tudo ou nada.
> O refresh recarrega o objeto com o que está no banco, o que é útil para
> pegar valores gerados lá, como o id. No meu projeto cada requisição abre a
> própria sessão via `Depends(get_db)` e ela é sempre fechada no `finally`."
