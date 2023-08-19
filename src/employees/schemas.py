from pydantic import BaseModel, ConfigDict


class EmployeesSchema(BaseModel):
    id: int
    name: str
    job: str

    model_config = ConfigDict(
        from_attributes=True,
    )


class EmployeesCreateSchema(BaseModel):
    name: str
    job: str
    model_config = ConfigDict(
        from_attributes=True,
    )
