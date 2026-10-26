from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import models
from app.auth import get_usuario_logado
from app.database import get_db
from app.schemas import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tarefas"])


def buscar_tarefa_do_usuario(id: int, usuario: models.User, db: Session) -> models.Task:
    tarefa = db.get(models.Task, id)
    # tarefa de outro usuário responde 404, e não 403, para não revelar que ela existe
    if tarefa is None or tarefa.user_id != usuario.id:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


@router.post("", status_code=201, response_model=TaskOut)
def criar_tarefa(
    tarefa: TaskCreate,
    usuario: models.User = Depends(get_usuario_logado),
    db: Session = Depends(get_db),
):
    nova = models.Task(titulo=tarefa.titulo, descricao=tarefa.descricao, user_id=usuario.id)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@router.get("", response_model=list[TaskOut])
def listar_tarefas(
    concluida: bool | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    usuario: models.User = Depends(get_usuario_logado),
    db: Session = Depends(get_db),
):
    consulta = db.query(models.Task).filter(models.Task.user_id == usuario.id)
    if concluida is not None:
        consulta = consulta.filter(models.Task.concluida == concluida)
    return consulta.order_by(models.Task.id).offset(skip).limit(limit).all()


@router.get("/{id}", response_model=TaskOut)
def buscar_tarefa(
    id: int,
    usuario: models.User = Depends(get_usuario_logado),
    db: Session = Depends(get_db),
):
    return buscar_tarefa_do_usuario(id, usuario, db)


@router.put("/{id}", response_model=TaskOut)
def editar_tarefa(
    id: int,
    dados: TaskUpdate,
    usuario: models.User = Depends(get_usuario_logado),
    db: Session = Depends(get_db),
):
    tarefa = buscar_tarefa_do_usuario(id, usuario, db)
    tarefa.titulo = dados.titulo
    tarefa.descricao = dados.descricao
    tarefa.concluida = dados.concluida
    db.commit()
    db.refresh(tarefa)
    return tarefa


@router.delete("/{id}", status_code=204)
def apagar_tarefa(
    id: int,
    usuario: models.User = Depends(get_usuario_logado),
    db: Session = Depends(get_db),
):
    tarefa = buscar_tarefa_do_usuario(id, usuario, db)
    db.delete(tarefa)
    db.commit()
