from sqlalchemy import Column, Integer, String

from src.db import Base


class EmployeesModel(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    job = Column(String(255), nullable=False)

    def __str__(self):
        return f"EmployeesModel({self.id}, {self.name}, {self.job})"
