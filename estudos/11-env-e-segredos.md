# 11 · `.env` e segredos

## O problema

A `SECRET_KEY` assina todos os tokens. **Quem tiver essa chave consegue criar
um token de qualquer usuário.** Se ela estiver escrita no código e o código
for para o GitHub, qualquer pessoa no mundo pode entrar na conta de qualquer
usuário.

## A solução: variáveis de ambiente

O segredo fica **fora do código**, num arquivo `.env` que **não vai para o
Git**:

```
# .env  (só na sua máquina, está no .gitignore)
SECRET_KEY=a3f9c1...64 caracteres aleatórios...
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

O código só **lê** o valor ([app/auth.py](../app/auth.py)):

```python
from dotenv import load_dotenv
load_dotenv()                                  # lê o .env e põe no ambiente

SECRET_KEY = os.environ["SECRET_KEY"]          # obrigatória: sem ela o app nem sobe
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))  # opcional, padrão 30
```

| Forma | Se a variável não existir |
|---|---|
| `os.environ["X"]` | **erro na hora** (bom para o que é obrigatório) |
| `os.getenv("X", "padrão")` | usa o valor padrão |

Usar `os.environ` na `SECRET_KEY` é de propósito: é melhor o app **nem subir**
do que subir com uma chave vazia ou previsível.

## `.env.example`

O `.env` não vai para o GitHub. Como quem clonar o projeto vai saber quais
variáveis precisa? Pelo **`.env.example`**, que **vai** para o Git, com valores
de mentira:

```
SECRET_KEY=troque-por-uma-chave-secreta
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Quem clona copia para `.env` e gera a própria chave:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

> 32 bytes = 64 caracteres hexadecimais. É o tamanho recomendado para HS256.

## Em produção

No Render, na Vercel e afins, não existe arquivo `.env`: você cadastra as
variáveis no painel do serviço. O código não muda, porque o `os.environ` lê
de onde quer que elas estejam.

## 🎯 Resposta de entrevista

> "Segredos como a chave do JWT ficam em variáveis de ambiente, nunca no
> código. Localmente uso um .env que está no .gitignore, e deixo um
> .env.example no repositório mostrando quais variáveis são necessárias. Em
> produção cadastro as variáveis no painel do provedor. A chave é
> obrigatória: se ela faltar, o app falha ao iniciar, em vez de rodar inseguro."
