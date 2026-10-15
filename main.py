from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    status: str

class TaskUpdate(BaseModel):
    title: str | None = None
    status: str | None = None

app = FastAPI()

data = [
    {
        "id": 1,
        "title": "Read paper",
        "status": "todo"
    },
    {
        "id": 2,
        "title": "Run experiment",
        "status": "done"
    }
]


@app.get("/")
def root():
    return {"message": "Hello"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in data:
        if task["id"] == task_id:
            return task
        
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def create_task(task: TaskCreate):
    added_data = {
        "id": data[-1]["id"] + 1,
        "title": task.title,
        "status": task.status
    }

    data.append(added_data)

    return added_data

@app.get("/tasks")
def get_all_tasks():
    return data

@app.patch("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    
    if update.title is None and update.status is None:
        raise HTTPException(status_code=400, detail="Bad format")
    
    for task in data:
        if task["id"] == task_id:
            need_update_data = task

            if update.title is not None:
                need_update_data["title"] = update.title
    
            if update.status is not None:
                need_update_data["status"] = update.status

            return need_update_data
        
    raise HTTPException(status_code=404, detail="Not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in data:
        if task["id"] == task_id:
            data.remove(task)
            return {"message": "Task deleted"}

    raise HTTPException(status_code=404, detail="Task not found")