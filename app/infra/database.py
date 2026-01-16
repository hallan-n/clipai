from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool
from consts import DATABASE_URL
import infra.models
from sqlmodel import SQLModel


class Connection:
    def __init__(self):
        engine = create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=3600,
            echo=True,
        )
        SQLModel.metadata.create_all(engine)
        self._session = Session(engine)

    def __enter__(self):
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()
