import enum

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.db import Base


class StatusEnum(enum.Enum):
    todo = "todo"
    doing = "doing"
    done = "done"


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.todo)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    parent_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)

    employee = relationship("EmployeesModel", backref="tasks")
    parent = relationship(
        "TaskModel", remote_side=id, backref="children", cascade="all, delete"
    )
