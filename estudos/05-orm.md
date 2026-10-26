# 05 · ORM (Object-Relational Mapping)

## A ideia em uma frase

ORM é uma **ponte entre o mundo do Python (classes e objetos) e o mundo do
banco (tabelas e linhas)**. Você trabalha com objetos e ele escreve o SQL.

## O problema que ele resolve

Sem ORM, para salvar uma tarefa você escreveria SQL na mão:

```python
cursor.execute(
    "INSERT INTO tasks (titulo, descricao, concluida) VALUES (?, ?, ?)",
    ("Estudar", None, False),
)
```

Com ORM (SQLAlchemy), você escreve só Python:

```python
nova = models.Task(titulo="Estudar", descricao=None)
db.add(nova)
db.commit()
```

O SQLAlchemy gera aquele `INSERT` por baixo dos panos.

## O mapeamento

| Mundo Python            | Mundo do banco       | No projeto                  |
|-------------------------|----------------------|-----------------------------|
| Classe                  | Tabela               | `class Task` → `tasks`      |
| Atributo da classe      | Coluna               | `titulo` → coluna `titulo`  |
| Objeto (instância)      | Linha (registro)     | `Task(titulo="Estudar")`    |
| Tipo Python             | Tipo SQL             | `str` → `VARCHAR`, `bool` → `BOOLEAN` |

No projeto ([app/models.py](../app/models.py)):

```python
class Task(Base):
    __tablename__ = "tasks"          # nome da tabela no banco

    id: Mapped[int] = mapped_column(primary_key=True)   # chave primária
    titulo: Mapped[str]                                 # obrigatório (NOT NULL)
    descricao: Mapped[str | None]                       # opcional (pode ser NULL)
    concluida: Mapped[bool] = mapped_column(default=False)
```

## Exemplos de "tradução"

| Python (SQLAlchemy)                  | SQL gerado                              |
|--------------------------------------|-----------------------------------------|
| `db.get(models.Task, 3)`             | `SELECT * FROM tasks WHERE id = 3`      |
| `db.query(models.Task).all()`        | `SELECT * FROM tasks`                   |
| `db.add(nova)` + `db.commit()`       | `INSERT INTO tasks (...) VALUES (...)`  |
| `tarefa.titulo = "X"` + `db.commit()`| `UPDATE tasks SET titulo='X' WHERE id=…`|
| `db.delete(tarefa)` + `db.commit()`  | `DELETE FROM tasks WHERE id = …`        |

## Vantagens e desvantagens

✅ Menos SQL repetitivo, código mais legível.
✅ Protege contra **SQL Injection**, porque os valores são sempre passados como parâmetros.
✅ Trocar de banco (SQLite → PostgreSQL) quase não muda o código.

⚠️ Esconde o SQL: em consultas complexas pode gerar SQL lento sem você perceber.
⚠️ **Não substitui saber SQL.** Quando algo dá errado, você precisa entender o SQL que foi gerado.

## 🎯 Resposta de entrevista

> "ORM é uma camada que mapeia tabelas do banco para classes da linguagem.
> Cada classe vira uma tabela, cada atributo uma coluna e cada objeto uma
> linha. No meu projeto uso o SQLAlchemy: em vez de escrever um INSERT, eu
> crio um objeto `Task`, adiciono na sessão e dou commit. Além de deixar o
> código mais limpo, ele protege contra SQL injection. Mesmo assim, é
> importante saber SQL para entender o que o ORM está fazendo."
