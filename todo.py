from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from database import engine
from models.todo import Todo

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/")
def create(todo: Todo):
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

@router.get("/")
def read_all():
    with Session(engine) as session:
        result = session.exec(select(Todo)).all()
        return result

@router.get("/{id}")
def read_one(id: int):
    with Session(engine) as session:
        todo = session.get(Todo, id)
        if not todo:
            raise HTTPException(404, "Todo not found")
        return todo

@router.put("/{id}")
def update(id: int, updated: Todo):
    with Session(engine) as session:
        todo = session.get(Todo, id)
        if not todo:
            raise HTTPException(404, "Todo not found")

        todo.title = updated.title
        todo.completed = updated.completed

        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

@router.delete("/{id}")
def delete(id: int):
    with Session(engine) as session:
        todo = session.get(Todo, id)
        if not todo:
            raise HTTPException(404, "Todo not found")

        session.delete(todo)
        session.commit()
        return {"message": "Todo deleted"}
