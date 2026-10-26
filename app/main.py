from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, get_db
from app.schemas import TaskCreate, TaskOut, TaskUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def retorna():
    return {"status": "ok"}


@app.post("/tasks", status_code=201, response_model=TaskOut)
def criar_tarefa(tarefa: TaskCreate, db: Session = Depends(get_db)):
    nova = models.Task(titulo=tarefa.titulo, descricao=tarefa.descricao)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@app.get("/tasks", response_model=list[TaskOut])
def listar_tarefas(
    concluida: bool | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    consulta = db.query(models.Task)
    if concluida is not None:
        consulta = consulta.filter(models.Task.concluida == concluida)
    return consulta.order_by(models.Task.id).offset(skip).limit(limit).all()


@app.get("/tasks/{id}", response_model=TaskOut)
def buscar_tarefa(id: int, db: Session = Depends(get_db)):
    tarefa = db.get(models.Task, id)
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


@app.put("/tasks/{id}", response_model=TaskOut)
def editar_tarefa(id: int, dados: TaskUpdate, db: Session = Depends(get_db)):
    tarefa = db.get(models.Task, id)
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefa.titulo = dados.titulo
    tarefa.descricao = dados.descricao
    tarefa.concluida = dados.concluida
    db.commit()
    db.refresh(tarefa)
    return tarefa


@app.delete("/tasks/{id}", status_code=204)
def apagar_tarefa(id: int, db: Session = Depends(get_db)):
    tarefa = db.get(models.Task, id)
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(tarefa)
    db.commit()
