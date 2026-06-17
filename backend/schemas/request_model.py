from pydantic import BaseModel, Field
class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1)


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list
    latency_ms: float


class IngestResponse(BaseModel):
    message: str
    chunks: int


class AnalyticsResponse(BaseModel):
    total_queries: int
    average_latency: float
    failed_queries: int
    top_questions: list