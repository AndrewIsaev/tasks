from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_async_session
from sqlalchemy.orm import query

from src.employeers.models import EmployeesModel

router = APIRouter(prefix='/employees', tags=["employees"])

@router.get('/')
async def get_employees(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(EmployeesModel))
    return result.scalars().all()
