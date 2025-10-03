from typing import Annotated, Dict, Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from docker import DockerClient

from bytebox.auth.helpers import get_session_user
from bytebox.users.models import UserModel

class ExecutionRequest(BaseModel):
    files: Dict[str, Any]
    entrypoint: str
    setup_id: int

router = APIRouter(prefix = "/executor")

@router.get("/images")
async def get_images(user: Annotated[UserModel, Depends(get_session_user)]):
    images = list_images()
    return list(map(lambda x: {
        "id": x.id,
        "name": x.attrs["RepoTags"][0],
    }, images))

@router.post("/run")
async def execute(request: ExecutionRequest):
    return request.model_dump_json()
    
def list_images():
    client = DockerClient.from_env()
    return client.images.list()