
import datetime
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from bytebox.settings import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)

def get_database():
    yield Session(engine)

class BaseORMModel(Base):
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=int(datetime.datetime.now(datetime.timezone.utc).timestamp()))
    updated_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=int(datetime.datetime.now(datetime.timezone.utc).timestamp()))