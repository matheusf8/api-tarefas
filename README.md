# ✅ Minhas Tarefas: API + React

Aplicação full stack de lista de tarefas com contas de usuário: cada pessoa
cria a sua conta, faz login e gerencia **só as próprias tarefas**.

Projeto de estudo feito **etapa por etapa** para fixar o básico de backend e
frontend: CRUD, banco relacional, autenticação, testes e integração com uma
tela em React.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)
![Testes](https://img.shields.io/badge/testes-24%20passando-brightgreen)

---

## Funcionalidades

- **Cadastro e login** com senha guardada como hash (bcrypt) e autenticação por **JWT**
- **CRUD de tarefas**: criar, listar, buscar, editar, concluir e apagar
- **Filtro** por concluídas/pendentes e **paginação** (`skip`/`limit`)
- **Isolamento entre usuários**: ninguém vê nem altera tarefas de outra pessoa
- **Tela em React**: login/cadastro, lista com filtros e logout automático quando o token expira
- **24 testes automatizados** com pytest, rodando num banco em memória

## Tecnologias

| Camada | Tecnologia |
|---|---|
| API | FastAPI, Pydantic, Uvicorn |
| Banco | SQLite + SQLAlchemy 2 (ORM) |
| Autenticação | PyJWT (HS256) + bcrypt |
| Testes | Pytest + TestClient |
| Frontend | React 19 + Vite, JavaScript, `fetch`, CSS puro |

## Como rodar

Resumo rápido (o passo a passo completo, com solução de problemas, está no
**[MANUAL.md](MANUAL.md)**):

```powershell
# backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env          # depois coloque uma SECRET_KEY de verdade
uvicorn app.main:app --reload        # http://127.0.0.1:8000/docs

# frontend (em outro terminal)
cd frontend
npm install
npm run dev                          # http://localhost:5173
```

Testes:

```powershell
pytest
```

## Rotas da API

| Método | Rota | Autenticação | Descrição |
|---|---|---|---|
| `POST` | `/register` | – | Cria uma conta |
| `POST` | `/login` | – | Devolve um token JWT (formulário OAuth2) |
| `GET` | `/me` | 🔒 | Dados do usuário logado |
| `POST` | `/tasks` | 🔒 | Cria uma tarefa |
| `GET` | `/tasks` | 🔒 | Lista as tarefas (`?concluida=`, `?skip=`, `?limit=`) |
| `GET` | `/tasks/{id}` | 🔒 | Busca uma tarefa |
| `PUT` | `/tasks/{id}` | 🔒 | Edita uma tarefa |
| `DELETE` | `/tasks/{id}` | 🔒 | Apaga uma tarefa |

Documentação interativa (Swagger) em `/docs`, com o botão **Authorize** funcionando.

## Decisões de segurança

- **Senhas** nunca são salvas: só o hash bcrypt, com salt. O hash nunca aparece nas respostas.
- **Login** devolve a mesma mensagem para e-mail inexistente e senha errada, para não revelar quais e-mails estão cadastrados.
- **Tarefa de outro usuário responde 404, e não 403**, para não revelar que ela existe (prevenção de IDOR).
- **O dono da tarefa vem do token**, nunca do corpo da requisição.
- **`SECRET_KEY` fica no `.env`**, fora do Git. O app nem sobe sem ela.
- **CORS** liberado só para a origem do frontend.
- **Chave estrangeira** ligada no SQLite (`PRAGMA foreign_keys = ON`), que vem desligada por padrão.

## Testes

```
tests/
├── conftest.py      # banco SQLite em memória novo para cada teste (dependency_overrides)
├── test_users.py    # cadastro, login, /me, token vencido e token falso (11 testes)
└── test_tasks.py    # CRUD, 401/404/422, filtro, paginação e isolamento (13 testes)
```

Os testes foram validados introduzindo bugs de propósito (por exemplo, tirar a
checagem de dono da tarefa). O teste correspondente falhou em cada caso.

## Estrutura

```
├── app/
│   ├── main.py            # cria o app, CORS, lifespan e routers
│   ├── database.py        # engine, sessão e get_db
│   ├── models.py          # User e Task (1:N)
│   ├── schemas.py         # entrada e saída (Pydantic)
│   ├── auth.py            # bcrypt, JWT e get_usuario_logado
│   └── routers/           # users.py e tasks.py
├── tests/
├── frontend/src/
│   ├── api.js             # todas as chamadas à API
│   ├── App.jsx
│   └── components/        # Login, Tarefas, NovaTarefa, TarefaItem
├── estudos/               # explicação de cada conceito usado no projeto
└── MANUAL.md              # instalação, uso e problemas comuns
```

## Como foi feito

O projeto foi construído em etapas, e cada uma virou um commit:

| Etapa | Conteúdo |
|---|---|
| 0 | Ambiente (venv) e primeira rota |
| 1 | CRUD em memória |
| 2 | Banco SQLite com SQLAlchemy |
| 3 | Filtro e paginação |
| 4 | Cadastro, login, bcrypt e JWT |
| 5 | Tarefas por usuário e rotas protegidas |
| 6 | Testes automatizados |
| – | Frontend em React |

Usei o **Claude Code** como apoio durante o desenvolvimento. A pasta **[estudos/](estudos/README.md)** tem
um resumo de cada conceito usado (ORM, sessão, JWT, IDOR, CORS, fixtures,
hooks do React...).

## Próximos passos

- [ ] CI no GitHub Actions rodando o pytest
- [ ] Docker
- [ ] Deploy (API no Render, frontend na Vercel)
- [ ] Editar o título da tarefa pela tela
- [ ] Migrations com Alembic

---

Feito por **Matheus Franco**: [GitHub](https://github.com/matheusf8) · [LinkedIn](https://www.linkedin.com/in/matheusfrancon)
