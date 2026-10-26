from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    titulo: str
    descricao: str | None = None


class TaskUpdate(BaseModel):
    titulo: str
    descricao: str | None = None
    concluida: bool


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descricao: str | None = None
    concluida: bool
    criada_em: datetime
