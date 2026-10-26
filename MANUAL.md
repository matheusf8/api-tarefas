# 📘 Manual: Minhas Tarefas

Sistema de lista de tarefas com contas de usuário. Cada pessoa cria a sua
conta e vê **só as próprias tarefas**.

- **Backend (API):** Python + FastAPI + SQLite, na porta **8000**
- **Frontend (tela):** React + Vite, na porta **5173**

Sumário:
1. [O que você precisa ter instalado](#1-o-que-você-precisa-ter-instalado)
2. [Preparar o projeto (só na primeira vez)](#2-preparar-o-projeto-só-na-primeira-vez)
3. [Executar o sistema (todo dia)](#3-executar-o-sistema-todo-dia)
4. [Como usar a tela](#4-como-usar-a-tela)
5. [Usar a API direto pelo /docs](#5-usar-a-api-direto-pelo-docs)
6. [Rodar os testes automatizados](#6-rodar-os-testes-automatizados)
7. [Problemas comuns](#7-problemas-comuns)
8. [Onde fica cada coisa](#8-onde-fica-cada-coisa)

---

## 1. O que você precisa ter instalado

| Programa | Versão | Como conferir |
|---|---|---|
| Python | 3.10 ou mais nova | `python --version` |
| Node.js | 22 ou mais nova | `node --version` |
| Git | qualquer | `git --version` |

Os comandos deste manual são para o **PowerShell** (Windows).

---

## 2. Preparar o projeto (só na primeira vez)

Abra o PowerShell **na pasta do projeto** (`projeto-simples-1.0`).

### 2.1 Backend

**a) Criar o ambiente virtual**

```powershell
python -m venv venv
```

**b) Ativar o ambiente virtual.** Vai aparecer `(venv)` no começo da linha.

```powershell
.\venv\Scripts\Activate.ps1
```

**c) Instalar as bibliotecas do Python**

```powershell
pip install -r requirements.txt
```

**d) Criar o arquivo `.env`** com a chave secreta. Primeiro copie o modelo:

```powershell
Copy-Item .env.example .env
```

Depois gere uma chave aleatória:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Abra o arquivo `.env` e troque `troque-por-uma-chave-secreta` pela chave que
apareceu. Salve.

> ⚠️ O `.env` **nunca** vai para o GitHub (ele está no `.gitignore`). Cada
> máquina tem o seu.

### 2.2 Frontend

```powershell
cd frontend
```

```powershell
npm install
```

```powershell
cd ..
```

Pronto! Isso só precisa ser feito uma vez.

---

## 3. Executar o sistema (todo dia)

Você vai precisar de **dois terminais abertos ao mesmo tempo**: um para a API
e outro para a tela.

### Terminal 1: API (backend)

Na pasta do projeto:

```powershell
.\venv\Scripts\Activate.ps1
```

```powershell
uvicorn app.main:app --reload
```

Deixe esse terminal aberto. Deve aparecer
`Uvicorn running on http://127.0.0.1:8000`.

> Na primeira vez, o arquivo `tarefas.db` (o banco) é criado sozinho.

### Terminal 2: tela (frontend)

Abra **outro** terminal, na pasta do projeto:

```powershell
cd frontend
```

```powershell
npm run dev
```

Deixe esse terminal aberto também. Deve aparecer `Local: http://localhost:5173/`.

### Abrir no navegador

👉 **http://localhost:5173**

### Para desligar

Em cada um dos dois terminais, aperte **Ctrl + C**.

---

## 4. Como usar a tela

### Criar conta
1. Na tela inicial, clique em **"Não tem conta? Cadastre-se"**.
2. Digite seu **e-mail** e uma **senha de no mínimo 8 caracteres**.
3. Clique em **Cadastrar**. Você já entra direto.

### Entrar
1. Digite e-mail e senha e clique em **Entrar**.
2. Se aparecer *"E-mail ou senha incorretos"*, confira os dados. Por
   segurança, o sistema não diz qual dos dois está errado.

### Adicionar uma tarefa
1. Escreva o que precisa fazer no campo **"O que você precisa fazer?"**.
2. Se quiser, preencha a **descrição**, que é opcional.
3. Clique em **Adicionar** ou aperte **Enter**.

### Concluir uma tarefa
- Clique na **caixinha ☐** ao lado da tarefa. Ela fica ~~riscada~~.
- Clicou sem querer? Clique de novo e ela volta a ficar pendente.

### Filtrar
Use os botões acima da lista:
- **Todas:** mostra tudo.
- **Pendentes:** só o que falta fazer.
- **Concluídas:** só o que já foi feito.

### Apagar uma tarefa
- Clique na **lixeira 🗑️** e confirme. ⚠️ Não dá para desfazer.

### Sair
- Clique em **Sair**, no canto superior direito.

### Bom saber
- Se você **fechar o navegador e voltar**, continua logado.
- Por segurança, o login **expira em 30 minutos**. Depois disso, o sistema
  volta sozinho para a tela de entrar. É só entrar de novo.
- O tempo pode ser mudado no `.env` (`ACCESS_TOKEN_EXPIRE_MINUTES`).

---

## 5. Usar a API direto pelo /docs

Com o backend rodando, abra **http://127.0.0.1:8000/docs**. É a documentação
automática da API, e dá para testar tudo por ali.

1. Em **POST /register**, clique em **Try it out**, preencha e clique em **Execute**.
2. Clique no botão **Authorize 🔒** no topo da página.
3. Em `username` coloque o **e-mail** e em `password` a senha. Clique em
   **Authorize** e depois em **Close**.
4. Pronto: as rotas de `/tasks` agora funcionam com o seu usuário.

| Rota | O que faz |
|---|---|
| `POST /register` | cria uma conta |
| `POST /login` | faz login e devolve o token |
| `GET /me` | mostra quem está logado |
| `POST /tasks` | cria uma tarefa |
| `GET /tasks` | lista as tarefas (aceita `?concluida=true`, `?skip=0&limit=10`) |
| `GET /tasks/{id}` | busca uma tarefa |
| `PUT /tasks/{id}` | edita uma tarefa |
| `DELETE /tasks/{id}` | apaga uma tarefa |

---

## 6. Rodar os testes automatizados

Com o ambiente virtual ativado, na pasta do projeto:

```powershell
pytest
```

Devem aparecer **24 passed**. Os testes usam um banco próprio, só em memória,
então **não mexem** no seu `tarefas.db`.

Para ver o nome de cada teste:

```powershell
pytest -v
```

---

## 7. Problemas comuns

**❌ "a execução de scripts foi desabilitada neste sistema" ao ativar o venv**

O Windows bloqueia scripts por padrão. Rode uma vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**❌ `KeyError: 'SECRET_KEY'` ao subir a API**

Falta o arquivo `.env`. Refaça o passo **2.1 d**.

**❌ `ModuleNotFoundError: No module named 'fastapi'` (ou outro)**

O ambiente virtual não está ativado. Confira se aparece `(venv)` na linha do
terminal. Se não aparecer, rode `.\venv\Scripts\Activate.ps1`.

**❌ Na tela: "Não foi possível conectar à API. Ela está rodando?"**

O Terminal 1 (backend) não está rodando, ou foi fechado. Veja o passo 3.

**❌ `'uvicorn' não é reconhecido` / `'npm' não é reconhecido`**

- uvicorn: ative o venv.
- npm: instale o Node.js e **reabra** o terminal.

**❌ Erro de CORS no console do navegador**

Abra a tela **exatamente** em `http://localhost:5173`. A API só aceita essa
origem (e `127.0.0.1:5173`).

**❌ Porta já em uso (`address already in use`)**

Já tem um servidor rodando na mesma porta, provavelmente num terminal
esquecido. Feche-o com **Ctrl + C** ou feche o terminal.

**🔄 Quero começar com o banco zerado**

Desligue a API e apague o arquivo `tarefas.db`. Ao subir de novo, ele é
recriado vazio. ⚠️ Isso apaga **todas** as contas e tarefas.

---

## 8. Onde fica cada coisa

```
projeto-simples-1.0/
├── app/                    # BACKEND (Python)
│   ├── main.py             #   cria a API, liga o CORS e junta as rotas
│   ├── database.py         #   conexão com o banco SQLite
│   ├── models.py           #   tabelas: users e tasks
│   ├── schemas.py          #   formato dos dados que entram e saem
│   ├── auth.py             #   senhas (bcrypt) e tokens (JWT)
│   └── routers/
│       ├── users.py        #   /register, /login, /me
│       └── tasks.py        #   /tasks
├── tests/                  # TESTES (pytest)
├── frontend/               # FRONTEND (React)
│   └── src/
│       ├── api.js          #   todas as chamadas para a API
│       ├── App.jsx         #   decide: tela de login ou de tarefas
│       ├── index.css       #   visual (cores no topo do arquivo)
│       └── components/     #   Login, Tarefas, NovaTarefa, TarefaItem
├── estudos/                # explicação de cada conceito usado
├── .env.example            # modelo do .env
├── requirements.txt        # bibliotecas do Python
├── README.md               # apresentação do projeto
└── MANUAL.md               # este arquivo
```

Quer entender **como** cada parte funciona? Veja a pasta
[estudos/](estudos/README.md).
