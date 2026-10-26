# 10 · JWT (JSON Web Token)

## O problema

O HTTP **não tem memória**: cada requisição chega sem saber nada da anterior.
Depois do login, como a API sabe que a próxima requisição é sua?

**Resposta:** no login a API te entrega um **token**, como uma pulseira de
festa. Em toda requisição seguinte você mostra a pulseira.

## O fluxo

```
1. POST /login  (e-mail + senha)        ──▶  API confere a senha
2.              ◀── { "access_token": "eyJhbGci..." }
3. GET /tasks   Header: Authorization: Bearer eyJhbGci...   ──▶  API confere o token
4.              ◀── suas tarefas
```

O passo 3 é a Etapa 5. Na Etapa 4 fizemos os passos 1 e 2.

## Anatomia de um JWT

São **3 partes separadas por ponto**, todas em Base64:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 . eyJzdWIiOiIxIiwiZXhwIjoxNzkzMDMyNjYzfQ . XQ48qdbawS1Pet7npwk...
└──────────── header ──────────────┘   └────────────── payload ─────────────┘   └── assinatura ──┘
{"alg": "HS256", "typ": "JWT"}          {"sub": "1", "exp": 1793032663}
```

- **Header:** qual algoritmo foi usado.
- **Payload:** os dados ("claims"). No projeto: `sub` = id do usuário,
  `exp` = quando expira (30 minutos).
- **Assinatura:** um "lacre" calculado a partir do header, do payload e da
  `SECRET_KEY`.

## ⚠️ JWT NÃO é criptografado

Qualquer pessoa consegue **ler** o payload. Cole um token em jwt.io e veja.
**Nunca coloque senha nem dados sensíveis no payload.**

O que o JWT garante é que **ninguém consegue alterar** o conteúdo. Se alguém
trocar `"sub": "1"` por `"sub": "2"` para se passar por outro usuário, a
assinatura deixa de bater e a API recusa. Só quem tem a `SECRET_KEY` consegue
assinar um token válido.

Nos testes da Etapa 4, conferir o token com uma chave errada deu
`InvalidSignatureError` ✅

## No projeto ([app/auth.py](../app/auth.py))

```python
def criar_token(user_id: int) -> str:
    expira_em = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados = {"sub": str(user_id), "exp": expira_em}
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)
```

- O `sub` é texto (`str`) porque a especificação do JWT pede assim.
- `timezone.utc`: o `exp` é sempre em UTC, para não depender do fuso do servidor.

## Por que o login usa formulário, e não JSON?

O `/login` usa `OAuth2PasswordRequestForm`, o **padrão OAuth2**, que manda
`username` e `password` como formulário. A vantagem é que o botão
**"Authorize" 🔒 do `/docs`** passa a funcionar sozinho. O campo se chama
`username`, mas recebe o e-mail.

## Por que o token expira?

Se um token vazar, ele só funciona por 30 minutos. Sem expiração, valeria para
sempre.

## 🎯 Resposta de entrevista

> "Depois do login a API gera um JWT assinado com uma chave secreta, contendo
> o id do usuário e a data de expiração. O cliente manda esse token no header
> Authorization em cada requisição. O JWT não é criptografado, qualquer um lê
> o payload, por isso não coloco dados sensíveis nele. O que ele garante é a
> integridade: sem a chave secreta ninguém consegue alterar o conteúdo sem
> invalidar a assinatura. Uso expiração curta para limitar o estrago se um
> token vazar."
