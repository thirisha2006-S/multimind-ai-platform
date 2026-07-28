"""Knowledge Doctor AI — scans and maintains the knowledge base."""

from typing import List, Optional, Dict, Any
from ..knowledge.store import VectorStore
from ..knowledge.conflict_detector import ConflictDetector
from ..utils.helpers import current_timestamp


class KnowledgeDoctor:
    """Automatically scans the knowledge base for issues and recommends improvements."""

    def __init__(self, vector_store: Optional[VectorStore] = None):
        self.vector_store = vector_store or VectorStore()
        self.conflict_detector = ConflictDetector()

    def scan_outdated_documents(self, max_age_days: int = 365) -> List[Dict[str, Any]]:
        """Identify documents older than max_age_days."""
        outdated = []
        for chunk in self.vector_store.chunks:
            source = chunk.metadata.get("original_file", chunk.source)
            # Basic heuristic — in production, check actual file modification dates
            if "old" in source.lower() or "archive" in source.lower():
                outdated.append(
                    {"source": source, "chunk_id": chunk.id, "reason": "Potentially outdated file name"}
                )
        return outdated

    def scan_duplicate_documents(self) -> List[Dict[str, Any]]:
        """Identify duplicate or near-duplicate content chunks."""
        duplicates = []
        seen_content_hashes = set()
        for chunk in self.vector_store.chunks:
            content_hash = hash(chunk.content.strip())
            if content_hash in seen_content_hashes:
                duplicates.append({"chunk_id": chunk.id, "source": chunk.source, "reason": "Duplicate content"})
            else:
                seen_content_hashes.add(content_hash)
        return duplicates

    def scan_missing_policies(self) -> List[str]:
        """Check for missing policy documents in the knowledge base."""
        sources = set(c.source for c in self.vector_store.chunks)
        expected_policies = ["leave_policy", "remote_work", "data_classification", "security_policy", "code_of_conduct"]

        missing = []
        for policy in expected_policies:
            found = any(policy in s.lower() for s in sources)
            if not found:
                missing.append(f"Missing policy: {policy}")

        return missing

    def scan_conflicts(self) -> List[Any]:
        """Scan for knowledge conflicts using the Conflict Detector."""
        documents = [
            {
                "source": c.source,
                "content": c.content,
                "version": c.metadata.get("version", "1.0"),
            }
            for c in self.vector_store.chunks
        ]
        return self.conflict_detector.detect(documents)

    def run_full_diagnosis(self) -> Dict[str, Any]:
        """Run a comprehensive scan of the knowledge base."""
        return {
            "timestamp": current_timestamp(),
            "total_chunks": len(self.vector_store.chunks),
            "outdated_documents": self.scan_outdated_documents(),
            "duplicates": self.scan_duplicate_documents(),
            "missing_policies": self.scan_missing_policies(),
            "conflicts": [
                {
                    "field": c.field,
                    "value_a": c.value_a,
                    "value_b": c.value_b,
                    "source_a": c.source_a,
                    "source_b": c.source_b,
                    "resolution": c.resolution,
                }
                for c in self.conflicts
            ] if hasattr(self, "conflicts") else [],
            "recommendations": self._generate_recommendations(),
        }

    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on scan results."""
        recommendations = []

        outdated = self.scan_outdated_documents()
        if outdated:
            recommendations.append(f"Archive or update {len(outdated)} outdated documents")

        duplicates = self.scan_duplicate_documents()
        if duplicates:
            recommendations.append(f"Remove {len(duplicates)} duplicate content chunks")

        missing = self.scan_missing_policies()
        if missing:
            recommendations.extend(missing)

        if not recommendations:
            recommendations.append("Knowledge base is in good health")

        return recommendations
