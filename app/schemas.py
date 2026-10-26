from pydantic import BaseModel


class TaskCreate(BaseModel):
    titulo: str
    descricao: str | None = None


class TaskUpdate(BaseModel):
    titulo: str
    descricao: str | None = None
    concluida: bool


class TaskOut(BaseModel):
    id: int
    titulo: str
    descricao: str | None = None
    concluida: bool