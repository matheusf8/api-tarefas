from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import tasks, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # roda quando o servidor sobe; os testes usam um banco próprio e não passam por aqui
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/")
def retorna():
    return {"status": "ok"}
