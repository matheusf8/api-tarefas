export default function TarefaItem({ tarefa, onAlternar, onApagar }) {
  return (
    <li className={tarefa.concluida ? "tarefa feita" : "tarefa"}>
      <input
        type="checkbox"
        checked={tarefa.concluida}
        onChange={() => onAlternar(tarefa)}
        aria-label="Marcar como concluída"
      />
      <div className="texto">
        <strong>{tarefa.titulo}</strong>
        {tarefa.descricao && <small>{tarefa.descricao}</small>}
      </div>
      <button className="apagar" onClick={() => onApagar(tarefa.id)} aria-label="Apagar tarefa">
        🗑️
      </button>
    </li>
  );
}
