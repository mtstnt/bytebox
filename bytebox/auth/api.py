import jwt

from fastapi import APIRouter, HTTPException

from bytebox.auth.helpers import generate_token
from bytebox.auth.schemas import LoginRequest
from bytebox.settings import JWT_SECRET
from bytebox.settings import ENVIRONMENT
from bytebox.users.models import UserModel

router = APIRouter(prefix = "/auth")

@router.post("/login")
async def login(request: LoginRequest):
    if ENVIRONMENT == "development": 
        if request.username == "admin" and request.password == "admin":
            token = generate_token(UserModel(username=request.username, email="admin@admin.com"))
            return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid username or password")