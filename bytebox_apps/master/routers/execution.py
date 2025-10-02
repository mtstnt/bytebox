from typing import Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel

from bytebox_core.docker import list_images

class ExecutionRequest(BaseModel):
    files: Dict[str, Any]
    entrypoint: str
    setup_id: int

router = APIRouter(prefix = "/executor")

@router.get("/images")
async def get_images():
    images = list_images()
    return list(map(lambda x: {
        "id": x.id,
        "name": x.attrs["RepoTags"][0],
    }, images))

@router.post("/run")
async def execute(request: ExecutionRequest):
    return request.model_dump_json()