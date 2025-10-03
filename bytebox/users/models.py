from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from bytebox.config.database import BaseORMModel

class UserModel(BaseORMModel):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)