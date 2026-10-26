# 16 · React básico: componentes, props, useState e useEffect

## A ideia do React

Você **não manda a tela mudar** ("esconde este botão, escreve aquele texto").
Você descreve **como a tela deve ser para cada estado**, e o React atualiza
sozinho quando o estado muda.

```
estado (dados)  ──▶  React desenha a tela  ──▶  usuário clica
      ▲                                              │
      └────────────── muda o estado ◀────────────────┘
```

## Componentes

Um componente é uma **função que devolve o pedaço de tela** que ela cuida
(em JSX, um "HTML dentro do JavaScript"). Nomes começam com maiúscula.

```
App                      → decide: login ou tarefas?
├── Login                → formulário de entrar/cadastrar
└── Tarefas              → a tela principal
    ├── NovaTarefa       → formulário de adicionar
    └── TarefaItem (×N)  → uma linha da lista
```

Cada arquivo em [frontend/src/components/](../frontend/src/components/) é um
componente pequeno, com uma responsabilidade só.

## Props: dados de pai para filho

Props são os **parâmetros** de um componente. O pai passa e o filho recebe:

```jsx
// o pai (Tarefas.jsx) passa:
<TarefaItem tarefa={tarefa} onAlternar={alternarConcluida} onApagar={apagar} />

// o filho (TarefaItem.jsx) recebe:
export default function TarefaItem({ tarefa, onAlternar, onApagar }) { ... }
```

Props com nome `on...` são **funções**: é assim que o filho **avisa o pai**
que algo aconteceu. O `TarefaItem` não sabe apagar nada. Ele só chama
`onApagar(id)`, e quem decide o que fazer é o `Tarefas`.

> Os dados **descem** por props e os avisos **sobem** por funções.

## useState: a memória do componente

```jsx
const [titulo, setTitulo] = useState("");
//     valor    função que   valor inicial
//     atual    troca o valor
```

- **Nunca** altere direto (`titulo = "x"` ❌). Use `setTitulo("x")` ✅.
- Toda vez que um `set...` é chamado, **o React redesenha o componente** com o
  valor novo.

**Input controlado:** o valor do campo vem do estado, e cada tecla atualiza o
estado:

```jsx
<input value={titulo} onChange={(e) => setTitulo(e.target.value)} />
```

Por isso dá para limpar o formulário com `setTitulo("")` depois de adicionar.

## useEffect: fazer algo "depois de desenhar"

Para buscar dados na API quando a tela abre:

```jsx
useEffect(() => {
  carregar();       // busca as tarefas
}, [filtro]);       // ← lista de dependências
```

| Dependências | Quando roda |
|---|---|
| `[]` | **uma vez**, quando o componente aparece |
| `[filtro]` | quando aparece **e toda vez que `filtro` mudar** |

É assim que clicar em "Concluídas" recarrega a lista: o clique muda o
`filtro`, o `filtro` mudou, e o efeito roda de novo.

> Em desenvolvimento, o `<StrictMode>` roda os efeitos **duas vezes** de
> propósito, para achar bugs. Por isso aparecem chamadas repetidas na aba
> Network. Na versão final (build) isso não acontece.

## Renderização condicional

```jsx
{token ? <Tarefas ... /> : <Login ... />}       // um ou outro
{erro && <p className="erro">{erro}</p>}        // só mostra se tiver erro
```

## Listas e `key`

```jsx
{tarefas.map((tarefa) => (
  <TarefaItem key={tarefa.id} tarefa={tarefa} ... />
))}
```

O `key` ajuda o React a saber **qual item é qual** quando a lista muda. Use
sempre um id único. O índice da lista não serve, porque ele muda quando um
item é apagado.

## 🎯 Resposta de entrevista

> "No frontend dividi a tela em componentes pequenos. Os dados descem por
> props e os eventos sobem por funções de callback, tipo onApagar. Uso
> useState para o estado local, como os campos do formulário controlados e a
> lista de tarefas, e useEffect para buscar os dados na API quando a tela
> abre e quando o filtro muda, com o filtro na lista de dependências. Nas
> listas uso o id como key."
