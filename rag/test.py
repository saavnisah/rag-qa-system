import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from pipeline import RAGPipeline

pipeline = RAGPipeline()

# Only run once
# pipeline.ingest_document(
#     r"C:\Users\saavn\rag-qa-system\data\AWS Customer Agreement.pdf"
# )

response = pipeline.ask_question(
    "Can AWS terminate my account?"
)

print("\nQuestion:")
print(response["question"])

print("\nAnswer:")
print(response["answer"])

print("\nSource Pages:")
print(response["sources"])

print("\nLatency:")
print(response["latency_ms"], "ms")