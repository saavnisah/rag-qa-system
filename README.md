# RAG Question Answering System

## Overview

This project is a Retrieval-Augmented Generation (RAG) based Question Answering System built using FastAPI, Streamlit, FAISS, SQLite, and Ollama.

The system processes the AWS Customer Agreement PDF, creates a semantic vector index using FAISS, retrieves the most relevant document chunks for a user's query, and generates accurate answers using the Phi-3 Mini Large Language Model running locally through Ollama.

In addition to question answering, the system logs every query into a SQLite database and provides analytics through a REST API.

---

# Features

* Retrieval-Augmented Generation (RAG)
* PDF document ingestion
* Semantic search using FAISS
* Local LLM inference using Ollama
* FastAPI REST API
* Streamlit User Interface
* SQLite query logging
* Analytics dashboard
* Source page retrieval
* Response latency measurement

---

# Project Structure

```
rag-qa-system/
│
├── backend/
│   ├── main.py
│   └── schemas/
│
├── rag/
│   ├── chunker.py
│   ├── embedder.py
│   ├── retriever.py
│   ├── generator.py
│   └── pipeline.py
│
├── db/
│   ├── database.py
│   ├── models.py
│   └── queries.py
│
├── frontend/
│   └── app.py
│
├── vector_store/
│
├── data/
│
├── requirements.txt
└── README.md
```

---

# Technology Stack

* Python 3.11
* FastAPI
* Streamlit
* LangChain
* Sentence Transformers
* FAISS
* SQLite
* SQLAlchemy
* Ollama
* Phi-3 Mini
* PyPDF

---

# Setup Instructions

## 1. Clone the Repository

```bash
git clone https://github.com/<YOUR_USERNAME>/rag-qa-system.git

cd rag-qa-system
```

---

## 2. Create a Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install Ollama

Download Ollama from:

https://ollama.com/download

Pull the required model:

```bash
ollama pull phi3:mini
```

Start the Ollama server:

```bash
ollama serve
```

---

## 5. Run the Backend

```bash
uvicorn backend.main:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 6. Create the Vector Store

Open Swagger UI.

Run:

```
POST /ingest
```

This creates the FAISS vector index from the AWS Customer Agreement PDF.

---

## 7. Run the Frontend

```bash
streamlit run frontend/app.py
```

---

# API Endpoints

## POST /ingest

Processes the AWS Customer Agreement PDF and creates the FAISS vector store.

---

## POST /ask

Accepts a question and returns:

* Generated Answer
* Source Pages
* Response Latency

---

## GET /analytics

Returns:

* Total Queries
* Average Response Time
* Failed Queries
* Most Frequently Asked Questions

---

# Architecture Overview

```
                    Streamlit
                        │
                        ▼
                   FastAPI API
                        │
        ┌───────────────┼───────────────┐
        ▼                               ▼
   RAG Pipeline                    SQLite Logs
        │
        ▼
 PDF → Chunking → Embedding → FAISS
                        │
                        ▼
                 Semantic Retrieval
                        │
                        ▼
                 Phi-3 Mini (Ollama)
                        │
                        ▼
                     Response
```

---

# Key Design Decisions

### Chunking Strategy

* Recursive Character Text Splitter
* Chunk Size: 1000 characters
* Chunk Overlap: 200 characters

This balances context preservation while maintaining retrieval efficiency.

---

### Embedding Model

Sentence Transformers

```
all-MiniLM-L6-v2
```

Chosen because it provides high-quality semantic embeddings while remaining lightweight and fast for local inference.

---

### Vector Database

FAISS

Chosen because it offers efficient similarity search with low memory usage and fast retrieval.

---

### Retrieval Strategy

Top-K Retrieval

```
Top K = 4
```

The four most semantically relevant chunks are retrieved for answer generation.

---

### LLM

Phi-3 Mini

Running locally using Ollama.

Benefits:

* Offline inference
* No API costs
* Low latency
* Easy deployment

---

### Database

SQLite

Used to store:

* User Question
* Generated Answer
* Response Latency
* Retrieved Chunk Count
* Answer Status
* Timestamp

---

# Assumptions

* The input document is the AWS Customer Agreement PDF.
* Users ask questions related only to the ingested document.
* Ollama is installed and running locally.
* The FAISS vector store is generated before asking questions.

---

# Author

Saavni Sah
