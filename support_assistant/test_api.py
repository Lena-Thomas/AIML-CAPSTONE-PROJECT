"""
Module 3 - Automated API verification
Uses FastAPI's TestClient to send real requests through the actual `app`
object. Test queries updated to match the exact 2-category design
(policy_question / general_question) and the exact required keyword list.
"""

import os
from fastapi.testclient import TestClient
from support_assistant.api import app

client = TestClient(app)

test_cases = [
    ("Policy question (should retrieve)", {"query": "How long do I have to return a damaged item?"}),
    ("General question (should NOT retrieve)", {"query": "What is the capital of France?"}),
]

print(f"MOCK_LLM env value: {os.environ.get('MOCK_LLM', '(unset, defaults to mock)')}")
print()

for label, payload in test_cases:
    print("=" * 60)
    print(f"TEST: {label}")
    print(f"Request: POST /ask {payload}")
    print("-" * 60)

    response = client.post("/ask", json=payload)

    print(f"HTTP status code: {response.status_code}")
    print(f"JSON response: {response.json()}")
    print()

print("=" * 60)
print("TEST: Invalid input (missing 'query' field)")
print("-" * 60)
bad_response = client.post("/ask", json={})
print(f"HTTP status code: {bad_response.status_code}")
print(f"JSON response: {bad_response.json()}")
