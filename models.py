from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_uuid = Column(String, unique=True, index=True)
    description = Column(String)

    params = relationship("Parameter", back_populates="owner")


class Parameter(Base):
    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True, index=True)
    parameter = Column(String, index=True)
    parameter1 = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey("tasks.id"))

    owner = relationship("Task", back_populates="params")