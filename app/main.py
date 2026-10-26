from fastapi import FastAPI

from app.database import Base, engine
from app.routers import tasks, users

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/")
def retorna():
    return {"status": "ok"}
