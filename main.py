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



@app.post("/task/add", response_model=schemas.ShowTask)
def create_task(request: schemas.ShowTask, db: Session = Depends(get_db)):
    db_task = crud.get_task_by_uuid(db, task_uuid=request.task_uuid)
    if db_task:
        raise HTTPException(status_code=400, detail="UUID already registered")
    return crud.create_task(db=db, task=request)


@app.get("/tasks", response_model=List[schemas.Task])
def read_tasks(db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db)
    return tasks


@app.put("/task/{task_sid}")
def update_task(task_sid, Task: schemas.TaskCreate,  Parameters: schemas.ParameterBase, db: Session = Depends(get_db)):
    return crud.update(task_sid = task_sid, db = db, task = Task, parameters = Parameters)