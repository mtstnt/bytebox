from enum import Enum
from bytebox.config.database import Base, CommonMixin
from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class WorkerStatus(Enum):
    Connected = 0
    Disconnected = 1

class WorkerModel(CommonMixin, Base):
    __tablename__ = "workers"
    
    ip_address: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False)
    parallel_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    last_healthcheck_at: Mapped[int] = mapped_column(BigInteger, nullable=False)