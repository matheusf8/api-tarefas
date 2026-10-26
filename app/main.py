from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def retorna():
    return{"status": "ok"}