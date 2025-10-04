from pydantic import BaseModel
from typing import Optional
from bytebox.pipelines.models import PipelineType

# Pipeline schemas
class PipelineCreate(BaseModel):
    name: str
    type: PipelineType

class PipelineUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[PipelineType] = None

class PipelineResponse(BaseModel):
    id: int
    name: str
    type: int
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True

# PipelineStep schemas
class PipelineStepCreate(BaseModel):
    name: str
    sequence_no: int
    base_image: str
    command: str
    config: str

class PipelineStepUpdate(BaseModel):
    name: Optional[str] = None
    sequence_no: Optional[int] = None
    base_image: Optional[str] = None
    command: Optional[str] = None
    config: Optional[str] = None

class PipelineStepResponse(BaseModel):
    id: int
    name: str
    pipeline_id: int
    sequence_no: int
    base_image: str
    command: str
    config: str
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True