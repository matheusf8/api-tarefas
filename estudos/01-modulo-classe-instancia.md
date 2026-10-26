# 01 · Módulo, classe e instância

## Os três níveis

- **Módulo:** um arquivo `.py` (ou um **pacote**, que é uma pasta de módulos)
  que organiza código. Exemplo: `fastapi`.
- **Classe:** um **molde** que define dados (atributos) e comportamentos
  (métodos). Por convenção o nome começa com maiúscula. Exemplo: `FastAPI`.
- **Instância:** um **objeto concreto** criado a partir da classe, chamando-a
  com `()`. Exemplo: `app = FastAPI()`.

## Analogia

| Conceito  | Exemplo de bolo     | No código          |
|-----------|---------------------|--------------------|
| Módulo    | Livro de receitas   | `fastapi`          |
| Classe    | A receita do bolo   | `FastAPI`          |
| Instância | O bolo pronto       | `app = FastAPI()`  |

Com uma receita você faz vários bolos: `app1 = FastAPI()` e `app2 = FastAPI()`
são duas aplicações diferentes.

## O erro que aconteceu na Etapa 0

```python
import fastapi
app = fastapi        # ❌ app virou o MÓDULO (o livro), não uma aplicação
```

```python
from fastapi import FastAPI
app = FastAPI()      # ✅ app é uma INSTÂNCIA da classe FastAPI
```

O módulo não tem o método `.get()` para criar rotas. Quem tem é a instância.

## 🎯 Resposta de entrevista

> "Módulo é um arquivo Python que organiza código e pode conter funções e
> classes. Classe é um molde que define atributos e métodos. Instância é um
> objeto concreto criado a partir da classe. Exemplo: `fastapi` é o módulo,
> `FastAPI` é a classe e `app = FastAPI()` é a instância."
