from typing import Annotated, Optional
from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select
import datetime
import bcrypt

from bytebox.auth.helpers import get_session_user
from bytebox.users.models import UserModel
from bytebox.config.database import get_database
from bytebox.users.repository import UserRepository
from bytebox.users.schemas import UserCreateRequest, UserResponse, UserUpdateRequest

router = APIRouter(prefix="/users")

@router.post("/", response_model=UserResponse)
async def create_user(
    request: UserCreateRequest,
    _ = Depends(get_session_user),
    db: Session = Depends(get_database)
):
    user_repository = UserRepository.from_session(db)
    existing_user = user_repository.get_by_email_or_username(request.email, request.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email or username already exists")
        
    hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    new_user = user_repository.create(UserModel(
        email=request.email,
        username=request.username,
        password=hashed_password
    ))
    
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at
    )

@router.get("/", response_model=list[UserResponse])
async def get_users(
    current_user = Depends(get_session_user),
    db: Session = Depends(get_database)
):
    stmt = select(UserModel)
    users = db.execute(stmt).scalars().all()
    
    return [
        UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        for user in users
    ]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user = Depends(get_session_user),
    db: Session = Depends(get_database)
):
    stmt = select(UserModel).where(UserModel.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    request: UserUpdateRequest,
    current_user = Depends(get_session_user),
    db: Session = Depends(get_database)
):
    stmt = select(UserModel).where(UserModel.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check for conflicts if email or username is being updated
    if request.email and request.email != user.email:
        stmt = select(UserModel).where(UserModel.email == request.email)
        existing_user = db.execute(stmt).scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already in use")
        user.email = request.email
    
    if request.username and request.username != user.username:
        stmt = select(UserModel).where(UserModel.username == request.username)
        existing_user = db.execute(stmt).scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already in use")
        user.username = request.username
    
    if request.password:
        # Hash password
        hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password.decode('utf-8')
    
    user.updated_at = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    
    db.commit()
    db.refresh(user)
    
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user = Depends(get_session_user),
    db: Session = Depends(get_database)
):
    stmt = select(UserModel).where(UserModel.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}


