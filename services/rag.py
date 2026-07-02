import csv
import io
import numpy as np
import os
import sentence_transformers
import tiktoken as tkn
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
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
        "page_pdf_data": bytes   # Optional one-page PDF if return_image=True
    }
    """

    # Source PDF path
    pdf_path = "data/ThePragmaticProgrammer.pdf"

    # Embedding management
    import json
    from services import llm

    if os.path.exists(CSV_FILE_PATH):
        # Load cached embeddings
        embeddings_data = load_embeddings_from_csv(CSV_FILE_PATH)
    else:
        # Extract and chunk the PDF
        pages = __extract_text_from_pdf(pdf_path)
        chunks = await __chunk_prompt(pages)
        docs = [c[1] for c in chunks]
        page_numbers = [c[0] for c in chunks]

        # Compute embeddings locally
        embeddings = await __calculate_embeddings(docs)

        # Save to CSV for future runs
        save_embeddings_to_csv(
            CSV_FILE_PATH,
            document_name="ThePragmaticProgrammer",
            page_numbers=page_numbers,
            embeddings=embeddings,
            contexts=docs,
        )
        embeddings_data = [
            {
                "document_name": "ThePragmaticProgrammer",
                "page_number": pn,
                "embedding": emb,
                "context": ctx,
            }
            for pn, emb, ctx in zip(page_numbers, embeddings, docs)
        ]

    # Semantic search
    # Build matrix of embeddings
    vectors = np.array([d["embedding"] for d in embeddings_data])
    nn = NearestNeighbors(n_neighbors=3, metric="cosine")
    nn.fit(vectors)

    # Embed the query
    query_emb = LocalEmbeddingGenerator().generate_single_embedding(query)

    # Retrieve top‑k nearest chunks
    distances, indices = nn.kneighbors([query_emb], n_neighbors=3)
    top_idx = indices[0][0]
    top_chunk = embeddings_data[top_idx]
    page_number = top_chunk["page_number"]
    context = top_chunk["context"]

    # Answer generation
    prompt = f"""You are a helpful assistant. Use the following excerpt from *The Pragmatic Programmer* (page {page_number}) to answer the user's question.

Excerpt:
\"\"\"{context}\"\"\"

Question: {query}

Provide a concise answer."""
    answer, _ = llm.converse_sync(prompt, [])

    # Optional page image extraction
    page_pdf_data = None
    if return_image:
        try:
            page_pdf_data = __extract_page_as_pdf(pdf_path, page_number)
        except Exception:
            page_pdf_data = None

    # Return the assembled result
    return {
        "answer": answer,
        "page_number": page_number,
        "context": context,
        "page_pdf_data": page_pdf_data,
    }

def __extract_text_from_pdf(pdf_path: str) -> List[Tuple[int, str]]:
    """
    Extract text content from each page of the PDF.
    Returns: List of (page_number, page_text) tuples
    """
    pages = []
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            pages.append((i + 1, text or ""))
    return pages

def __extract_page_as_pdf(pdf_path: str, page_number: int) -> bytes:
    """
    Extract a single PDF page as a one-page PDF.
    Returns: Raw PDF bytes for the selected page.
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    writer.add_page(reader.pages[page_number - 1])
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()

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
    encoding = tkn.encoding_for_model("gpt-3.5-turbo")
    chunks: List[Tuple[int, str]] = []
    for page_num, text in pages_text:
        tokens = encoding.encode(text)
        if len(tokens) <= chunk_size:
            chunks.append((page_num, text))
        else:
            start = 0
            while start < len(tokens):
                end = min(start + chunk_size, len(tokens))
                chunk_tokens = tokens[start:end]
                chunk_text = encoding.decode(chunk_tokens)
                chunks.append((page_num, chunk_text))
                start += chunk_size - overlap
    return chunks

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
    generator = LocalEmbeddingGenerator()
    embeddings: List[List[float]] = []
    # Process in batches to avoid memory spikes
    for i in range(0, len(documents), batch_size):
        batch = documents[i : i + batch_size]
        batch_emb = generator.generate_embeddings(batch)
        embeddings.extend(batch_emb)
    return embeddings

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
    import json

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(["document_name", "page_number", "embedding", "context"])
        for pn, emb, ctx in zip(page_numbers, embeddings, contexts):
            writer.writerow([document_name, pn, json.dumps(emb), ctx])

def load_embeddings_from_csv(file_path: str) -> List[dict]:
    """
    Load previously cached embeddings from CSV.

    Returns: List of dicts with keys:
        - document_name: str
        - page_number: int
        - embedding: List[float]
        - context: str
    """
    import json

    embeddings = []
    if not os.path.exists(file_path):
        return embeddings
    with open(file_path, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            embeddings.append(
                {
                    "document_name": row["document_name"],
                    "page_number": int(row["page_number"]),
                    "embedding": json.loads(row["embedding"]),
                    "context": row["context"],
                }
            )
    return embeddings
