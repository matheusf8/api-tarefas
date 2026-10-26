import { useState } from "react";

import Login from "./components/Login.jsx";
import Tarefas from "./components/Tarefas.jsx";

export default function App() {
  // o token fica salvo no navegador: ao recarregar a página você continua logado
  const [token, setToken] = useState(() => localStorage.getItem("token"));

  function entrar(novoToken) {
    localStorage.setItem("token", novoToken);
    setToken(novoToken);
  }

  function sair() {
    localStorage.removeItem("token");
    setToken(null);
  }

  // sem token mostra o login; com token mostra as tarefas
  return (
    <main className="container">
      <h1>✅ Minhas Tarefas</h1>
      {token ? <Tarefas token={token} onSair={sair} /> : <Login onEntrar={entrar} />}
    </main>
  );
}
