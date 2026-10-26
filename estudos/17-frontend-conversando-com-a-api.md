# 17 · Frontend conversando com a API: fetch, token e CORS

## Tudo num arquivo só: `api.js`

[frontend/src/api.js](../frontend/src/api.js) concentra **todas** as chamadas
ao backend. Os componentes só fazem `await criarTarefa(token, titulo)`, sem
saber de URL, header ou JSON.

Vantagem: se a URL da API mudar (por exemplo, no deploy), você muda **uma
linha** (`API_URL`).

## fetch

`fetch` é a função do navegador para fazer requisições HTTP:

```js
const resposta = await fetch("http://127.0.0.1:8000/tasks", {
  method: "POST",
  headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
  body: JSON.stringify({ titulo: "Estudar" }),
});
const dados = await resposta.json();
```

⚠️ **Pegadinha:** o `fetch` **não dá erro** em 401, 404 ou 422. Ele só falha se
a rede cair. Por isso o `api.js` confere o `resposta.ok` (status 200 a 299) e
lança um `ErroApi` com o status quando não está ok.

## async / await

Chamadas de rede demoram. `await` significa "espere a resposta antes de
seguir", sem travar a página. Só funciona dentro de uma função `async`. Os
erros são pegos com `try/catch`, como no Python.

## O token no navegador

| Momento | O que acontece |
|---|---|
| Login | a API devolve o token e o `App` salva no `localStorage` |
| Cada requisição | o `api.js` manda `Authorization: Bearer <token>` |
| Recarregar a página | o `App` lê o token do `localStorage`, então você continua logado |
| Token vencido (401) | o `Tarefas` chama `onSair()` e volta para o login |
| Sair | apaga o token do `localStorage` |

> ⚠️ O `localStorage` é simples e ótimo para estudo, mas qualquer script que
> rode na página consegue ler o token. Em sistemas maiores, é comum guardar o
> token num **cookie httpOnly**, que o JavaScript não acessa. É um bom ponto
> para citar em entrevista: mostra que você conhece o trade-off.

## Login é formulário, cadastro é JSON

```js
// cadastro: JSON
body: JSON.stringify({ email, senha })

// login: formulário (padrão OAuth2, o e-mail vai no campo "username")
body: new URLSearchParams({ username: email, password: senha })
```

## CORS

O React roda em `http://localhost:5173` e a API em `http://127.0.0.1:8000`.
Portas diferentes significam **origens diferentes**. Por segurança, o navegador
**bloqueia** uma página de chamar outra origem, a menos que a API autorize.

```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Pontos importantes:
- **Quem bloqueia é o navegador**, não a API. Por isso o curl e o pytest
  funcionavam sem CORS.
- Liste **as origens exatas**. `allow_origins=["*"]` libera qualquer site e é
  má prática fora de testes.
- Antes de um POST com JSON ou com header `Authorization`, o navegador manda
  um **preflight** (`OPTIONS`) perguntando "posso?". O middleware responde
  essa pergunta.

## 🎯 Resposta de entrevista

> "Centralizei as chamadas num módulo api.js com fetch. Como o fetch não lança
> erro em 4xx, eu checo resposta.ok e lanço um erro com o status. Assim a tela
> trata o 401 deslogando o usuário. O token fica no localStorage e vai no
> header Authorization; sei que um cookie httpOnly seria mais seguro contra
> XSS. Como front e back rodam em origens diferentes, configurei o CORS no
> FastAPI liberando só a origem do frontend."
