from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from bytebox.config.database import get_database
from bytebox.workers.models import WorkerModel, WorkerStatus
from bytebox.workers.schemas import (
    WorkerCreate,
    WorkerResponse,
    WorkerUpdate,
)
from bytebox.utils.helpers import DEFAULT_CURRENT_TIMESTAMP

router = APIRouter(prefix="/workers")


@router.post("", response_model=WorkerResponse)
async def create_worker(
    db: Annotated[Session, Depends(get_database)],
    request: WorkerCreate
):
    worker = WorkerModel(
        ip_address=request.ip_address,
        parallel_capacity=request.parallel_capacity,
        status=WorkerStatus.Connected.value,
        last_healthcheck_at=DEFAULT_CURRENT_TIMESTAMP()
    )
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return worker


@router.get("", response_model=list[WorkerResponse])
async def list_workers(db: Annotated[Session, Depends(get_database)]):
    stmt = select(WorkerModel)
    workers = db.execute(stmt).scalars().all()
    return workers


@router.get("/{worker_id}", response_model=WorkerResponse)
async def get_worker(
    db: Annotated[Session, Depends(get_database)],
    worker_id: int
):
    stmt = select(WorkerModel).where(WorkerModel.id == worker_id)
    worker = db.execute(stmt).scalar_one_or_none()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker


@router.put("/{worker_id}", response_model=WorkerResponse)
async def update_worker(
    db: Annotated[Session, Depends(get_database)],
    worker_id: int,
    request: WorkerUpdate
):
    stmt = select(WorkerModel).where(WorkerModel.id == worker_id)
    worker = db.execute(stmt).scalar_one_or_none()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    if request.ip_address is not None:
        worker.ip_address = request.ip_address
    if request.parallel_capacity is not None:
        worker.parallel_capacity = request.parallel_capacity
    
    db.commit()
    db.refresh(worker)
    return worker


@router.delete("/{worker_id}")
async def delete_worker(
    db: Annotated[Session, Depends(get_database)],
    worker_id: int
):
    stmt = select(WorkerModel).where(WorkerModel.id == worker_id)
    worker = db.execute(stmt).scalar_one_or_none()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    db.delete(worker)
    db.commit()
    return {"message": "Worker deleted successfully"}
