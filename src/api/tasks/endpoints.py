from typing import List

from fastapi import APIRouter, HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models.models import TasksModel
from src.api.schemas.tasks import TaskSchema, TaskUpdateSchema, TaskGetSchema, TaskDeleteSchema
from src.db.database import SessionDep, engine
from src.db.models.models import Base

router = APIRouter(prefix="/tasks")

@router.get("/all", response_model=List[TaskGetSchema])
async def get_tasks(session : SessionDep):
        try:
            tasks = await session.execute(select(TasksModel))
            tasks_list = tasks.scalars().all()
            return tasks_list
        except:
            raise HTTPException(status_code=500, detail="Tasks getting failed")


@router.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            return {"msg": "database setup complete"}
        except:
            raise HTTPException(status_code=404, detail="Database setup failed")

@router.post("/create_task")
async def create_task(task : TaskSchema, session : SessionDep):
    try:
        new_task = TasksModel(
            title = task.title,
            description = task.description,
            start_date = task.start_date,
            reward_points = task.reward_points,
            end_date = task.end_date,
            is_done = task.is_done
        )
        session.add(new_task)
        await session.commit()
        return {"msg": "task created"}
    except:
        raise HTTPException(status_code=404, detail="Task creation failed")

@router.post("/update_task/{task_id}")
async def update_task(update_data : TaskUpdateSchema, session : SessionDep, task_id : int):
    try:
            old_task = await session.execute(select(TasksModel).where(TasksModel.id == task_id))
            old_task = old_task.scalar_one_or_none()
            if old_task is None:
                raise HTTPException(status_code=404, detail="Task not found")
            update_dict = update_data.dict(exclude_unset=True)
            for key,value in update_dict.items():
                setattr(old_task, key, value)
            await session.commit()
            return {"msg": "Task updated"}
    except:
        raise HTTPException(status_code=404, detail="Task update failed")

@router.delete("/delete_task/{task_id}")
async def delete_task(task_id : int, session : SessionDep):
    try:
            result = session.execute(select(TasksModel).where(TasksModel.id == task_id))
            task = result.scalar_one_or_none()
            session.delete(task)
            await session.commit()
    except:
        raise HTTPException(status_code=404, detail="Task deletion failed")

    return {"msg": "task deleted"}