from pydantic import BaseModel
from typing import Dict, Any

class ExecutionRequest(BaseModel):
    files_flat: str
    configuration: Dict[str, Any]
    pipeline_id: int
    
class ExecutionResponse(BaseModel):
    session_id: int
    started_at: int
    
class SessionStatusResponse(BaseModel):
    status: str
    outputs: Dict[str, Any]
    logs: Dict[str, Any]
    completed_at: int
    failed_at: int
    started_at: int
    updated_at: int