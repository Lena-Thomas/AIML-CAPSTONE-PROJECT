# Zepto Support Assistant

## Overview

The Zepto Support Assistant is a small Retrieval-Augmented Generation (RAG) service built with Python, Sentence Transformers, ChromaDB, LangGraph, Pydantic, and FastAPI.

The system answers questions about Zepto's delivery, returns, membership, tracking, cancellation, gift card, and customer-support policies using a local document corpus.

The required graded implementation uses a deterministic offline mock mode controlled by the `MOCK_LLM` environment variable. When `MOCK_LLM` is unset or set to `1`, no external LLM API is called. Embedding and retrieval continue to run locally.

The optional real-LLM path is activated only when `MOCK_LLM=0`.

---

## RAG Architecture

The complete RAG pipeline follows these stages:

**Ingestion → Embedding → Retrieval → Generation**

### 1. Ingestion

The Zepto policy corpus is stored in the `docs/` directory as eight text documents:

* `doc_01.txt` — Delivery Policy
* `doc_02.txt` — Returns & Refunds
* `doc_03.txt` — Membership Tiers
* `doc_04.txt` — Order Tracking
* `doc_05.txt` — Order Cancellation Policy
* `doc_06.txt` — Damaged or Missing Items
* `doc_07.txt` — Gift Cards
* `doc_08.txt` — Customer Support Hours

The `ingest.py` module loads the eight documents from `docs/`, performs the required chunking, generates embeddings using the local `all-MiniLM-L6-v2` Sentence Transformers model, and stores the resulting vectors, document IDs, and metadata in the ChromaDB collection.

Since the supplied policy documents are short, a simple per-document chunking approach is sufficient.

The data flow is:

```text
Policy documents in docs/
        ↓
ingest.py
        ↓
Document chunks
        ↓
Embedding stage
```

### 2. Embedding

Each document chunk is converted into a numerical vector using the local Sentence Transformers model:

`all-MiniLM-L6-v2`

The embeddings are generated locally, so no embedding API key or external embedding service is required.

The resulting vectors, together with their document/chunk IDs and text, are stored in the ChromaDB collection.

The ChromaDB collection acts as the local vector store for the policy corpus.

The embedding flow is:

```text
Policy document
      ↓
Text chunk
      ↓
all-MiniLM-L6-v2
      ↓
Embedding vector
      ↓
ChromaDB collection
```

All eight policy documents are therefore embedded and made queryable through ChromaDB.

### 3. Retrieval

Incoming user queries first pass through the LangGraph intent-routing stage implemented by the application.

The LangGraph graph contains three main nodes:

* `classify_intent`
* `retrieve_and_answer`
* `direct_answer`

The `classify_intent` node determines whether the query is:

* `policy_question`
* `general_question`

In the required mock mode, this classification uses a deterministic keyword heuristic. A query containing terms such as `delivery`, `return`, `refund`, `membership`, `tracking`, `cancel`, `gift card`, or `support hours` is classified as a `policy_question`.

The graph then uses a conditional edge to route the query.

For a `policy_question`, the query is passed to the `retrieve_and_answer` node.

The `retrieve_and_answer` node embeds the query using `all-MiniLM-L6-v2` and searches the ChromaDB collection using cosine similarity. The top three most similar chunks are retrieved.

The most relevant retrieved chunk is then used by the mock generation logic to construct the answer.

Importantly, retrieval itself does not depend on `MOCK_LLM`. It runs locally in both mock mode and optional real-LLM mode.

The retrieval flow is:

```text
User query
    ↓
classify_intent
    ↓
policy_question
    ↓
retrieve_and_answer
    ↓
Query embedding
    ↓
ChromaDB similarity search
    ↓
Top-3 relevant chunks
```

### 4. Generation

For policy questions, final answer generation is handled by the `retrieve_and_answer` LangGraph node.

In the required default/mock mode, no LLM is called. Instead, the node deterministically generates an answer using the most similar retrieved chunk:

```text
Based on the retrieved context: {top_chunk_snippet}
```

The `top_chunk_snippet` is a short excerpt from the highest-ranked retrieved chunk.

For general questions, the `direct_answer` node is used. In mock mode it returns the fixed response:

```text
I can only answer questions about Zepto policies right now.
```

The final response is validated using the Pydantic response model defined in `schemas.py`. The model contains:

* `answer` — generated answer text
* `sources` — list of retrieved chunk/document IDs
* `confidence` — confidence value between `0` and `1`

In mock mode, these values are populated deterministically by the application code.

The optional real-LLM generation path uses the structured prompt template defined in `prompts.py`.

---

## LangGraph Flow

The graph-based orchestration can be represented as:

```text
                         ┌─────────────────────┐
                         │     User Query      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   classify_intent   │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    │ policy_question               │ general_question
                    ▼                               ▼
          ┌─────────────────────┐         ┌─────────────────────┐
          │ retrieve_and_answer │         │    direct_answer    │
          └──────────┬──────────┘         └──────────┬──────────┘
                     │                               │
                     ▼                               │
          ┌─────────────────────┐                     │
          │ Query Embedding     │                     │
          │ all-MiniLM-L6-v2    │                     │
          └──────────┬──────────┘                     │
                     │                               │
                     ▼                               │
          ┌─────────────────────┐                     │
          │     ChromaDB       │                     │
          │  Cosine Retrieval  │                     │
          └──────────┬──────────┘                     │
                     │                               │
                     ▼                               │
          ┌─────────────────────┐                     │
          │ Top-3 Relevant      │                     │
          │ Chunks              │                     │
          └──────────┬──────────┘                     │
                     │                               │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                          ┌────────────────────┐
                          │ Structured Pydantic│
                          │ Response           │
                          │ answer/sources/    │
                          │ confidence         │
                          └─────────┬──────────┘
                                    │
                                    ▼
                              FastAPI /ask
```

---

## Structured Prompt Template

The application contains a structured prompt template in `prompts.py` for the optional real-LLM path.

The template follows the required:

**Role → Context → Task → Format → Length**

structure.

It also contains an explicit negative constraint and a few-shot example.

The prompt is designed to ensure that the real LLM answers only from the retrieved Zepto policy context.

The prompt structure is:

```text
ROLE:
You are a Zepto customer-support assistant.

CONTEXT:
Use only the retrieved Zepto policy documents provided below.

TASK:
Answer the user's question using the retrieved context.

FORMAT:
Return the answer using the required structured output fields:
answer, sources, and confidence.

LENGTH:
Keep the answer concise and directly relevant to the user's question.

NEGATIVE CONSTRAINT:
Do not answer using information that is not present in the provided context.
Do not invent or assume Zepto policies.

FEW-SHOT EXAMPLE:
Question: How long can I report a damaged grocery item?

Context: Grocery and perishable items may be reported for a return within
24 hours of delivery if damaged, spoiled, or incorrect.

Expected behavior:
Answer using only the provided policy context and identify the relevant
source document.
```

This prompt is used by the optional real-LLM generation path when `MOCK_LLM=0`.

---

## MOCK_LLM Behavior

`MOCK_LLM` controls the LLM-dependent classification and generation behavior.

### Default / Required Graded Mode

When `MOCK_LLM` is unset or set to:

```text
MOCK_LLM=1
```

the application uses deterministic local mock logic.

In this mode:

```text
Intent classification
        ↓
Keyword heuristic
        ↓
Policy question? ── Yes ──→ Real local retrieval
                              ↓
                         ChromaDB
                              ↓
                         Mock answer

Policy question? ── No ───→ Fixed direct answer
```

No external LLM provider is contacted.

Embedding and ChromaDB retrieval still run normally because they are local components and are independent of the LLM toggle.

### Optional Real-LLM Mode

Only when:

```text
MOCK_LLM=0
```

is explicitly set does the application use the optional real-LLM path.

In this mode:

* `classify_intent` can use the LLM for intent classification.
* `retrieve_and_answer` still performs the same local embedding and ChromaDB retrieval.
* The retrieved context is supplied to the structured prompt in `prompts.py`.
* The LLM generates the final grounded response.
* The structured response is validated against the Pydantic schema in `schemas.py`.
* If the raw LLM output fails validation, the application can retry with a corrective instruction up to two additional times.

Therefore, the retrieval stage is the same in both modes; the LLM-dependent classification/generation behavior is what changes.

---

## Structured API Response

The FastAPI service returns a validated JSON response with the following fields:

```json
{
  "answer": "Based on the retrieved context: ...",
  "sources": ["..."],
  "confidence": 1.0
}
```

For policy questions, `sources` contains the IDs of the retrieved chunks/documents.

For general questions, `sources` is empty.

In the required mock mode, the confidence value is deterministic.

The response schema is defined in `schemas.py`.

---

## FastAPI Endpoint

The application exposes:

```text
POST /ask
```

Request format:

```json
{
  "query": "How long do I have to return a damaged item?"
}
```

The endpoint is implemented using FastAPI and accepts the request through a Pydantic request model.

The API wrapper is implemented in `api.py`, while the application and LangGraph processing are handled by the application code in `app.py`.

The response is validated using the Pydantic response model before being returned to the client.

---

## Example Verification Calls

The following examples were tested against the locally running Dockerized FastAPI application with `MOCK_LLM` left at its default state.

### Example 1 — Policy Question

The following query contains the keyword `return`, so `classify_intent` routes it to `policy_question`.

Request:

```powershell
Invoke-RestMethod -Uri "http://localhost:7860/ask" -Method Post -ContentType "application/json" -Body '{"query":"How long do I have to return a damaged item?"}' | ConvertTo-Json -Depth 10
```

Raw JSON response:

```json
{
    "answer": "Based on the retrieved context: Damaged or Missing Items:\n\n\"If an order arrives with damaged, spoiled, or missing items, customers must report it within 24 hours of delivery through the \u0027Report an Issue\u0027 button on the order page. Ze",
    "sources": [
        "doc_06.txt",
        "doc_02.txt",
        "doc_05.txt"
    ],
    "confidence": 1.0
}
```

The top retrieved source is `doc_06.txt`, which contains the Zepto damaged or missing items policy. The response follows the required mock-generation format:

```text
Based on the retrieved context: {top_chunk_snippet}
```

### Example 2 — General Question

The following query does not contain any of the policy-routing keywords, so `classify_intent` routes it to `general_question` and the `direct_answer` node handles it without retrieval.

Request:

```powershell
Invoke-RestMethod -Uri "http://localhost:7860/ask" -Method Post -ContentType "application/json" -Body '{"query":"What is the capital of France?"}' | ConvertTo-Json -Depth 10
```

Raw JSON response:

```json
{
    "answer": "I can only answer questions about Zepto policies right now.",
    "sources": [],
    "confidence": 1.0
}
```

The empty `sources` list confirms that no document retrieval was performed for the general question. The fixed answer and deterministic confidence value demonstrate the required mock-mode behavior.

---

## Docker Verification

The FastAPI application is containerized using the project `Dockerfile`.

The Docker image was successfully built and run locally.

The container exposes port `7860` and runs the FastAPI application using Uvicorn.

Example:

```powershell
docker run --rm -p 7860:7860 zepto-support-assistant
```

The running container produced:

```text
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:7860
```

A real POST request to `/ask` was then successfully processed and returned:

```text
200 OK
```

This verifies that the Dockerized FastAPI service is locally buildable, runnable, and accessible through the `/ask` endpoint.

No Hugging Face Spaces deployment is included because cloud deployment is an optional, ungraded extension.

---

## End-to-End Data Flow

The complete system can be summarized as:

```text
8 Zepto Policy Documents
        │
        ▼
     Ingestion
   docs/*.txt
        │
        ▼
     ingest.py
        │
        ▼
      Chunking
        │
        ▼
all-MiniLM-L6-v2
     Embeddings
        │
        ▼
     ChromaDB
   Vector Collection
        │
        │
        │        User Query
        │             │
        │             ▼
        │      classify_intent
        │             │
        │       ┌─────┴─────┐
        │       │           │
        │   policy       general
        │       │           │
        │       ▼           ▼
        │  retrieve_    direct_answer
        │  and_answer
        │       │
        │       ▼
        └──► ChromaDB
              Retrieval
                 │
                 ▼
          Retrieved Context
                 │
                 ▼
        Mock Generation OR
        Optional Real LLM
                 │
                 ▼
       Pydantic Validation
                 │
                 ▼
             FastAPI
             POST /ask
                 │
                 ▼
           JSON Response
```

The data therefore flows from the eight source documents into chunks, from chunks into local embeddings stored in ChromaDB, from the user's policy query into vector retrieval, and finally from the retrieved context into the answer-generation stage.

The required graded path is completely deterministic and offline when `MOCK_LLM` is left unset or set to `1`.

---

## Module 3 Completion Status

The required graded components of the Support Assistant module have been implemented and verified locally:

* Eight-document Zepto policy corpus
* Local Sentence Transformers embeddings
* ChromaDB vector retrieval
* LangGraph intent routing and retrieval flow
* Deterministic offline mock mode
* Structured Pydantic response
* FastAPI `/ask` endpoint
* Local Docker build and run
* Policy and general-question verification examples


