from fastapi import FastAPI

from src.employees.router import router as employees_router
from src.tasks.router import router as task_router

app = FastAPI(title="Tasks")

app.include_router(employees_router)
app.include_router(task_router)
