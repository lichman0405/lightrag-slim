# lightrag-slim

> A slim, standalone extraction of the **core graph-based RAG pipeline** from the outstanding [LightRAG](https://github.com/HKUDS/LightRAG) project.

---

## Acknowledgements & Credits

**This project would not exist without the exceptional work of the LightRAG team.**

[LightRAG](https://github.com/HKUDS/LightRAG) is a brilliant, production-grade Retrieval-Augmented Generation framework built by researchers at The Hong Kong University of Science and Technology. It introduces a graph-aware dual-level retrieval paradigm that fundamentally outperforms naive RAG on complex, multi-hop questions. The elegant design of its entity/relation extraction pipeline, the multi-mode query system (naive / local / global / hybrid), and the cross-process shared storage architecture are truly impressive pieces of engineering.

### Please support the original project ⭐

If `lightrag-slim` is useful to you, the credit belongs to the original authors. **Please go to the original repository, give it a star, and consider forking it.**

| Resource | Link |
|---|---|
| GitHub Repository | [https://github.com/HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) |
| Research Paper (arXiv) | [LightRAG: Simple and Fast Retrieval-Augmented Generation](https://arxiv.org/abs/2410.05779) |
| Authors | Zirui Guo, Lianghao Xia, Yanhua Yu, Tu Ao, Chao Huang |

> **Citation** (BibTeX):
> ```bibtex
> @article{guo2024lightrag,
>   title={LightRAG: Simple and Fast Retrieval-Augmented Generation},
>   author={Guo, Zirui and Xia, Lianghao and Yu, Yanhua and Ao, Tu and Huang, Chao},
>   journal={arXiv preprint arXiv:2410.05779},
>   year={2024}
> }
> ```

---

## What is lightrag-slim?

`lightrag-slim` strips the LightRAG repository down to its essential retrieval engine. It removes the FastAPI server, React WebUI, evaluation framework, 13+ optional storage backends (Neo4j, PostgreSQL, MongoDB, Redis, Milvus, Qdrant, …), and all LLM provider bindings, keeping only:

- The core graph-based knowledge extraction and retrieval pipeline
- 4 lightweight, file-based storage backends (NetworkX, NanoVectorDB, JSON KV, JSON Doc Status)
- A clean Python API with no opinionated LLM/embedding vendor lock-in

The result is a library you can embed directly into any Python application or agent framework, supplying your own `llm_model_func` and `embedding_func`.

### Dependency footprint

| | LightRAG | lightrag-slim |
|---|---|---|
| Core dependencies | 18+ | **8** |
| Optional backends removed | — | Neo4j, PostgreSQL, MongoDB, Redis, Milvus, Qdrant, Chroma, Oracle, … |
| LLM bindings removed | — | OpenAI, Anthropic, Gemini, Ollama, … |
| API server | FastAPI + Gunicorn | **removed** |
| WebUI | React 19 + TypeScript | **removed** |

---

## Installation

```bash
pip install lightrag-slim
```

Or from source:

```bash
git clone https://github.com/your-org/lightrag-slim.git
cd lightrag-slim
pip install -e .
```

**Requires Python ≥ 3.10**

---

## Quick Start

You bring your own LLM and embedding functions; `lightrag-slim` handles the rest.

```python
import asyncio
import numpy as np
from lightrag_slim import LightRAG, QueryParam
from lightrag_slim.utils import EmbeddingFunc

# --- 1. Define your LLM function ---
async def my_llm(
    prompt: str,
    system_prompt: str | None = None,
    history_messages: list | None = None,
    **kwargs,
) -> str:
    # Replace with any LLM call (OpenAI, Anthropic, DeepSeek, local Ollama, …)
    raise NotImplementedError("Provide your own LLM function")

# --- 2. Define your embedding function ---
@EmbeddingFunc.wrap(embedding_dim=1024, max_token_size=8192)
async def my_embedding(texts: list[str]) -> np.ndarray:
    # Replace with any embedding call (OpenAI, BGE, Cohere, local model, …)
    raise NotImplementedError("Provide your own embedding function")

# --- 3. Create and initialize the RAG engine ---
async def main():
    rag = LightRAG(
        working_dir="./rag_storage",
        llm_model_func=my_llm,
        embedding_func=my_embedding,
    )
    await rag.initialize_storages()

    # Insert documents
    await rag.ainsert("Your document text goes here…")

    # Query in different modes
    result = await rag.aquery("Your question?", param=QueryParam(mode="hybrid"))
    print(result)

    await rag.finalize_storages()

asyncio.run(main())
```

### Query modes

| Mode | Description |
|---|---|
| `naive` | Simple vector similarity search |
| `local` | Entity-centric local context (best for specific entity questions) |
| `global` | Community summary-level global context (best for broad thematic questions) |
| `hybrid` | Combines local + global (recommended default) |
| `mix` | Merges vector search with graph traversal |

---

## Architecture Overview

```
Your Application
       │
       ▼
  LightRAG (lightrag.py)          ← orchestrator
       │
       ├── operate.py             ← chunking, extraction, querying
       │        │
       │        └── prompt.py     ← all LLM prompt templates
       │
       └── Storage Layer (kg/)
                ├── NetworkXStorage      (knowledge graph)
                ├── NanoVectorDBStorage  (vector embeddings)
                ├── JsonKVStorage        (key-value cache)
                └── JsonDocStatusStorage (document tracking)
```

### Lifecycle

```python
rag = LightRAG(...)           # configure
await rag.initialize_storages()  # REQUIRED before use
await rag.ainsert(...)           # extract entities/relations → populate graph
await rag.aquery(...)            # retrieve and answer
await rag.finalize_storages()    # flush to disk
```

---

## Configuration

Key parameters passed to `LightRAG(...)`:

| Parameter | Default | Description |
|---|---|---|
| `working_dir` | required | Directory for all storage files |
| `llm_model_func` | required | Async function: `(prompt, ...) → str` |
| `embedding_func` | required | `EmbeddingFunc` wrapping: `(texts) → np.ndarray` |
| `chunk_token_size` | `1200` | Max tokens per document chunk |
| `chunk_overlap_token_size` | `100` | Overlap between adjacent chunks |
| `entity_extract_max_gleaning` | `1` | Max re-extraction passes for entities |
| `max_parallel_insert` | `2` | Concurrent insertion workers |
| `embedding_batch_num` | `32` | Texts per embedding batch |

---

## Storage Files

All data is stored in `working_dir/` as plain files — no database server required:

| File | Backend | Contents |
|---|---|---|
| `graph_chunk_entity_relation.graphml` | NetworkX | Knowledge graph |
| `vdb_entities.json` | NanoVectorDB | Entity embeddings |
| `vdb_relationships.json` | NanoVectorDB | Relation embeddings |
| `vdb_chunks.json` | NanoVectorDB | Chunk embeddings |
| `kv_store_*.json` | JSON | Cached LLM responses, document metadata |
| `kv_store_doc_status.json` | JSON | Document insertion status |

---

## Differences from LightRAG

| Feature | LightRAG | lightrag-slim |
|---|---|---|
| Core RAG pipeline | ✅ | ✅ |
| All 4 query modes | ✅ | ✅ |
| File-based storage | ✅ | ✅ |
| REST API server | ✅ | ❌ removed |
| Web UI | ✅ | ❌ removed |
| 13+ storage backends | ✅ | ❌ removed (keep 4) |
| 12+ LLM provider bindings | ✅ | ❌ removed (BYO) |
| Evaluation framework | ✅ | ❌ removed |
| pandas / Excel export | ✅ | ❌ removed |
| pypinyin (optional) | ✅ | ⚠️ optional, graceful fallback |

---

## License

MIT — same as the original LightRAG.

This project is a derivative of [LightRAG](https://github.com/HKUDS/LightRAG). All original algorithmic contributions belong to the LightRAG authors. Please cite their paper if you use this in academic work.
