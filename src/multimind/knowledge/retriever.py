"""Knowledge retriever with semantic search and re-ranking."""

from typing import List, Optional
from ..knowledge.store import VectorStore
from ..knowledge.ingestor import KnowledgeIngestor


class KnowledgeRetriever:
    """Retrieves relevant knowledge chunks using vector similarity search."""

    def __init__(self, vector_store: Optional[VectorStore] = None):
        self.vector_store = vector_store or VectorStore()
        self.ingestor = KnowledgeIngestor()

    async def search(
        self, query: str, top_k: int = 5, source_filter: Optional[str] = None
    ) -> List[dict]:
        """Search for relevant knowledge chunks with optional source filtering."""
        results = self.vector_store.search(query, top_k=top_k)

        if source_filter:
            results = [r for r in results if source_filter in r.get("source", "")]

        return results

    async def add_documents(self, file_paths: list) -> int:
        """Add documents from file paths to the knowledge base."""
        chunks = self.ingestor.ingest_batch(file_paths)
        self.vector_store.add_chunks(chunks)
        self.vector_store.build_index()
        return len(chunks)

    async def add_text(self, text: str, source: str = "manual") -> int:
        """Add raw text to the knowledge base."""
        chunks = self.ingestor.ingest_text(text, source=source)
        self.vector_store.add_chunks(chunks)
        self.vector_store.build_index()
        return len(chunks)

    async def delete_source(self, source: str) -> int:
        """Remove all chunks from a specific source."""
        return self.vector_store.delete_source(source)

    def get_stats(self) -> dict:
        """Return knowledge base statistics."""
        return self.vector_store.get_stats()
