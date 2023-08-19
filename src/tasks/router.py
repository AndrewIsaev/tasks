from fastapi import APIRouter, Depends, status
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.tasks.models import TaskModel
from src.tasks.schemas import TaskSchema, TaskCreateSchema

router = APIRouter(
    prefix="/tasks",
    tags=["tags"],
)


@router.get("/", response_model=list[TaskSchema], status_code=status.HTTP_200_OK)
async def get_all_tasks(session: AsyncSession = Depends(get_async_session)):
    query = select(TaskModel)
    tasks = await session.execute(query)
    return tasks.scalars().all()


@router.get("/task_id", response_model=TaskSchema, status_code=status.HTTP_200_OK)
async def get_task_by_pk(
    task_id: int, session: AsyncSession = Depends(get_async_session)
):
    query = select(TaskModel).filter(TaskModel.id == task_id)
    task = await session.execute(query)
    return task.scalars().one()


@router.post("/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreateSchema, session: AsyncSession = Depends(get_async_session)
):
    task = TaskModel(**task.model_dump())
    try:
        session.add(task)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise e
    return task


@router.put("/task_id", response_model=TaskSchema, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: int,
    data: TaskCreateSchema,
    session: AsyncSession = Depends(get_async_session),
):
    statement = (
        update(TaskModel)
        .filter(TaskModel.id == task_id)
        .values(**data.model_dump())
        .returning(TaskModel)
    )
    try:
        res = await session.execute(statement)
        await session.commit()

    except Exception as e:
        await session.rollback()
        raise e
    return res.scalars().one()


@router.delete("/task_id")
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = (
            delete(TaskModel)
            .filter(TaskModel.id == task_id)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(query)
        await session.commit()
        return {"status": status.HTTP_200_OK}
    except IntegrityError:
        return (
            {
                "error": "Not allow to delete parent task",
                "status": status.HTTP_405_METHOD_NOT_ALLOWED,
            },
        )
