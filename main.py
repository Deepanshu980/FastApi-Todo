from fastapi import FastAPI
from routers import todo

app = FastAPI()

app.include_router(todo.router)

@app.get("/")
def home():
    return {"message": "Todo API Running"}
