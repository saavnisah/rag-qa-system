from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Float
from sqlalchemy import DateTime
from datetime import datetime

from db.database import Base


class QueryLog(Base):

    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)

    question = Column(String)

    answer = Column(String)

    answer_found = Column(Boolean)

    latency_ms = Column(Float)

    retrieved_chunks = Column(Integer)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )