import { useState } from "react";

import { cadastrar, login } from "../api.js";

export default function Login({ onEntrar }) {
  const [modo, setModo] = useState("entrar"); // "entrar" ou "cadastrar"
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const [enviando, setEnviando] = useState(false);

  async function enviar(evento) {
    evento.preventDefault(); // impede o formulário de recarregar a página
    setErro("");
    setEnviando(true);
    try {
      if (modo === "cadastrar") {
        await cadastrar(email, senha);
      }
      // depois de cadastrar, já entra direto
      const token = await login(email, senha);
      onEntrar(token);
    } catch (e) {
      setErro(e.message || "Não foi possível conectar à API. Ela está rodando?");
    } finally {
      setEnviando(false);
    }
  }

  function trocarModo() {
    setModo(modo === "entrar" ? "cadastrar" : "entrar");
    setErro("");
  }

  return (
    <form className="cartao" onSubmit={enviar}>
      <h2>{modo === "entrar" ? "Entrar" : "Criar conta"}</h2>

      <label>
        E-mail
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="voce@email.com"
          required
        />
      </label>

      <label>
        Senha
        <input
          type="password"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          placeholder="mínimo 8 caracteres"
          minLength={8}
          required
        />
      </label>

      {erro && <p className="erro">{erro}</p>}

      <button type="submit" disabled={enviando}>
        {enviando ? "Aguarde..." : modo === "entrar" ? "Entrar" : "Cadastrar"}
      </button>

      <button type="button" className="link" onClick={trocarModo}>
        {modo === "entrar" ? "Não tem conta? Cadastre-se" : "Já tem conta? Entre"}
      </button>
    </form>
  );
}
