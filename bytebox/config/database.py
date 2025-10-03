
import datetime
from sqlalchemy import BigInteger, Integer
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, Session
from sqlalchemy import create_engine

from bytebox.settings import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)

def get_database():
    yield Session(engine)

class CommonMixin(object):
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=int(datetime.datetime.now(datetime.timezone.utc).timestamp()))
    updated_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=int(datetime.datetime.now(datetime.timezone.utc).timestamp()))