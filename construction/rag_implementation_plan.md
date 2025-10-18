# RAG Implementation Plan for `services/rag.py`

This document outlines a step‑by‑step plan for implementing the Retrieval‑Augmented Generation (RAG) functionality used by the Quick Chat feature. Each step is represented as a checklist item that can be marked as completed during development.

---

## ✅ Plan Checklist

- [ ] **Extract PDF Text**
  - Implement `__extract_text_from_pdf` to read each page of `ThePragmaticProgrammer.pdf` and return a list of `(page_number, page_text)` tuples.

- [ ] **Convert PDF Page to Image**
  - Implement `__extract_page_as_image` to render a specific page as a PNG byte stream using `pdf2image`.

- [ ] **Chunk Text**
  - Implement `__chunk_prompt` to create chunks from the extracted pages.
  - Primary strategy: one chunk per page (easy mapping to page numbers).
  - Optional: split overly long pages using token counting (`tiktoken`) with configurable `chunk_size` and `overlap`.

- [ ] **Calculate Embeddings**
  - Implement `__calculate_embeddings` using the provided `LocalEmbeddingGenerator` (model `all-mpnet-base-v2`).
  - Process documents in batches (default `batch_size=20`) and return a list of embedding vectors.

- [ ] **Cache Embeddings**
  - Implement `save_embeddings_to_csv` to write embeddings, page numbers, and context to `data/ThePragmaticProgrammer.embeddings.csv`.
  - Implement `load_embeddings_from_csv` to read the CSV back into a list of dictionaries.

- [ ] **Nearest‑Neighbor Search**
  - In `ask_book`, after loading embeddings, fit a `sklearn.neighbors.NearestNeighbors` model (cosine metric) and retrieve the top‑k most similar chunks for a given query embedding.

- [ ] **Prompt Construction**
  - Build a prompt that includes the retrieved context, the original user query, and clear instructions for the LLM.
  - Example format:
    ```
    You are a helpful assistant. Use the following excerpt from *The Pragmatic Programmer* (page {page_number}) to answer the user's question.

    Excerpt:
    """{context}"""

    Question: {query}
    ```

- [ ] **LLM Call**
  - Use `services.llm.converse_sync` to obtain an answer from the LLM.
  - Pass the constructed prompt and an empty message list (or a starter if needed).

- [ ] **Optional Image Retrieval**
  - If `return_image=True`, call `__extract_page_as_image` for the most relevant page and include the PNG bytes in the result.

- [ ] **Return Result**
  - Assemble a dictionary with keys:
    - `answer` (LLM response)
    - `page_number` (page of the top chunk)
    - `context` (text of the top chunk)
    - `image_data` (optional PNG bytes)

- [ ] **Error Handling & Logging**
  - Add try/except blocks around PDF operations, embedding generation, and LLM calls.
  - Ensure that `book_handler.ask_book` receives a fallback response when errors occur.

- [ ] **Testing**
  - After implementation, run a quick manual test (e.g., query “What is the main idea of chapter 1?”) to verify:
    - Embeddings are generated/cached correctly.
    - Semantic search returns relevant pages.
    - LLM answer is returned.
    - Image data is returned when requested.

- [ ] **Documentation**
  - Add docstrings to all new functions.
  - Update any relevant README sections to describe the RAG feature.

---

## 📌 Notes

- The plan follows the hints provided in the assignment description and the example notebooks (`chunking-pruning-tutorial.ipynb`, `embeddings-tutorial.ipynb`).
- All implementations will be placed inside `services/rag.py` without altering its public interface.
- The checklist can be updated in this file as each step is completed (replace `[ ]` with `[x]`).

--- 

*End of plan.*
