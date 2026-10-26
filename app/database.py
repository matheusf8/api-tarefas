from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./tarefas.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


# o SQLite vem com as chaves estrangeiras desligadas; isto liga em cada conexão
@event.listens_for(engine, "connect")
def ligar_chaves_estrangeiras(conexao, _):
    conexao.execute("PRAGMA foreign_keys = ON")


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
