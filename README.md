# Zepto AI/ML Project

This repository contains three independent modules, each demonstrating a different data/AI skill set:

| Module | Folder | Status | Marks |
|---|---|---|---|
| 1 — Data Pipeline | `data_pipeline/` | Complete | 25 |
| 2 — Analytics & ML | `analytics/` | Not started | 50 |
| 3 — GenAI Support Assistant | `support_assistant/` | Not started | 25 |

## Module 1 — Data Pipeline

Scrapes book data from books.toscrape.com, cleans it, converts prices to INR using a fixed exchange rate, loads it into a normalized SQLite database, and demonstrates equivalent SQL and pandas approaches to querying it.

See [`data_pipeline/README.md`](data_pipeline/README.md) for full details, installation steps, and design decisions.

## Module 2 — Analytics & Machine Learning

Will explore, clean, and model the Titanic dataset — covering EDA, classification, regression, and a saved end-to-end prediction pipeline.

Not yet started.

## Module 3 — GenAI Support Assistant

Will build a retrieval-augmented (RAG) support chatbot for Zepto customer policies, served via FastAPI and containerized with Docker, running fully offline in mock mode by default.

Not yet started.

## Project-wide setup

- Python 3.13.2
- Virtual environment: `.venv` (not committed — see `.gitignore`)
- Each module has its own `requirements.txt` and README with module-specific installation/run steps.