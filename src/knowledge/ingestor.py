"""Document ingestion and processing for knowledge base."""

from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel


class DocumentChunk(BaseModel):
    id: str
    content: str
    source: str
    metadata: dict = {}
    embedding: Optional[List[float]] = None


class KnowledgeIngestor(ABC):
    """Abstract base class for document ingesters."""

    @abstractmethod
    async def ingest(self, source: str, content: str) -> List[DocumentChunk]:
        """Ingest a document and return chunks."""
        pass

    @abstractmethod
    async def ingest_batch(self, sources: List[str]) -> List[DocumentChunk]:
        """Ingest multiple documents in batch."""
        pass
