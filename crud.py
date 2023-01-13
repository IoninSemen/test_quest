import models, schemas
from sqlalchemy.orm import Session


def get_task_by_uuid(db: Session, task_uuid: str):
    return db.query(models.Task).filter(models.Task.task_uuid == task_uuid).first()


def get_tasks(db: Session):
    return db.query(models.Task).all()


def update(task_sid, db: Session, task: schemas.TaskCreate, parameters: schemas.ParameterBase):
    update_task = db.query(models.Task).filter(models.Task.id == task_sid).update({
            models.Task.task_uuid: task.task_uuid,
            models.Task.description: task.description,
        }, synchronize_session=False)
    db.commit()
    update_parameters = db.query(models.Parameter).filter(models.Parameter.owner_id == task_sid).update({
            models.Parameter.parameter: parameters.parameter,
            models.Parameter.parameter1: parameters.parameter1,
    }, synchronize_session=False)
    db.commit()
    return "update"


def create_task(db: Session, task: schemas.ShowTask):
    db_task = models.Task(task_uuid=task.task_uuid, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    print(db_task.id)
    db_parameter = models.Parameter(**task.params.dict(), owner_id = db_task.id)
    db.add(db_parameter)
    db.commit()
    db.refresh(db_parameter)
    return db_task