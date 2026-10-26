# 13 · Relacionamento 1:N e chave estrangeira

## 1:N (um para muitos)

**Um** usuário tem **muitas** tarefas. **Cada** tarefa tem **um** dono.

```
users                         tasks
┌────┬────────────────┐       ┌────┬──────────────────┬─────────┐
│ id │ email          │       │ id │ titulo           │ user_id │
├────┼────────────────┤       ├────┼──────────────────┼─────────┤
│ 1  │ ana@teste.com  │◀──┬───│ 1  │ Tarefa da Ana 1  │ 1       │
│ 2  │ beto@teste.com │◀┐ └───│ 2  │ Tarefa da Ana 2  │ 1       │
└────┴────────────────┘ └─────│ 3  │ Tarefa do Beto   │ 2       │
                              └────┴──────────────────┴─────────┘
```

A coluna `user_id` é a **chave estrangeira (foreign key)**: ela aponta para o
`id` de outra tabela. **O lado "N" é que guarda a referência**: a tarefa sabe
quem é o dono, e o usuário não guarda uma lista de ids.

## No projeto ([app/models.py](../app/models.py))

```python
class Task(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    dono: Mapped["User"] = relationship(back_populates="tarefas")

class User(Base):
    tarefas: Mapped[list["Task"]] = relationship(back_populates="dono", cascade="all, delete-orphan")
```

| Linha | O que faz |
|---|---|
| `ForeignKey("users.id")` | cria a coluna e a regra no **banco** |
| `index=True` | deixa rápido o `WHERE user_id = ...`, que roda em toda listagem |
| `relationship(...)` | atalho no **Python**: `tarefa.dono` e `usuario.tarefas` |
| `back_populates` | liga os dois lados: mudar um atualiza o outro |
| `cascade="all, delete-orphan"` | apagar o usuário apaga as tarefas dele |

> `ForeignKey` é coisa do **banco** (vira uma coluna). `relationship` é coisa
> do **Python** (não vira coluna, é só uma conveniência do ORM).

## Integridade referencial

A chave estrangeira garante que **não existe tarefa órfã**, ou seja, uma
tarefa com `user_id = 999` quando o usuário 999 não existe.

⚠️ **Pegadinha do SQLite:** ele vem com essa verificação **desligada**. Por
isso [app/database.py](../app/database.py) liga em toda conexão:

```python
@event.listens_for(engine, "connect")
def ligar_chaves_estrangeiras(conexao, _):
    conexao.execute("PRAGMA foreign_keys = ON")
```

No teste, inserir uma tarefa com `user_id = 999` deu `IntegrityError` ✅
(PostgreSQL e MySQL já vêm com isso ligado.)

## E se o banco já existisse?

O `create_all` **só cria tabelas que não existem**. Ele não acrescenta a
coluna `user_id` numa tabela `tasks` que já existe. Nesta etapa o `tarefas.db`
ainda não existia, então ele nasceu com a estrutura nova. Se existisse, em
desenvolvimento bastaria apagar o arquivo. Em produção, ninguém apaga o banco: usam-se
**migrations**, com o **Alembic**, que alteram a tabela mantendo os dados.

## 🎯 Resposta de entrevista

> "Usuário e tarefa têm relacionamento 1:N. A tabela de tarefas tem uma chave
> estrangeira user_id apontando para users.id, com índice porque toda
> listagem filtra por ela. No SQLAlchemy uso relationship com back_populates
> para navegar dos dois lados e cascade para apagar as tarefas junto com o
> usuário. No SQLite precisei ligar o PRAGMA foreign_keys, que vem desligado.
> Para alterar tabelas em produção eu usaria migrations com Alembic."
