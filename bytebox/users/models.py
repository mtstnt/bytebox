from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from bytebox.config.database import Base, CommonMixin

class UserModel(CommonMixin, Base):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)