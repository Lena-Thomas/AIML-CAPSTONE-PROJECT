"""
Module 3 - Task 2: Structured Prompt Template
Defines a reusable prompt template following the role -> context -> task ->
format -> length skeleton, including an explicit negative constraint and a
few-shot example grounded in the real Zepto policy corpus.

This template will be used by the optional MOCK_LLM=0 real-LLM path in a
later task. No LLM/API call happens here - this only builds prompt TEXT.
"""


def build_prompt(query: str, context: str) -> str:
    """
    Build a complete, ready-to-send prompt for the Zepto support assistant.

    Args:
        query: the user's actual question (e.g. "How long do I have to return a damaged item?")
        context: the retrieved policy text to ground the answer in (e.g. the
                 top-3 chunks retrieved from ChromaDB in a later task)

    Returns:
        A single formatted prompt string containing all required sections.
    """
    prompt = f"""ROLE:
You are a Zepto customer support assistant. You answer customer questions strictly using the Zepto policy information provided to you below - you do not use outside knowledge or make assumptions about policies that are not stated.

CONTEXT:
{context}

TASK:
Answer the user's question below using only the information in the CONTEXT section above.

User question: {query}

FORMAT:
Respond in plain, direct sentences (no bullet points, no headers). Answer the question first, then briefly state the specific policy detail (such as a time limit, fee, or condition) that supports your answer.

LENGTH:
Keep the response to 1-3 sentences - concise, like a real support chat reply.

NEGATIVE CONSTRAINT:
Do not answer using information that is not present in the provided context. If the context does not contain enough information to answer the question, say so explicitly rather than guessing or inventing a policy detail.

FEW-SHOT EXAMPLE:
User question: What is the delivery fee for a small order?
Context: "Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation... Standard delivery is free on orders over INR 149; orders below this threshold incur a flat INR 25 delivery fee."
Answer: Orders below INR 149 incur a flat INR 25 delivery fee. Orders over INR 149 get free standard delivery.

Now answer the user's actual question using the CONTEXT provided above.
"""
    return prompt


if __name__ == "__main__":
    # Simple manual verification: build one example prompt and inspect it.
    example_query = "How long do I have to return a damaged item?"
    example_context = (
        "Damaged or Missing Items:\n"
        "\"If an order arrives with damaged, spoiled, or missing items, customers "
        "must report it within 24 hours of delivery through the 'Report an Issue' "
        "button on the order page. Zepto ships a free replacement or issues a full "
        "refund for damaged, spoiled, or missing items without requiring the "
        "customer to return the original item, unless the order value exceeds "
        "INR 1000, in which case a photo of the issue must be submitted through "
        "the report form before a replacement or refund is processed.\""
    )

    generated_prompt = build_prompt(query=example_query, context=example_context)

    print("=" * 60)
    print("GENERATED EXAMPLE PROMPT")
    print("=" * 60)
    print(generated_prompt)

    print("=" * 60)
    print("VERIFICATION CHECKS")
    print("=" * 60)
    checks = {
        "ROLE section present": "ROLE:" in generated_prompt,
        "CONTEXT section present and populated": "CONTEXT:" in generated_prompt and example_context in generated_prompt,
        "TASK section present": "TASK:" in generated_prompt,
        "FORMAT section present": "FORMAT:" in generated_prompt,
        "LENGTH section present": "LENGTH:" in generated_prompt,
        "Negative constraint present": "Do not answer using information that is not present" in generated_prompt,
        "Few-shot example present": "FEW-SHOT EXAMPLE:" in generated_prompt,
        "Query correctly inserted": example_query in generated_prompt,
    }
    for check_name, passed in checks.items():
        print(f"[{'PASS' if passed else 'FAIL'}] {check_name}")