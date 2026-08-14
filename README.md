# Zepto AI/ML Project

This repository contains three independent modules, each demonstrating a different data/AI skill set:

| Module | Folder | Status |
|---|---|---|
| 1 — Data Pipeline | `data_pipeline/` | Complete |
| 2 — Analytics & ML | `analytics/` | Complete |
| 3 — GenAI Support Assistant | `support_assistant/` | Complete |

## Module 1 — Data Pipeline

Scrapes book data from books.toscrape.com, cleans it, converts prices to INR using a fixed exchange rate, loads it into a normalized SQLite database, and demonstrates equivalent SQL and pandas approaches to querying it.

See [`data_pipeline/README.md`](data_pipeline/README.md) for full details, installation steps, and design decisions.

## Module 2 — Analytics & Machine Learning

Explores, cleans, and models the Titanic dataset — covering EDA, three classifiers (Logistic Regression, Decision Tree, Random Forest), imbalance handling, hyperparameter tuning, a regression side-task, and a saved end-to-end prediction pipeline.

See [`analytics/README.md`](analytics/README.md) for full details, all written interpretations, the model comparison table, and the final recommendation.

## Module 3 — GenAI Support Assistant

Builds a retrieval-augmented generation (RAG) support assistant for Zepto customer policies.

The module includes:

- Eight-document Zepto policy corpus
- Local `all-MiniLM-L6-v2` embeddings using Sentence Transformers
- ChromaDB vector storage and cosine-similarity retrieval
- LangGraph-based intent routing with three nodes:
  - `classify_intent`
  - `retrieve_and_answer`
  - `direct_answer`
- Deterministic offline `MOCK_LLM` mode as the required graded baseline
- Optional real-LLM path controlled by `MOCK_LLM=0`
- Structured Pydantic response validation
- FastAPI `POST /ask` endpoint
- Dockerized local deployment
- Verification examples for both policy and general questions

The required graded path runs without an LLM API key or external LLM provider.

See [`support_assistant/README.md`](support_assistant/README.md) for the complete RAG architecture, pipeline flow, API usage, verification results, Docker instructions, and `MOCK_LLM` behavior.

## Project-wide setup

- Python 3.13.2
- Virtual environment: `.venv` (not committed — see `.gitignore`)
- Each module has its own `requirements.txt` and README with module-specific installation/run steps.
- Generated ChromaDB vector data is excluded from Git through `.gitignore` and can be regenerated locally using the Module 3 ingestion pipeline.

## How to run this repo

1. Clone the repository.
2. Create and activate a virtual environment (`.venv`).
3. Enter the required module's folder.
4. Follow that module's README for installation and execution instructions.

Module-specific documentation:

- [`data_pipeline/README.md`](data_pipeline/README.md)
- [`analytics/README.md`](analytics/README.md)
- [`support_assistant/README.md`](support_assistant/README.md)