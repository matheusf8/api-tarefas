from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]
    descricao: Mapped[str | None]
    concluida: Mapped[bool] = mapped_column(default=False)
    criada_em: Mapped[datetime] = mapped_column(default=datetime.now)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    dono: Mapped["User"] = relationship(back_populates="tarefas")


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    senha_hash: Mapped[str]
    criado_em: Mapped[datetime] = mapped_column(default=datetime.now)

    tarefas: Mapped[list["Task"]] = relationship(back_populates="dono", cascade="all, delete-orphan")
