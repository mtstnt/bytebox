import base64
import json
from fastapi import APIRouter

from bytebox.sandbox.schemas import ExecutionRequest

router = APIRouter(prefix = "/sandbox")

@router.post("/run")
async def execute(request: ExecutionRequest):
    # TODO: Steps
    # Convert base64 to json.
    files_str = base64.b64decode(request.files_flat).decode("utf-8")
    files = json.loads(files_str)
    
    # Input validation (files, configuration)
    # Find available worker: load balance multiple workers. (Returns a list of order of workers)
    # Create session in database.
    # Attempt to send task to worker.
    # If worker replies, then return session ID to user and started at.
    # If doesn't, try other worker. (If all workers are busy, then return error)
    
    return request.model_dump_json()
    
@router.get("/sessions/{session_id}")
async def poll_session_status(session_id: int):
    # TODO: Steps
    # Check session status in database.
    # If session is not found, then return error.
    # If session is found, then return status, outputs, logs, completed at, failed at, started at, updated at.
    
    return {
        "status": "todo"
    }