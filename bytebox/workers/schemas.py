from pydantic import BaseModel
from typing import Optional

class WorkerCreate(BaseModel):
    ip_address: str
    parallel_capacity: int

class WorkerUpdate(BaseModel):
    ip_address: Optional[str] = None
    parallel_capacity: Optional[int] = None

class WorkerResponse(BaseModel):
    id: int
    ip_address: str
    status: int
    parallel_capacity: int
    last_healthcheck_at: int
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True
