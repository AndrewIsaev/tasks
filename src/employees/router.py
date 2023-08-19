from fastapi import APIRouter, Depends, status
from sqlalchemy import delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_async_session
from src.employees.models import EmployeesModel
from src.employees.schemas import EmployeesSchema, EmployeesCreateSchema

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=list[EmployeesSchema])
async def get_all_employees(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(EmployeesModel))
    return result.scalars().all()


@router.get("/{employees_id}", response_model=EmployeesSchema)
async def get_employees(
        employees_id: int, session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(EmployeesModel).filter(EmployeesModel.id == employees_id)
    )
    return result.scalars().one()


@router.post("/", response_model=EmployeesSchema, status_code=status.HTTP_201_CREATED)
async def create_employees(
        employee: EmployeesCreateSchema, session: AsyncSession = Depends(get_async_session)
):
    employee = EmployeesModel(**employee.model_dump())
    try:
        session.add(employee)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise e
    return employee


@router.put("/{employees_id}", response_model=EmployeesSchema)
async def update_employee(
        employees_id: int,
        data: EmployeesCreateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    query = (
        update(EmployeesModel)
        .filter(EmployeesModel.id == employees_id)
        .values(**data.model_dump())
        .returning(EmployeesModel)
    )
    res = await session.execute(query)
    await session.commit()
    return res.scalars().one()


@router.delete("/{employees_id}", status_code=status.HTTP_200_OK)
async def delete_employee(
        employees_id: int, session: AsyncSession = Depends(get_async_session)
):
    query = delete(EmployeesModel).where(EmployeesModel.id == employees_id)
    await session.execute(query)
    await session.commit()
    return {"status": status.HTTP_200_OK}
