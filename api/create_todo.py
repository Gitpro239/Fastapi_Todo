from fastapi import APIRouter, HTTPException, status
from database.database import Database
from dotenv import load_dotenv
from models.model import *

import sqlite3

router = APIRouter()
db = Database()

load_dotenv()

@router.post("/create_task", response_model=TodoResponse)
def create_todo(todo: TodoCreate):
    """Create a new todo item"""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO todos (title, description, completed) VALUES (?, ?, ?)",
            (todo.title, todo.description, todo.completed)
        )
        conn.commit()
        
        # Get the inserted todo
        todo_id = cursor.lastrowid
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        todo_data = cursor.fetchone()
        
        if todo_data:
            return dict(todo_data)
        else:
            raise HTTPException(status_code=500, detail="Failed to create todo")
            
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()
