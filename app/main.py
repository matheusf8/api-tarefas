from fastapi import FastAPI, HTTPException

from app.schemas import TaskCreate, TaskUpdate, TaskOut

app = FastAPI()

tarefas = []
proximo_id = 1


@app.get("/")
def retorna():
    return {"status": "ok"}


@app.post("/tasks", status_code=201, response_model=TaskOut)
def criar_tarefa(tarefa: TaskCreate):
    global proximo_id

    nova = {
        "id": proximo_id,
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "concluida": False,
    }
    tarefas.append(nova)
    proximo_id += 1
    return nova


@app.get("/tasks", response_model=list[TaskOut])
def listar_tarefas():
    return tarefas


@app.get("/tasks/{id}", response_model=TaskOut)
def buscar_tarefa(id: int):
    for t in tarefas:
        if t["id"] == id:
            return t
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


@app.put("/tasks/{id}", response_model=TaskOut)
def editar_tarefa(id: int, dados: TaskUpdate):
    for t in tarefas:
        if t["id"] == id:
            t["titulo"] = dados.titulo
            t["descricao"] = dados.descricao
            t["concluida"] = dados.concluida
            return t
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


@app.delete("/tasks/{id}", status_code=204)
def apagar_tarefa(id: int):
    for t in tarefas:
        if t["id"] == id:
            tarefas.remove(t)
            return
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")