from sqlalchemy import func

from db.models import QueryLog
from db.database import SessionLocal


# --------------------------------------------------
# Log Query
# --------------------------------------------------
def log_query(
    question,
    answer,
    answer_found,
    latency_ms,
    retrieved_chunks
):
    """
    Store a user query in the database.
    """

    db = SessionLocal()

    query = QueryLog(
        question=question,
        answer=answer,
        answer_found=answer_found,
        latency_ms=latency_ms,
        retrieved_chunks=retrieved_chunks
    )

    db.add(query)
    db.commit()
    db.close()


# --------------------------------------------------
# Total Queries
# --------------------------------------------------
def get_total_queries():

    db = SessionLocal()

    total = db.query(QueryLog).count()

    db.close()

    return total


# --------------------------------------------------
# Average Latency
# --------------------------------------------------
def get_average_latency():

    db = SessionLocal()

    avg = db.query(
        func.avg(QueryLog.latency_ms)
    ).scalar()

    db.close()

    return round(avg or 0, 2)


# --------------------------------------------------
# Failed Queries
# --------------------------------------------------
def get_failed_queries():

    db = SessionLocal()

    failed = db.query(QueryLog).filter(
        QueryLog.answer_found == False
    ).count()

    db.close()

    return failed


# --------------------------------------------------
# Top Questions
# --------------------------------------------------
def get_top_questions():

    db = SessionLocal()

    result = (
        db.query(
            QueryLog.question,
            func.count(QueryLog.question).label("count")
        )
        .group_by(QueryLog.question)
        .order_by(func.count(QueryLog.question).desc())
        .limit(5)
        .all()
    )

    db.close()

    return [
        {
            "question": row.question,
            "count": row.count
        }
        for row in result
    ]