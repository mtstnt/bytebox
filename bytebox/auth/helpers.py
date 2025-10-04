import jwt

from typing import Annotated, Dict, Optional, Tuple
from fastapi import HTTPException, Header, Depends
from sqlalchemy.orm import Session

from bytebox.config.database import get_database
from bytebox.users.models import UserModel
from bytebox.users.repository import UserRepository
from bytebox.config.settings import JWT_SECRET

def get_session_user(db: Annotated[Session, Depends(get_database)], authorization: Annotated[str, Header()] = None) -> Tuple[Dict, str]:
    user_repository = UserRepository.from_session(db)
    claims, _token = parse_auth_header(authorization)
    user = user_repository.get_by_email_or_username(claims["email"], claims["username"])
    return user

def parse_auth_header(authorization: Optional[str]) -> Tuple[Dict, str]:
    if authorization is None: 
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    authorization_parts = authorization.split(" ")
    if len(authorization_parts) != 2 or authorization_parts[0] != "Bearer":
        raise HTTPException(status_code=400, detail="Invalid authorization header")
        
    token = authorization_parts[1]
    try:
        claims = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return (claims, token)
    
def generate_token(user: UserModel, jwt_secret: str) -> str:
    return jwt.encode({"email": user.email, "username": user.username}, jwt_secret, algorithm="HS256")