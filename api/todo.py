from fastapi import APIRouter, HTTPException, status
from database.database import Database
from dotenv import load_dotenv
from models.model import *

import sqlite3

router = APIRouter()
db = Database()

load_dotenv()

@router.post("/create-task", response_model=TodoResponse)
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

@router.get("/list-tasks", response_model=list[TodoResponse])
def get_all_todos(completed: bool = None):
    """Get all todos, optionally filtered by completion status"""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    try:
        if completed is not None:
            cursor.execute("SELECT * FROM todos WHERE completed = ? ORDER BY created_at DESC", (completed,))
        else:
            cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
        
        todos = cursor.fetchall()
        return [dict(todo) for todo in todos]
    finally:
        conn.close()

@router.get("/get-task/{task_id}", response_model=TodoResponse)
def get_todo(task_id: int):
    """Get a specific todo by ID"""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM todos WHERE id = ?", (task_id,))
        todo = cursor.fetchone()
        
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        return dict(todo)
    finally:
        conn.close()

@router.put("/update-task/{task_id}", response_model=TodoResponse)
def update_todo(task_id: int, todo: TodoUpdate):
    """Update a todo item"""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if todo exists
        cursor.execute("SELECT * FROM todos WHERE id = ?", (task_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        # Build dynamic update query
        update_fields = []
        params = []
        
        if todo.title is not None:
            update_fields.append("title = ?")
            params.append(todo.title)
        
        if todo.description is not None:
            update_fields.append("description = ?")
            params.append(todo.description)
        
        if todo.completed is not None:
            update_fields.append("completed = ?")
            params.append(todo.completed)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_query = f"UPDATE todos SET {', '.join(update_fields)} WHERE id = ?"
        params.append(task_id)
        
        cursor.execute(update_query, params)
        conn.commit()
        
        # Fetch updated todo
        cursor.execute("SELECT * FROM todos WHERE id = ?", (task_id,))
        updated_todo = cursor.fetchone()
        
        return dict(updated_todo)
        
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@router.delete("/delete-task/{task_id}")
def delete_todo(task_id: int):
    """Delete a todo item"""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM todos WHERE id = ?", (task_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        return {"message": "Todo deleted successfully"}
        
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

