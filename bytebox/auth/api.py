from typing import Annotated
import jwt

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from bytebox.auth.helpers import generate_token
from bytebox.auth.schemas import LoginRequest
from bytebox.config.database import get_database
from bytebox.users.models import UserModel

from bytebox.config.settings import JWT_SECRET

router = APIRouter(prefix = "/auth")

@router.post("/login")
async def login(db: Annotated[Session, Depends(get_database)], request: LoginRequest):
    stmt = select(UserModel).where(UserModel.username == request.username and UserModel.password == request.password)
    user = db.execute(stmt).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = generate_token(user, JWT_SECRET)
    return {
        "token": token,
        "user": {
            "username": user.username,
            "email": user.email
        },
    }