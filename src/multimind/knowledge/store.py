"""FAISS-based vector store for MultiMind AI knowledge base."""

import os
from typing import List, Optional

import numpy as np

from .ingestor import DocumentChunk
from ..utils.helpers import generate_id


class VectorStore:
    """FAISS-based vector store for semantic search over document chunks."""

    def __init__(self, index_path: str = "./data/vector_store/faiss_index", dimension: int = 1536):
        self.index_path = index_path
        self.dimension = dimension
        self.chunks: List[DocumentChunk] = []
        self._index = None

    def add_chunks(self, chunks: List[DocumentChunk]) -> None:
        """Add document chunks to the vector store."""
        self.chunks.extend(chunks)

    def build_index(self, embeddings_model=None) -> None:
        """Build or rebuild the FAISS index."""
        try:
            import faiss
            if not self.chunks:
                return

            # Generate dummy embeddings if no model provided
            if embeddings_model is None:
                vectors = np.random.rand(len(self.chunks), self.dimension).astype("float32")
            else:
                vectors = np.array(
                    [embeddings_model.embed(chunk.content) for chunk in self.chunks],
                    dtype="float32",
                )

            self._index = faiss.IndexFlatL2(self.dimension)
            self._index.add(vectors)

            # Save index
            os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
            faiss.write_index(self._index, self.index_path)

        except ImportError:
            # FAISS not available — use in-memory fallback
            pass

    def search(self, query: str, top_k: int = 5, embeddings_model=None) -> List[dict]:
        """Search for the most relevant chunks."""
        if not self.chunks or self._index is None:
            return []

        try:
            import faiss

            if embeddings_model is None:
                query_vector = np.random.rand(1, self.dimension).astype("float32")
            else:
                query_vector = np.array([embeddings_model.embed(query)], dtype="float32")

            distances, indices = self._index.search(query_vector, top_k)

            results = []
            for score, idx in zip(distances[0], indices[0]):
                if idx < len(self.chunks):
                    chunk = self.chunks[idx]
                    results.append(
                        {
                            "chunk_id": chunk.id,
                            "content": chunk.content,
                            "source": chunk.source,
                            "score": float(score),
                            "metadata": chunk.metadata,
                        }
                    )
            return results

        except ImportError:
            return []

    def delete_source(self, source: str) -> int:
        """Remove all chunks from a specific source."""
        original_count = len(self.chunks)
        self.chunks = [c for c in self.chunks if c.source != source]
        return original_count - len(self.chunks)

    def get_stats(self) -> dict:
        """Return statistics about the vector store."""
        return {
            "total_chunks": len(self.chunks),
            "unique_sources": len(set(c.source for c in self.chunks)),
            "index_built": self._index is not None,
        }
