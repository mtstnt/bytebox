from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from bytebox.config.database import get_database
from bytebox.pipelines.models import PipelineModel, PipelineStepModel, PipelineType
from bytebox.pipelines.schemas import (
    PipelineCreate,
    PipelineResponse,
    PipelineUpdate,
    PipelineStepCreate,
    PipelineStepResponse,
    PipelineStepUpdate,
)

router = APIRouter(prefix="/pipelines")


# Pipeline CRUD endpoints
@router.post("", response_model=PipelineResponse)
async def create_pipeline(
    db: Annotated[Session, Depends(get_database)], request: PipelineCreate
):
    pipeline = PipelineModel(name=request.name, type=request.type.value)
    db.add(pipeline)
    db.commit()
    db.refresh(pipeline)
    return pipeline


@router.get("", response_model=list[PipelineResponse])
async def list_pipelines(db: Annotated[Session, Depends(get_database)]):
    stmt = select(PipelineModel)
    pipelines = db.execute(stmt).scalars().all()
    return pipelines


@router.get("/{pipeline_id}", response_model=PipelineResponse)
async def get_pipeline(db: Annotated[Session, Depends(get_database)], pipeline_id: int):
    stmt = select(PipelineModel).where(PipelineModel.id == pipeline_id)
    pipeline = db.execute(stmt).scalar_one_or_none()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline


@router.put("/{pipeline_id}", response_model=PipelineResponse)
async def update_pipeline(
    db: Annotated[Session, Depends(get_database)],
    pipeline_id: int,
    request: PipelineUpdate,
):
    stmt = select(PipelineModel).where(PipelineModel.id == pipeline_id)
    pipeline = db.execute(stmt).scalar_one_or_none()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    if request.name is not None:
        pipeline.name = request.name
    if request.type is not None:
        pipeline.type = request.type.value

    db.commit()
    db.refresh(pipeline)
    return pipeline


@router.delete("/{pipeline_id}")
async def delete_pipeline(
    db: Annotated[Session, Depends(get_database)], pipeline_id: int
):
    stmt = select(PipelineModel).where(PipelineModel.id == pipeline_id)
    pipeline = db.execute(stmt).scalar_one_or_none()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    db.delete(pipeline)
    db.commit()
    return {"message": "Pipeline deleted successfully"}


# PipelineStep CRUD endpoints
@router.post("/{pipeline_id}/steps", response_model=PipelineStepResponse)
async def create_pipeline_step(
    db: Annotated[Session, Depends(get_database)],
    pipeline_id: int,
    request: PipelineStepCreate,
):
    # Verify pipeline exists
    stmt = select(PipelineModel).where(PipelineModel.id == pipeline_id)
    pipeline = db.execute(stmt).scalar_one_or_none()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    step = PipelineStepModel(
        name=request.name,
        pipeline_id=pipeline_id,
        sequence_no=request.sequence_no,
        base_image=request.base_image,
        command=request.command,
        config=request.config,
    )
    db.add(step)
    db.commit()
    db.refresh(step)
    return step


@router.get("/{pipeline_id}/steps", response_model=list[PipelineStepResponse])
async def list_pipeline_steps(
    db: Annotated[Session, Depends(get_database)], pipeline_id: int
):
    stmt = (
        select(PipelineStepModel)
        .where(PipelineStepModel.pipeline_id == pipeline_id)
        .order_by(PipelineStepModel.sequence_no)
    )
    steps = db.execute(stmt).scalars().all()
    return steps


@router.get("/{pipeline_id}/steps/{step_id}", response_model=PipelineStepResponse)
async def get_pipeline_step(
    db: Annotated[Session, Depends(get_database)], pipeline_id: int, step_id: int
):
    stmt = select(PipelineStepModel).where(
        PipelineStepModel.id == step_id, PipelineStepModel.pipeline_id == pipeline_id
    )
    step = db.execute(stmt).scalar_one_or_none()
    if not step:
        raise HTTPException(status_code=404, detail="Pipeline step not found")
    return step


@router.put("/{pipeline_id}/steps/{step_id}", response_model=PipelineStepResponse)
async def update_pipeline_step(
    db: Annotated[Session, Depends(get_database)],
    pipeline_id: int,
    step_id: int,
    request: PipelineStepUpdate,
):
    stmt = select(PipelineStepModel).where(
        PipelineStepModel.id == step_id, PipelineStepModel.pipeline_id == pipeline_id
    )
    step = db.execute(stmt).scalar_one_or_none()
    if not step:
        raise HTTPException(status_code=404, detail="Pipeline step not found")

    if request.name is not None:
        step.name = request.name
    if request.sequence_no is not None:
        step.sequence_no = request.sequence_no
    if request.base_image is not None:
        step.base_image = request.base_image
    if request.command is not None:
        step.command = request.command
    if request.config is not None:
        step.config = request.config

    db.commit()
    db.refresh(step)
    return step


@router.delete("/{pipeline_id}/steps/{step_id}")
async def delete_pipeline_step(
    db: Annotated[Session, Depends(get_database)], pipeline_id: int, step_id: int
):
    stmt = select(PipelineStepModel).where(
        PipelineStepModel.id == step_id, PipelineStepModel.pipeline_id == pipeline_id
    )
    step = db.execute(stmt).scalar_one_or_none()
    if not step:
        raise HTTPException(status_code=404, detail="Pipeline step not found")

    db.delete(step)
    db.commit()
    return {"message": "Pipeline step deleted successfully"}
