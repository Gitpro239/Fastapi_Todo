from fastapi import FastAPI
from api.todo import router as todoapi
from api.create_todo import router as create_todo

app = FastAPI()

app.include_router(todoapi)
app.include_router(create_todo)

@app.get("/")
def read_root():
    return {"message": "Welcome to Todo API"}

@app.get("/api")
def read_roots():
    return {"message": "Welcome to Todo API"}