import { useEffect, useState } from "react";

import { apagarTarefa, buscarUsuario, editarTarefa, listarTarefas } from "../api.js";
import NovaTarefa from "./NovaTarefa.jsx";
import TarefaItem from "./TarefaItem.jsx";

const FILTROS = [
  { rotulo: "Todas", valor: null },
  { rotulo: "Pendentes", valor: false },
  { rotulo: "Concluídas", valor: true },
];

export default function Tarefas({ token, onSair }) {
  const [tarefas, setTarefas] = useState([]);
  const [filtro, setFiltro] = useState(null);
  const [email, setEmail] = useState("");
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  // token vencido ou inválido (401): volta para a tela de login
  function tratarErro(e) {
    if (e.status === 401) onSair();
    else setErro(e.message || "Não foi possível conectar à API.");
  }

  async function carregar() {
    try {
      setTarefas(await listarTarefas(token, filtro));
      setErro("");
    } catch (e) {
      tratarErro(e);
    } finally {
      setCarregando(false);
    }
  }

  // roda ao abrir a tela e sempre que o filtro mudar
  useEffect(() => {
    carregar();
  }, [filtro]);

  // busca o e-mail do usuário uma vez, para mostrar no topo
  useEffect(() => {
    buscarUsuario(token)
      .then((usuario) => setEmail(usuario.email))
      .catch(tratarErro);
  }, []);

  async function alternarConcluida(tarefa) {
    try {
      await editarTarefa(token, { ...tarefa, concluida: !tarefa.concluida });
      carregar();
    } catch (e) {
      tratarErro(e);
    }
  }

  async function apagar(id) {
    if (!confirm("Apagar esta tarefa?")) return;
    try {
      await apagarTarefa(token, id);
      carregar();
    } catch (e) {
      tratarErro(e);
    }
  }

  return (
    <section className="cartao">
      <div className="topo">
        <span className="usuario">{email}</span>
        <button className="link" onClick={onSair}>
          Sair
        </button>
      </div>

      <NovaTarefa token={token} onCriada={carregar} onErro={tratarErro} />

      <div className="filtros">
        {FILTROS.map((f) => (
          <button
            key={f.rotulo}
            className={filtro === f.valor ? "ativo" : ""}
            onClick={() => setFiltro(f.valor)}
          >
            {f.rotulo}
          </button>
        ))}
      </div>

      {erro && <p className="erro">{erro}</p>}

      {carregando ? (
        <p className="vazio">Carregando...</p>
      ) : tarefas.length === 0 ? (
        <p className="vazio">Nenhuma tarefa por aqui.</p>
      ) : (
        <ul className="lista">
          {tarefas.map((tarefa) => (
            <TarefaItem
              key={tarefa.id}
              tarefa={tarefa}
              onAlternar={alternarConcluida}
              onApagar={apagar}
            />
          ))}
        </ul>
      )}
    </section>
  );
}
