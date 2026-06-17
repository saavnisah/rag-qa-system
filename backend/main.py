from fastapi import FastAPI, HTTPException
from rag.pipeline import RAGPipeline
from backend.schemas.request_model import QuestionRequest,QuestionResponse,IngestResponse
from db.queries import get_total_queries, get_average_latency, get_failed_queries, get_top_questions

app = FastAPI(
    title="RAG API",
    version="1.0.0"
)
pipeline = RAGPipeline()

@app.get("/")
def home():
    return {
        "message": "RAG API is running."
    }

@app.post("/ingest", response_model=IngestResponse)
def ingest():

    try:

        result = pipeline.ingest_document(
            r"data/AWS Customer Agreement.pdf"
        )

        return result

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/ask", response_model=QuestionResponse)
def ask(request: QuestionRequest):

    try:

        result = pipeline.ask_question(
            request.question
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/analytics")
def analytics():

    try:

        return {
            "total_queries": get_total_queries(),
            "average_latency_ms": get_average_latency(),
            "failed_queries": get_failed_queries(),
            "top_questions": get_top_questions()
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )