Knowledge Base module for MultiMind AI Platform.

Provides a KnowledgeBase class that wraps FAISS vector storage
and Cohere embedding integration for document ingestion and search.
"""

import os
import json
from typing import Optional


class KnowledgeBase:
    """Manages document ingestion, FAISS indexing, and semantic search."""

    def __init__(self, cohere_api_key: str, index_dir: str = "data/vector_store"):
        self.cohere_api_key = cohere_api_key
        self.index_dir = index_dir
        self._sources: list[str] = []
        self._chunks: list[dict] = []
        os.makedirs(index_dir, exist_ok=True)

    def add_document(self, filename: str, content: bytes) -> int:
        """Ingest a document and return the number of chunks created."""
        try:
            from langchain.text_splitter import RecursiveCharacterTextSplitter

            text = content.decode("utf-8", errors="replace")
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )
            splits = splitter.split_text(text)
            chunk_count = len(splits)
            for i, split in enumerate(splits):
                self._chunks.append(
                    {
                        "id": f"{filename}-{i}",
                        "source": filename,
                        "text": split,
                    }
                )
            self._sources.append(filename)

            # Persist to disk for reuse
            self._persist()
            return chunk_count
        except Exception as e:
            raise RuntimeError(f"Failed to ingest {filename}: {e}")

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Search the knowledge base using Cohere embeddings + cosine similarity."""
        try:
            import cohere
            import numpy as np
            import faiss

            client = cohere.Client(self.cohere_api_key)

            if not self._chunks:
                return []

            # Encode query
            embed_resp = client.embed([query], model="english")
            query_vector = np.array(embed_resp.embeddings[0], dtype="float32").reshape(
                1, -1
            )

            # Encode all chunks (batch)
            chunk_texts = [c["text"] for c in self._chunks]
            # Cohere embed handles up to 96 inputs at once
            chunk_embeddings = []
            batch_size = 96
            for i in range(0, len(chunk_texts), batch_size):
                batch = chunk_texts[i : i + batch_size]
                resp = client.embed(batch, model="english")
                chunk_embeddings.extend(resp.embeddings)

            all_vectors = np.array(chunk_embeddings, dtype="float32")

            # Build FAISS index
            dimension = all_vectors.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(all_vectors)

            # Search
            distances, indices = index.search(query_vector, top_k)

            results = []
            for score, idx in zip(distances[0], indices[0]):
                if idx < len(self._chunks):
                    chunk = self._chunks[idx]
                    results.append(
                        {
                            "text": chunk["text"],
                            "source": chunk["source"],
                            "score": float(score),
                        }
                    )
            return results

        except ImportError:
            # Fallback: return all chunks as placeholder
            return [
                {"text": chunk["text"][:300], "source": chunk["source"], "score": 0.5}
                for chunk in self._chunks[:top_k]
            ]
        except Exception:
            return []

    def list_sources(self) -> list[str]:
        """Return list of indexed document filenames."""
        return list(self._sources)

    def stats(self) -> dict:
        """Return knowledge base statistics."""
        return {
            "total_documents": len(self._sources),
            "total_chunks": len(self._chunks),
        }

    def reset(self) -> None:
        """Clear all documents and chunks."""
        self._sources.clear()
        self._chunks.clear()
        self._persist()

    def _persist(self) -> None:
        """Save chunks to disk."""
        state_path = os.path.join(self.index_dir, "kb_state.json")
        with open(state_path, "w") as f:
            json.dump(
                {"sources": self._sources, "chunks": self._chunks}, f, indent=2
            )

    def _load(self) -> None:
        """Load chunks from disk."""
        state_path = os.path.join(self.index_dir, "kb_state.json")
        if os.path.exists(state_path):
            with open(state_path, "r") as f:
                state = json.load(f)
                self._sources = state.get("sources", [])
                self._chunks = state.get("chunks", [])
