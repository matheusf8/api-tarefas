# 09 · Hash de senha (bcrypt)

## A regra de ouro

**Nunca guarde a senha. Guarde o hash dela.**

Se o banco vazar e as senhas estiverem em texto puro, o atacante tem a senha
de todo mundo. E como muita gente repete a mesma senha, ele tem também o
e-mail, o banco e o Instagram dessas pessoas.

## O que é um hash

Uma função que transforma um texto num "resumo" embaralhado, **de mão única**:

```
"senha1234"  ──hash──▶  "$2b$12$Z5WAAmMt.Fex5uPs.pny5u59gt6Wdf7Qj22eH..."
"$2b$12$..." ──✗──▶     não dá para voltar para "senha1234"
```

| Criptografia | Hash |
|---|---|
| Vai e **volta** (com a chave) | **Só vai** |
| Para dados que você vai ler de novo | Para senhas |

## Como o login confere a senha, então?

O sistema **não "desfaz" o hash**. Ele calcula o hash da senha digitada e
compara com o que está guardado:

```python
def verificar_senha(senha: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))
```

## Por que bcrypt e não SHA-256?

1. **Salt (sal):** o bcrypt mistura um valor aleatório em cada hash. Duas
   pessoas com a senha `123456` ficam com hashes **diferentes**. Isso derruba
   as "rainbow tables", listas prontas de hashes de senhas comuns.
2. **É lento de propósito:** o `12` em `$2b$12$` é o **custo**. Cada tentativa
   leva milissegundos, o que não faz diferença para o usuário, mas torna
   inviável testar bilhões de senhas por força bruta. O SHA-256 é rápido
   demais para senhas.

Anatomia do hash guardado no banco:

```
$2b$12$Z5WAAmMt.Fex5uPs.pny5u59gt6Wdf7Qj22eHlbvxNxl0d.ybCP6C
 └┬┘ └┬┘└─────────┬──────────┘└──────────────┬─────────────┘
 versão custo   salt (22 caracteres)       o hash em si
```

O salt fica **junto** do hash, por isso o `checkpw` não precisa de mais nada.

## Limite de 72 bytes

O bcrypt só usa os primeiros 72 **bytes** da senha, e a versão 5 da biblioteca
dá erro acima disso. Por isso o `UserCreate` recusa senhas maiores, devolvendo
422. Bytes não são letras: `a` ocupa 1 byte e `é` ocupa 2.

## Outros cuidados que o projeto toma

- O `UserOut` **não tem** `senha_hash`, então o hash nunca sai na resposta da API.
- O login devolve **a mesma mensagem** para e-mail inexistente e senha errada
  ("E-mail ou senha incorretos"). Se as mensagens fossem diferentes, um
  atacante descobriria quais e-mails estão cadastrados (**enumeração de usuários**).
- O e-mail é salvo em **minúsculas**, para `Matheus@` e `matheus@` não virarem
  duas contas.

## 🎯 Resposta de entrevista

> "Nunca guardo a senha, só o hash com bcrypt. Hash é de mão única: no login
> eu calculo o hash da senha digitada e comparo. Uso bcrypt porque ele tem
> salt aleatório, então senhas iguais geram hashes diferentes, e porque é
> lento de propósito, o que dificulta força bruta. Também não devolvo o hash
> na API e uso a mesma mensagem de erro no login para não revelar quais
> e-mails existem."
