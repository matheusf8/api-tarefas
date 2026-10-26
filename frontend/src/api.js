// Todas as conversas com o backend ficam neste arquivo.
// Os componentes só chamam estas funções e não precisam saber de URL nem de header.

const API_URL = "http://127.0.0.1:8000";

// Erro com o status HTTP junto, para a tela saber se foi 401, 409...
export class ErroApi extends Error {
  constructor(status, mensagem) {
    super(mensagem);
    this.status = status;
  }
}

async function requisicao(caminho, { token, ...opcoes } = {}) {
  const headers = { ...opcoes.headers };
  if (token) headers.Authorization = `Bearer ${token}`;

  const resposta = await fetch(`${API_URL}${caminho}`, { ...opcoes, headers });

  if (resposta.status === 204) return null; // apagou: não tem corpo

  const dados = await resposta.json();
  if (!resposta.ok) {
    // o FastAPI manda o erro em "detail": às vezes um texto, às vezes uma lista (422)
    const mensagem = Array.isArray(dados.detail) ? dados.detail[0].msg : dados.detail;
    throw new ErroApi(resposta.status, mensagem);
  }
  return dados;
}

// ---------- usuários ----------

export function cadastrar(email, senha) {
  return requisicao("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, senha }),
  });
}

export async function login(email, senha) {
  // o /login segue o padrão OAuth2: formulário, com o e-mail no campo "username"
  const dados = await requisicao("/login", {
    method: "POST",
    body: new URLSearchParams({ username: email, password: senha }),
  });
  return dados.access_token;
}

export function buscarUsuario(token) {
  return requisicao("/me", { token });
}

// ---------- tarefas ----------

export function listarTarefas(token, concluida) {
  // concluida: true, false ou null (todas)
  const filtro = concluida === null ? "" : `&concluida=${concluida}`;
  return requisicao(`/tasks?limit=100${filtro}`, { token });
}

export function criarTarefa(token, titulo, descricao) {
  return requisicao("/tasks", {
    method: "POST",
    token,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ titulo, descricao: descricao || null }),
  });
}

export function editarTarefa(token, tarefa) {
  return requisicao(`/tasks/${tarefa.id}`, {
    method: "PUT",
    token,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      titulo: tarefa.titulo,
      descricao: tarefa.descricao,
      concluida: tarefa.concluida,
    }),
  });
}

export function apagarTarefa(token, id) {
  return requisicao(`/tasks/${id}`, { method: "DELETE", token });
}
