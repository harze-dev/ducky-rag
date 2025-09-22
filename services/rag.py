import csv
import io
import numpy as np
import os
import sentence_transformers
import tiktoken as tkn
from PIL import Image
from PyPDF2 import PdfFileReader
from openai import OpenAI
from pdf2image import convert_from_path
from sklearn.neighbors import NearestNeighbors
from typing import List, Tuple

# Global configuration
EMBEDDING_MODEL = "text-embedding-3-small"  # OpenAI's best embeddings as of Feb 2024
CSV_FILE_PATH = "data/ThePragmaticProgrammer.embeddings.csv"

async def ask_book(query: str, return_image: bool = False):
    """
    Main RAG (Retrieval Augmented Generation) implementation.
    Takes a query about the book and returns relevant information with optional page image.

    Returns:
    {
        "answer": str,           # Generated response using context
        "page_number": int,      # Page where context was found
        "context": str,          # Text chunk used for answer
        "image_data": bytes      # Optional PNG of page if return_image=True
    }
    """

    # Source PDF path
    pdf_path = "data/ThePragmaticProgrammer.pdf"

    # TODO: Implement embedding management
    # 1. Check if embeddings exist in CSV_FILE_PATH
    # 2. If not:
    #    - Extract text from PDF using __extract_text_from_pdf()
    #    - Chunk the text (see chunking strategy note below)
    #    - Calculate embeddings using OpenAI API
    #    - Save to CSV for future use
    # 3. Load embeddings from CSV
    pass

    # TODO: Implement semantic search
    # 1. Set up nearest neighbors search with sklearn
    # 2. Get embedding for user's query
    # 3. Find most relevant context using cosine similarity
    pass

    # TODO: Implement answer generation
    # 1. Format prompt with context and query
    # 2. Get response from LLM (NOTE: use services.llm.converse_sync method for this)
    # 3. Package results with page number and context
    pass

    # TODO: Optional - Handle page image extraction
    # 1. Convert PDF page to image
    # 2. Return as PNG bytes
    pass

def __extract_text_from_pdf(pdf_path: str) -> List[Tuple[int, str]]:
    """
    Extract text content from each page of the PDF.
    Returns: List of (page_number, page_text) tuples
    """
    pass

def __extract_page_as_image(pdf_path: str, page_number: int) -> bytes:
    """
    Convert a specific PDF page to a PNG image.
    Returns: Raw PNG image data as bytes
    """
    pass

async def __chunk_prompt(pages_text: List[Tuple[int, str]], chunk_size: int = 1500, overlap: int = 50) -> List[Tuple[int, str]]:
    """
    Split text into chunks suitable for embedding.

    Note: For a good chunking implementation example, see:
    http://aitools.cs.vt.edu:8888/edit/module5/chunking-pruning-tutorial.ipynb

    Hint: Consider using one chunk per page as a starting strategy.
    This makes it easier to track context and display relevant pages.

    Args:
        pages_text: List of (page_number, text) tuples
        chunk_size: Target size for each chunk in tokens
        overlap: Number of tokens to overlap between chunks

    Returns: List of (page_number, chunk_text) tuples
    """
    pass

# TODO: Use this local embedding generator to embed text without network API calls
LOCAL_EMBEDDING_MODEL = "all-mpnet-base-v2"  # Better accuracy local model (~420MB)
class LocalEmbeddingGenerator():
    """Local embedding generator using sentence-transformers."""

    def __init__(self, model_name: str = LOCAL_EMBEDDING_MODEL):
        self.model_name = model_name
        self._model = None
        self._dimension = None

    def _load_model(self):
        """Lazy load the sentence transformer model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                print(f"Loading local embedding model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name, device="cpu")
                # Test embedding to get dimension
                test_embedding = self._model.encode(["test"], normalize_embeddings=True)
                self._dimension = test_embedding.shape[1]
                print(f"Local embedding model loaded. Dimension: {self._dimension}")
            except ImportError:
                raise ImportError(
                    "sentence-transformers is required for local embeddings. Install with: pip install sentence-transformers")
            except Exception as e:
                raise RuntimeError(f"Failed to load local embedding model {self.model_name}: {e}")

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        self._load_model()
        embeddings = self._model.encode(texts, batch_size=32, normalize_embeddings=True)
        return embeddings.tolist()

    def generate_single_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        self._load_model()
        embedding = self._model.encode([text], normalize_embeddings=True)
        return embedding[0].tolist()

    @property
    def embedding_dimension(self) -> int:
        """Return the dimension of the embeddings."""
        if self._dimension is None:
            self._load_model()
        return self._dimension


async def __calculate_embeddings(documents: List[str], batch_size: int = 20) -> List[List[float]]:
    """
    Get embeddings for text chunks using sentence transformers.

    Hint: Use the local embedding generator above for offline embedding.

    Args:
        documents: List of text chunks to embed
        batch_size: Number of chunks to process at once

    Returns: List of embedding vectors (each vector is List[float])
    """
    pass

def save_embeddings_to_csv(file_path: str, document_name: str, page_numbers: List[int], embeddings: List[List[float]], contexts: List[str]):
    """
    Cache embeddings to CSV for faster future lookups.

    CSV Format:
    document_name, page_number, embedding, context

    Args:
        file_path: Where to save the CSV
        document_name: Identifier for the source document
        page_numbers: List of page numbers for each chunk
        embeddings: List of embedding vectors
        contexts: List of text chunks
    """
    pass

def load_embeddings_from_csv(file_path: str) -> List[dict]:
    """
    Load previously cached embeddings from CSV.

    Returns: List of dicts with keys:
        - document_name: str
        - page_number: int
        - embedding: List[float]
        - context: str
    """
    pass
