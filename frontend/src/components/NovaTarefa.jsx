import { useState } from "react";

import { criarTarefa } from "../api.js";

export default function NovaTarefa({ token, onCriada, onErro }) {
  const [titulo, setTitulo] = useState("");
  const [descricao, setDescricao] = useState("");

  async function enviar(evento) {
    evento.preventDefault();
    if (!titulo.trim()) return;
    try {
      await criarTarefa(token, titulo.trim(), descricao.trim());
      setTitulo(""); // limpa o formulário
      setDescricao("");
      onCriada(); // avisa a tela de tarefas para recarregar a lista
    } catch (e) {
      onErro(e);
    }
  }

  return (
    <form className="nova-tarefa" onSubmit={enviar}>
      <input
        value={titulo}
        onChange={(e) => setTitulo(e.target.value)}
        placeholder="O que você precisa fazer?"
        required
      />
      <input
        value={descricao}
        onChange={(e) => setDescricao(e.target.value)}
        placeholder="Descrição (opcional)"
      />
      <button type="submit">Adicionar</button>
    </form>
  );
}
