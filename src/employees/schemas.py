from pydantic import BaseModel


class EmployeesSchema(BaseModel):
    id: int
    name: str
    job: str


class EmployeesCreateSchema(BaseModel):
    name: str
    job: str
