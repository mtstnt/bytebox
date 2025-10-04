from enum import Enum
from bytebox.config.database import Base, CommonMixin
from sqlalchemy import BigInteger, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from bytebox.utils.helpers import DEFAULT_CURRENT_TIMESTAMP

"""
Session defines the user submissions.
"""

class SessionStatus(Enum):
    Pending = 0
    Running = 1
    Completed = 2
    Failed = 3
    
class SessionModel(CommonMixin, Base):
    __tablename__ = "sessions"
    
    pipeline_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False)
    inputs: Mapped[str] = mapped_column(Text, nullable=False)
    last_updated_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=DEFAULT_CURRENT_TIMESTAMP)
    
class SessionDetailModel(CommonMixin, Base):
    __tablename__ = "session_details"
    
    session_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pipeline_step_id: Mapped[int] = mapped_column(Integer, nullable=False)
    worker_id: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False)
    output: Mapped[str] = mapped_column(Text, nullable=False)
    logs: Mapped[str] = mapped_column(Text, nullable=False)
    last_updated_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=DEFAULT_CURRENT_TIMESTAMP)