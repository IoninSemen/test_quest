from sqlalchemy.orm import Session

import models, schemas


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_task_by_uuid(db: Session, task_uuid: str):
    return db.query(models.Task).filter(models.Task.task_uuid == task_uuid).first()


def get_tasks(db: Session):
    return db.query(models.Task).all()


def update(task_sid, db: Session, task: schemas.TaskCreate, parameters: schemas.ParameterBase):
    new_task = db.query(models.Task).filter(models.Task.id == task_sid).update({
            models.Task.task_uuid: task.task_uuid,
            models.Task.description: task.description,
        }, synchronize_session=False)
    db.commit()
    new_parameters = db.query(models.Parameter).filter(models.Parameter.owner_id == task_sid).update({
            models.Parameter.parameter: parameters.parameter,
            models.Parameter.parameter1: parameters.parameter1,
    }, synchronize_session=False)
    db.commit()
    return "Update"


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(task_uuid=task.task_uuid, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_parameters(db: Session):
    return db.query(models.Parameter).all()


def create_task_parameter(db: Session, params: schemas.ParameterBase, task_id: int):
    db_parameter = models.Parameter(**params.dict(), owner_id = task_id)
    db.add(db_parameter)
    db.commit()
    db.refresh(db_parameter)
    return db_parameter