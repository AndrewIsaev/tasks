from fastapi import FastAPI
from src.employeers.router import router as employees_router

app = FastAPI(title="Tasks")

app.include_router(employees_router)
