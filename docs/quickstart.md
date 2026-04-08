# Quick Start

This guide walks you through inserting documents and querying them with `lightrag-slim`.
Choose the tab that matches your LLM and embedding setup.

!!! tip "Two steps, always the same"
    1. **Define** an `llm_model_func` and an `embedding_func`
    2. **Use** `LightRAG` — call `initialize_storages()`, `ainsert()`, `aquery()`, then `finalize_storages()`

---

## Complete Examples

=== "DeepSeek + BAAI/bge-m3 (local)"

    **Install dependencies**

    ```bash
    pip install lightrag-slim openai sentence-transformers
    ```

    **Set your API key**

    ```bash
    export DEEPSEEK_API_KEY="sk-..."
    ```

    **Full runnable script**

    ```python title="quickstart_deepseek.py"
    import asyncio
    import os

    import numpy as np
    from openai import AsyncOpenAI

    from lightrag_slim import LightRAG, QueryParam
    from lightrag_slim.utils import wrap_embedding_func_with_attrs

    # ── Config ────────────────────────────────────────────────────────────────
    DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    WORKING_DIR = "./rag_storage"

    # ── LLM function: DeepSeek via OpenAI-compatible SDK ─────────────────────
    _client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

    async def deepseek_llm(
        prompt: str,
        system_prompt: str | None = None,
        history_messages: list[dict] | None = None,
        **kwargs,
    ) -> str:
        messages: list[dict] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if history_messages:
            messages.extend(history_messages)
        messages.append({"role": "user", "content": prompt})
        response = await _client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.0,
        )
        return response.choices[0].message.content or ""

    # ── Embedding function: BAAI/bge-m3 local model (1024-dim, CPU-OK) ───────
    _bge_model = None

    def _load_bge():
        global _bge_model
        if _bge_model is None:
            from sentence_transformers import SentenceTransformer
            print("Loading BAAI/bge-m3 (downloads ~1 GB on first run)…")
            _bge_model = SentenceTransformer("BAAI/bge-m3")
        return _bge_model

    @wrap_embedding_func_with_attrs(embedding_dim=1024, max_token_size=8192)
    async def bge_embedding(texts: list[str]) -> np.ndarray:
        model = _load_bge()
        loop = asyncio.get_event_loop()
        embeddings = await loop.run_in_executor(None, model.encode, texts)
        return np.array(embeddings, dtype=np.float32)

    # ── Main ──────────────────────────────────────────────────────────────────
    async def main() -> None:
        rag = LightRAG(
            working_dir=WORKING_DIR,
            llm_model_func=deepseek_llm,
            embedding_func=bge_embedding,
        )
        await rag.initialize_storages()  # (1)!

        # Insert documents
        await rag.ainsert(
            "LightRAG is a graph-based RAG system that builds a knowledge graph "
            "from documents to answer complex multi-hop questions. It was developed "
            "at The Hong Kong University of Science and Technology."
        )

        # Query
        result = await rag.aquery(
            "What is LightRAG and where was it developed?",
            param=QueryParam(mode="hybrid"),  # (2)!
        )
        print(result)

        await rag.finalize_storages()  # (3)!

    if __name__ == "__main__":
        asyncio.run(main())
    ```

    1. **Always call `initialize_storages()`** before any insert or query. This loads or creates the graph, vector store, and KV cache.
    2. `mode="hybrid"` combines entity-level graph retrieval with community-level context — the recommended default.
    3. **Always call `finalize_storages()`** to flush pending data to disk.

=== "OpenAI + text-embedding-3-small"

    **Install dependencies**

    ```bash
    pip install lightrag-slim openai
    ```

    **Set your API key**

    ```bash
    export OPENAI_API_KEY="sk-..."
    ```

    **Full runnable script**

    ```python title="quickstart_openai.py"
    import asyncio
    import os

    import numpy as np
    from openai import AsyncOpenAI

    from lightrag_slim import LightRAG, QueryParam
    from lightrag_slim.utils import wrap_embedding_func_with_attrs

    # ── Config ────────────────────────────────────────────────────────────────
    WORKING_DIR = "./rag_storage"
    _client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

    # ── LLM function: GPT-4o-mini ─────────────────────────────────────────────
    async def openai_llm(
        prompt: str,
        system_prompt: str | None = None,
        history_messages: list[dict] | None = None,
        **kwargs,
    ) -> str:
        messages: list[dict] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if history_messages:
            messages.extend(history_messages)
        messages.append({"role": "user", "content": prompt})
        response = await _client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.0,
        )
        return response.choices[0].message.content or ""

    # ── Embedding function: text-embedding-3-small (1536-dim) ─────────────────
    @wrap_embedding_func_with_attrs(embedding_dim=1536, max_token_size=8191)
    async def openai_embedding(texts: list[str]) -> np.ndarray:
        response = await _client.embeddings.create(
            model="text-embedding-3-small",
            input=texts,
        )
        return np.array([e.embedding for e in response.data], dtype=np.float32)

    # ── Main ──────────────────────────────────────────────────────────────────
    async def main() -> None:
        rag = LightRAG(
            working_dir=WORKING_DIR,
            llm_model_func=openai_llm,
            embedding_func=openai_embedding,
        )
        await rag.initialize_storages()

        await rag.ainsert(
            "LightRAG is a graph-based RAG system that builds a knowledge graph "
            "from documents to answer complex multi-hop questions."
        )

        result = await rag.aquery(
            "What makes LightRAG different from simple vector search?",
            param=QueryParam(mode="hybrid"),
        )
        print(result)

        await rag.finalize_storages()

    if __name__ == "__main__":
        asyncio.run(main())
    ```

---

## Query Modes

Choose the mode based on the type of question:

| Mode | Best for | How it works |
|---|---|---|
| `naive` | Simple factual lookup | Pure vector similarity search over chunks |
| `local` | Questions about specific entities | Retrieves the entity's direct graph neighbourhood |
| `global` | Broad thematic / summary questions | Uses community-level summaries from the graph |
| `hybrid` | General use — **recommended default** | Combines `local` + `global` retrieval |
| `mix` | Exploratory questions | Merges vector search with graph traversal |

```python
from lightrag_slim import QueryParam

# Change mode here:
result = await rag.aquery("Your question", param=QueryParam(mode="hybrid"))
```

---

## Lifecycle

```
LightRAG(...)                  # 1. Configure — set working_dir, llm, embedding
    │
    ▼
await rag.initialize_storages()  # 2. REQUIRED — loads/creates graph & vector store
    │
    ▼
await rag.ainsert("...")          # 3. Insert — extract entities/relations → graph
await rag.ainsert("...")          #    (can be called many times)
    │
    ▼
await rag.aquery("?", param=...) # 4. Query — retrieve context → LLM generates answer
    │
    ▼
await rag.finalize_storages()    # 5. REQUIRED — flush all pending data to disk
```

!!! warning "Always call `initialize_storages()` and `finalize_storages()`"
    Skipping `initialize_storages()` will raise an error when you first use the RAG.
    Skipping `finalize_storages()` may cause data loss for the current session.

---

## Key Configuration Options

```python
rag = LightRAG(
    working_dir="./rag_storage",      # where all files are stored
    llm_model_func=my_llm,            # your async LLM function
    embedding_func=my_embedding,       # your EmbeddingFunc

    # Chunking
    chunk_token_size=1200,             # max tokens per chunk (default: 1200)
    chunk_overlap_token_size=100,      # overlap between chunks (default: 100)

    # Extraction quality
    entity_extract_max_gleaning=1,     # LLM re-extraction passes (default: 1)

    # Performance
    max_parallel_insert=2,             # concurrent insertion workers (default: 2)
    embedding_batch_num=32,            # texts per embedding batch (default: 32)
)
```
