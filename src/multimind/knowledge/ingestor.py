"""Document ingestion and chunking for the MultiMind AI knowledge base."""

import os
from typing import List, Optional
from dataclasses import dataclass, field

from langchain.text_splitter import RecursiveCharacterTextSplitter

from ..utils.helpers import generate_id, current_timestamp


@dataclass
class DocumentChunk:
    """A chunk of a document."""
    id: str
    content: str
    source: str
    metadata: dict = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    created_at: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = generate_id("chunk")
        if not self.created_at:
            self.created_at = current_timestamp()


class KnowledgeIngestor:
    """Ingests documents and splits them into searchable chunks."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        self.chunks: List[DocumentChunk] = []

    def ingest_file(self, file_path: str) -> List[DocumentChunk]:
        """Ingest a file and return chunks."""
        if not os.path.exists(file_path):
            return []

        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            content = self._read_pdf(file_path)
        elif ext in (".docx",):
            content = self._read_docx(file_path)
        elif ext in (".xlsx", ".xls", ".csv"):
            content = self._read_excel(file_path)
        elif ext in (".txt", ".md"):
            content = self._read_text(file_path)
        elif ext in (".png", ".jpg", ".jpeg"):
            content = self._read_image(file_path)
        else:
            content = self._read_text(file_path)

        text_chunks = self.splitter.split_text(content)

        new_chunks = []
        for text in text_chunks:
            chunk = DocumentChunk(
                content=text,
                source=file_path,
                metadata={"file_type": ext, "original_file": os.path.basename(file_path)},
            )
            new_chunks.append(chunk)
            self.chunks.append(chunk)

        return new_chunks

    def ingest_text(self, text: str, source: str = "manual") -> List[DocumentChunk]:
        """Ingest raw text and return chunks."""
        text_chunks = self.splitter.split_text(text)

        new_chunks = []
        for chunk_text in text_chunks:
            chunk = DocumentChunk(
                content=chunk_text,
                source=source,
                metadata={"file_type": "text", "original_file": source},
            )
            new_chunks.append(chunk)
            self.chunks.append(chunk)

        return new_chunks

    def ingest_batch(self, file_paths: List[str]) -> List[DocumentChunk]:
        """Ingest multiple files in batch."""
        all_chunks = []
        for path in file_paths:
            chunks = self.ingest_file(path)
            all_chunks.extend(chunks)
        return all_chunks

    def _read_pdf(self, path: str) -> str:
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(path)
            return " ".join(page.extract_text() for page in reader.pages if page.extract_text())
        except ImportError:
            return f"[PDF content from {path} — PyPDF2 not installed]"
        except Exception:
            return f"[Failed to extract PDF from {path}]"

    def _read_docx(self, path: str) -> str:
        try:
            from docx import Document
            doc = Document(path)
            return " ".join(paragraph.text for paragraph in doc.paragraphs)
        except ImportError:
            return f"[DOCX content from {path} — python-docx not installed]"
        except Exception:
            return f"[Failed to extract DOCX from {path}]"

    def _read_excel(self, path: str) -> str:
        try:
            import pandas as pd
            df = pd.read_excel(path)
            return df.to_string()
        except ImportError:
            return f"[Excel content from {path} — openpyxl not installed]"
        except Exception:
            return f"[Failed to extract Excel from {path}]"

    def _read_text(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return f"[Failed to read text file {path}]"

    def _read_image(self, path: str) -> str:
        return f"[Image file {os.path.basename(path)} — visual content requires multimodal model]"
