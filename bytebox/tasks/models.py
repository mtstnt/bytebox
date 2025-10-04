from sqlalchemy.orm import Mapped, mapped_column, Integer, Text, BigInteger
from bytebox.config.database import Base, CommonMixin
from bytebox.utils.helpers import DEFAULT_CURRENT_TIMESTAMP

"""
Task defines each low level step of the task needed to be executed by the worker.
"""

class TaskModel(CommonMixin, Base):
    __tablename__ = "tasks"
    
    pipeline_step_id: Mapped[int] = mapped_column(Integer, nullable=False)
    worker_id: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False)
    output: Mapped[str] = mapped_column(Text, nullable=False)
    logs: Mapped[str] = mapped_column(Text, nullable=False)
    last_updated_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=DEFAULT_CURRENT_TIMESTAMP)