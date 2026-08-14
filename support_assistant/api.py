"""
Module 3 - Task 5: FastAPI endpoint
Exposes POST /ask, which passes the query into the EXISTING compiled graph
from app.py and returns the validated SupportResponse it produces.
No separate answer-generation logic is implemented here.
"""

from fastapi import FastAPI
from pydantic import BaseModel

from .app import build_graph
from .schemas import SupportResponse

app = FastAPI()

# Compiled once at startup, reused for every request - not rebuilt per call.
compiled_graph = build_graph()


class AskRequest(BaseModel):
    query: str


@app.post("/ask", response_model=SupportResponse)
def ask(request: AskRequest) -> SupportResponse:
    result = compiled_graph.invoke({"query": request.query})
    return result["response"]