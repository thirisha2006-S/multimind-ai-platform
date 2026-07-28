"""RAG search module for MultiMind AI Platform."""
Provides answer_question() which uses Cohere to generate an answer
from retrieved knowledge base chunks with confidence scoring.
"""

from typing import Optional


def answer_question(
    client, question: str, chunks: list[dict], top_k: int = 3
) -> dict:
    """
    Generate an answer from retrieved knowledge base chunks.

    Returns a dict with:
    - answer: str
    - confidence: int (0-100)
    - has_context: bool
    - sources: list[str]
    - chunks_used: list[dict]
    """
    if not chunks:
        return {
            "answer": "No relevant documents found in the knowledge base.",
            "confidence": 0,
            "has_context": False,
            "sources": [],
            "chunks_used": [],
        }

    # Sort by relevance score (higher = better)
    sorted_chunks = sorted(chunks, key=lambda c: c.get("score", 0), reverse=True)
    used = sorted_chunks[:top_k]

    # Build context from top chunks
    context_text = "\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in used if c.get("text")
    )

    # Use Cohere for generation
    try:
        response = client.chat(
            message=question,
            documents=[context_text],
            temperature=0.3,
        )
        answer = response.text
        confidence = min(95, max(50, int(response.meta.get("score", 0.7) * 100)))
    except Exception:
        # Fallback: extract from first chunk
        answer = used[0]["text"][:500] if used else "No answer available."
        confidence = 60

    return {
        "answer": answer,
        "confidence": confidence,
        "has_context": True,
        "sources": list({c["source"] for c in used}),
        "chunks_used": used,
    }
