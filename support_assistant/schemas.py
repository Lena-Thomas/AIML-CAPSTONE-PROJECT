"""
Module 3 - Task 4: Pydantic Structured Response
Defines SupportResponse, the validated output shape for the support graph.
"""

from pydantic import BaseModel, Field


class SupportResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(ge=0.0, le=1.0)  # constrained to [0, 1]