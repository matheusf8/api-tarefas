# 02 · Ambiente virtual (venv) e uvicorn

## venv

Uma **pasta isolada** com um Python e as bibliotecas **só deste projeto**.

- Sem venv: todos os projetos dividem as mesmas bibliotecas. Se o e-commerce
  precisa do FastAPI 0.100 e este projeto do 0.162, um quebra o outro.
- Com venv: cada projeto tem a sua "caixinha".

```powershell
python -m venv venv              # cria
.\venv\Scripts\Activate.ps1      # ativa (aparece "(venv)" no terminal)
pip install fastapi              # instala só dentro do venv
pip freeze > requirements.txt    # salva a lista exata de versões
pip install -r requirements.txt  # recria o ambiente em outra máquina
```

A pasta `venv/` **não vai para o Git** (está no `.gitignore`). Quem clona o
projeto recria o ambiente a partir do `requirements.txt`.

## uvicorn

O FastAPI **define** as rotas, mas não sabe "escutar" a rede. Quem recebe as
requisições HTTP e repassa para o FastAPI é o **uvicorn**, um **servidor
ASGI**.

```
Navegador ──HTTP──▶ uvicorn ──▶ FastAPI ──▶ sua função
```

```powershell
uvicorn app.main:app --reload
```

- `app.main` → o arquivo `app/main.py`
- `:app` → a variável `app` dentro dele
- `--reload` → reinicia sozinho quando você salva um arquivo (só em desenvolvimento)

> ASGI (Asynchronous Server Gateway Interface) é o padrão de comunicação entre
> servidor e framework Python assíncrono. É o sucessor do WSGI (Flask/Django
> clássico).

## 🎯 Resposta de entrevista

> "O venv isola as dependências de cada projeto, evitando conflito de versões.
> Eu registro as versões no requirements.txt para qualquer pessoa recriar o
> ambiente. O uvicorn é o servidor ASGI que recebe as requisições HTTP e
> repassa para o FastAPI. O FastAPI só define as rotas."
