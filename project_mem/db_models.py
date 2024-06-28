import os

from sqlalchemy import String, Integer, create_engine
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, DeclarativeMeta, declarative_base


Base: DeclarativeMeta = declarative_base()

engine = create_engine(
   str(os.getenv('DATABASE_URL')),
    echo=False,
)

session_db = sessionmaker(engine)


class Mem(Base):
    __tablename__ = 'mems'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mem_path: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)


Base.metadata.create_all(engine)
