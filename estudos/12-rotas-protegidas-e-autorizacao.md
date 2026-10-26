# 12 · Rotas protegidas e autorização

## Autenticação × autorização

| | Pergunta | Erro quando falha | No projeto |
|---|---|---|---|
| **Autenticação** | **Quem é você?** | **401** | o token é válido? |
| **Autorização** | **Você pode mexer nisso?** | 403 (ou 404) | a tarefa é sua? |

## Como uma rota fica protegida

Basta pedir o usuário logado como dependência:

```python
@router.get("", response_model=list[TaskOut])
def listar_tarefas(
    usuario: models.User = Depends(get_usuario_logado),   # ← isso protege a rota
    db: Session = Depends(get_db),
):
```

O que o `get_usuario_logado` faz ([app/auth.py](../app/auth.py)), passo a passo:

```
Requisição chega com  Authorization: Bearer eyJhbGci...
  │
  ├─ 1. oauth2_scheme lê o header ─── não tem header? ───────▶ 401 "Not authenticated"
  ├─ 2. jwt.decode confere a assinatura ── adulterado? ───────▶ 401
  │                    e o exp ─────────── vencido? ──────────▶ 401
  ├─ 3. pega o "sub" (id do usuário)
  ├─ 4. busca o usuário no banco ───────── não existe mais? ──▶ 401
  └─ 5. entrega o objeto User para a rota ✅
```

A rota **nem chega a rodar** se o token não passar. Você protege uma rota
nova só acrescentando um parâmetro.

## Cada usuário só vê o que é seu

**Listar:** o filtro pelo dono vem **sempre**, antes de qualquer outro:

```python
consulta = db.query(models.Task).filter(models.Task.user_id == usuario.id)
```

**Buscar, editar, apagar:** a função auxiliar confere o dono:

```python
def buscar_tarefa_do_usuario(id, usuario, db):
    tarefa = db.get(models.Task, id)
    if tarefa is None or tarefa.user_id != usuario.id:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa
```

**Criar:** o `user_id` vem do **token**, nunca do corpo da requisição. Se
viesse do JSON, qualquer um criaria tarefas no nome de outra pessoa.

## Por que 404 e não 403 na tarefa de outro usuário?

Com 403, o Beto descobriria que **a tarefa 1 existe** ("existe, mas não é
sua"). Testando ids 1, 2, 3... ele mapearia quantas tarefas o sistema tem.
Com 404, para ele a tarefa da Ana **simplesmente não existe**. É a mesma ideia
da mensagem única no login.

> **IDOR (Insecure Direct Object Reference)** é o nome da falha que isso
> evita: trocar o id na URL e acessar dados de outra pessoa. É uma das falhas
> mais comuns em APIs reais e pergunta frequente em entrevista.

## Testes que provam (Etapa 5)

| Cenário | Resultado |
|---|---|
| Sem token / token inventado / outra chave / vencido / usuário inexistente | 401 |
| Beto busca, edita e apaga a tarefa 1 da Ana | 404 nos três |
| Ana busca a tarefa 1 depois disso | 200, intacta |

## 🎯 Resposta de entrevista

> "Autenticação é saber quem é o usuário, e falha com 401. Autorização é
> saber se ele pode acessar aquele recurso. Protejo as rotas com uma
> dependência `get_usuario_logado`, que valida o JWT e devolve o usuário. As
> consultas sempre filtram pelo id do usuário logado, e o dono da tarefa vem
> do token, nunca do corpo da requisição. Se alguém tenta acessar a tarefa de
> outro, devolvo 404 em vez de 403 para não revelar que ela existe. Isso
> previne IDOR."
