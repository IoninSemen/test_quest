from typing import List
from pydantic import BaseModel


class ParameterBase(BaseModel):
    parameter: str
    parameter1: int

    class Config:
        orm_mode = True


class ParameterCreate(ParameterBase):
    pass


class Parameter(ParameterBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    task_uuid: str


class TaskCreate(TaskBase):
    description: str


class ShowTask(TaskBase):
    description: str
    params: ParameterBase

    class Config:
        orm_mode = True


class Task(TaskBase):
    id: int
    description: str
    params: List[Parameter] = []

    class Config:
        orm_mode = True