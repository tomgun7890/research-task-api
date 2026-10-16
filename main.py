from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection, row_to_task

class TaskCreate(BaseModel):
    title: str
    status: str

class TaskUpdate(BaseModel):
    title: str | None = None
    status: str | None = None

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return row_to_task(row)

@app.post("/tasks")
def create_task(task: TaskCreate):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, status) VALUES (?, ?)",
        (task.title, task.status)
    )

    new_id = cursor.lastrowid

    connection.commit()
    connection.close()

    print("new data id:", new_id)

    return {
        "id": new_id,
        "title": task.title,
        "status": task.status
    }

@app.get("/tasks")
def get_all_tasks():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        task = row_to_task(row)

        result.append(task)

    connection.close()

    return result

@app.patch("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):

    if update.title is None and update.status is None:
        raise HTTPException(status_code=400, detail="Bad format")
    
    connection = get_connection()
    cursor = connection.cursor()
    
    updated_count = 0

    if update.title is not None:
        cursor.execute(
            "UPDATE tasks " \
            "SET title = ? " \
            "WHERE id = ?",
            (update.title, task_id)
        )
    
        updated_count += cursor.rowcount

    if update.status is not None:
        cursor.execute(
            "UPDATE tasks " \
            "SET status = ? " \
            "WHERE id = ?",
            (update.status, task_id)
        )
    
        updated_count += cursor.rowcount

    if updated_count == 0:
        connection.close()
        raise HTTPException(status_code=404, detail="Not found")
    
    connection.commit()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    connection.close()

    return row_to_task(row)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    deleted_row = cursor.rowcount

    if deleted_row == 0:
        connection.close()
        raise HTTPException(status_code=404, detail="Not found")
    
    connection.commit()
    connection.close()

    return {"message": "Task deleted"}