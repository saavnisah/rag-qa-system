import os
import time

from rag.chunker import Chunker
from rag.embedder import Embedder
from rag.retriever import Retriever
from rag.generator import Generator

from db.queries import log_query


class RAGPipeline:

    def __init__(self):

        self.chunker = Chunker()
        self.embedder = Embedder()
        self.retriever = Retriever()
        self.generator = Generator()

    def ingest_document(self, pdf_path):

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(
                f"{pdf_path} not found."
            )

        print("Loading PDF...")

        chunks = self.chunker.load_and_chunk(pdf_path)

        print(f"Created {len(chunks)} chunks")

        print("Generating embeddings...")

        embeddings = self.embedder.embed_chunks(chunks)

        print("Building FAISS index...")

        self.retriever.build_index(
            embeddings,
            chunks
        )

        return {
            "message": "Document ingested successfully.",
            "chunks": len(chunks)
        }

    def ask_question(self, question):

        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )
        if not os.path.exists(self.retriever.index_path):
            raise FileNotFoundError(
        "No document has been ingested. Please call /ingest first."
    )

        start = time.time()

        self.retriever.load_index()
        query_embedding = self.embedder.model.encode(
            question,
            convert_to_numpy=True
        )
        retrieved_chunks = self.retriever.retrieve(
            query_embedding,
            top_k=4
        )
        answer = self.generator.generate_answer(
            question,
            retrieved_chunks
        )

        end = time.time()

        latency = (end - start) * 1000

        answer_found = (
            "could not find this information"
            not in answer.lower()
        )
        log_query(
            question=question,
            answer=answer,
            answer_found=answer_found,
            latency_ms=latency,
            retrieved_chunks=len(retrieved_chunks)
        )

        # Source Pages
        source_pages = sorted(
            list(
                set(
                    chunk.metadata.get(
                        "page",
                        "Unknown"
                    )
                    for chunk in retrieved_chunks
                )
            )
        )

        return {
            "question": question,
            "answer": answer,
            "sources": source_pages,
            "latency_ms": round(latency, 2)
        }