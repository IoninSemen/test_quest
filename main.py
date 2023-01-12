import crud, models, schemas

from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


@app.post("/task/", response_model=schemas.Task)
def create_task(request: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = crud.get_task_by_uuid(db, task_uuid=request.task_uuid)
    if db_task:
        raise HTTPException(status_code=400, detail="UUID already registered")
    return crud.create_task(db=db, task=request)


@app.get("/tasks/", response_model=List[schemas.ShowTask])
def read_tasks(db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db)
    return tasks


@app.post("/tasks/{task_id}/parameters/", response_model=schemas.Parameter)
def create_parameters_for_task(task_id: int, request: schemas.ParameterCreate, db: Session = Depends(get_db)):
    return crud.create_task_parameter(db = db, params = request, task_id = task_id)


@app.get("/parameters/", response_model=List[schemas.Parameter])
def read_parameters(db: Session = Depends(get_db)):
    parameters = crud.get_parameters(db)
    return parameters


@app.put("/task/{task_id}")
def update_task(task_id, Task: schemas.TaskCreate,  Parameters: schemas.ParameterBase, db: Session = Depends(get_db)):
    return crud.update(task_sid = task_id, db = db, task = Task, parameters = Parameters)