from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import tasks, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # roda quando o servidor sobe; os testes usam um banco próprio e não passam por aqui
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

# o React roda em outra porta (5173); sem isto o navegador bloqueia as chamadas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/")
def retorna():
    return {"status": "ok"}
