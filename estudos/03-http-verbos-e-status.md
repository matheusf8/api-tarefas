# 03 · Verbos HTTP e status codes

## CRUD ↔ verbos HTTP

| Ação (CRUD) | Verbo    | Rota no projeto  | Sucesso |
|-------------|----------|------------------|---------|
| **C**reate  | `POST`   | `/tasks`         | **201** |
| **R**ead    | `GET`    | `/tasks`, `/tasks/{id}` | 200 |
| **U**pdate  | `PUT`    | `/tasks/{id}`    | 200     |
| **D**elete  | `DELETE` | `/tasks/{id}`    | **204** |

> **PUT × PATCH:** o `PUT` substitui o recurso inteiro (por isso o
> `TaskUpdate` exige todos os campos). O `PATCH` altera só os campos enviados.

## Status codes que você precisa saber

Pelo primeiro dígito: **2xx** = deu certo · **4xx** = erro de quem chamou ·
**5xx** = erro do servidor.

| Código | Nome | Quando |
|--------|------|--------|
| 200 | OK | Deu certo e tem resposta |
| 201 | Created | Algo novo foi criado (POST) |
| 204 | No Content | Deu certo, sem corpo de resposta (DELETE) |
| 400 | Bad Request | Pedido inválido por regra de negócio |
| 401 | Unauthorized | **Não sei quem você é** (sem token, ou token inválido) |
| 403 | Forbidden | **Sei quem você é, mas você não pode** |
| 404 | Not Found | Não existe |
| 422 | Unprocessable Entity | Dados no formato errado (o FastAPI/Pydantic gera sozinho) |
| 500 | Internal Server Error | Bug no servidor |

## Path param × query param × body

```
PUT /tasks/3?debug=true        { "titulo": "Estudar", "concluida": true }
         └┬┘ └────┬───┘         └──────────────────┬─────────────────┘
      path param  query param                    body (JSON)
```

- **Path param** (`/tasks/{id}`): identifica **qual** recurso.
- **Query param** (`?concluida=true`): filtros e opções. Vem na Etapa 3.
- **Body**: os **dados** enviados (POST e PUT).

O 422 da Etapa 1 mostrou de onde veio cada erro: `"loc": ["body", "titulo"]`
apontou para o corpo e `"loc": ["path", "id"]` para a URL.

## 🎯 Resposta de entrevista

> "Uso POST para criar e respondo 201, GET para ler, PUT para atualizar e
> DELETE para apagar, com 204 porque não há corpo. Para erros: 404 quando o
> recurso não existe, 422 quando o formato dos dados está errado, 401 quando
> falta autenticação e 403 quando o usuário está autenticado mas não tem
> permissão."
