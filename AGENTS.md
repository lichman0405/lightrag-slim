# Repository Guidelines — lightrag-slim

## Project Overview

`lightrag-slim` is a standalone lightweight RAG (Retrieval-Augmented Generation) engine extracted from [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG). It retains only the core graph-based knowledge retrieval pipeline and minimal file-based storage backends, removing the API server, WebUI, evaluation layer, tool layer, and 13+ optional storage/LLM backends.

**Package name**: `lightrag_slim`
**Project path**: `/home/shibo/projects/lightrag-slim/`
**Source**: Forked core from LightRAG (April 2026 main branch)

## Architecture

### Core Files (from LightRAG, with `lightrag.` → `lightrag_slim.` import rename)
- `lightrag.py`: Main `LightRAG` orchestrator class. Critical: always call `await rag.initialize_storages()` after instantiation.
- `operate.py`: Core extraction and query operations (entity/relation extraction, chunking, retrieval).
- `base.py`: Abstract base classes for storage backends.
- `prompt.py`: All LLM prompt templates.
- `utils.py`: Shared utilities. pandas Excel export removed. pypinyin optional (falls back to string sort).
- `utils_graph.py`: Graph-specific utilities.
- `exceptions.py`: Custom exceptions. **Fully rewritten** — no httpx dependency.
- `constants.py`, `types.py`, `namespace.py`, `_version.py`, `__init__.py`: Supporting modules.

### Storage Backends (kept 4 out of 25+)
Located in `lightrag_slim/kg/`:
- `json_kv_impl.py` — JsonKVStorage (KV store)
- `nano_vector_db_impl.py` — NanoVectorDBStorage (vector embeddings)
- `networkx_impl.py` — NetworkXStorage (knowledge graph)
- `json_doc_status_impl.py` — JsonDocStatusStorage (document tracking)
- `shared_storage.py` — Shared storage utilities
- `__init__.py` — STORAGES registry (slimmed to 4 entries)

### Removed from LightRAG
- `api/` — FastAPI server, routers, Gunicorn launcher
- `lightrag_webui/` — React 19 + TypeScript frontend
- `evaluation/` — Evaluation framework
- `tools/` — Agent tools
- `llm/` — All 12+ LLM provider bindings (users supply their own `llm_model_func`)
- 9+ storage backends (Neo4j, PostgreSQL, MongoDB, Redis, Milvus, Qdrant, etc.)

## Dependencies

8 core dependencies (down from 18):
```
json-repair, nano-vectordb, networkx, numpy, pydantic, python-dotenv, tiktoken
```

Removed: google-genai, google-api-core, pandas, pypinyin, xlsxwriter, pipmaster, configparser, aiohttp, tenacity, setuptools

## Key Modifications from LightRAG

1. **exceptions.py**: Completely rewritten. `APIStatusError` takes `status_code: int` instead of `httpx.Response`. No httpx imports.
2. **kg/__init__.py**: STORAGES dict reduced to 4 entries. `STORAGE_IMPLEMENTATIONS` and `STORAGE_ENV_REQUIREMENTS` slimmed.
3. **lightrag.py**: `_get_storage_class` simplified — no fallback dynamic import via `lazy_external_import`, raises `ValueError` for unknown storage names.
4. **utils.py**: pandas Excel export branch removed (lines with `import pandas as pd` / `pd.ExcelWriter`).

## Build & Development

```bash
# Create env and install (python3-venv may not be available; use uv)
uv venv .venv
source .venv/bin/activate
uv pip install -e .

# Verify import
python -c "from lightrag_slim import LightRAG, QueryParam; print('OK')"

# Lint
ruff check .

# Test (once configured)
python -m pytest tests/
```

## Coding Style
- Follow PEP 8, 4-space indentation
- Type annotations on functions
- Use `lightrag_slim.utils.logger` instead of print
- Async/await throughout

## Current Status & Remaining Work

### Completed (Steps 1-9)
- [x] Project initialization with pyproject.toml
- [x] Core file copy from LightRAG
- [x] Import rename `lightrag.` → `lightrag_slim.`
- [x] Dependency cleanup (18 → 8)
- [x] exceptions.py rewrite (remove httpx)
- [x] kg/__init__.py slim (25+ → 4 backends)
- [x] lightrag.py cleanup (remove fallback dynamic import)
- [x] utils.py cleanup (remove pandas export)
- [x] Install test passed (`uv pip install -e .` + import verification)
- [x] Real functional test passed — all 5 tests green (302s total)
  - LLM: DeepSeek `deepseek-chat` via OpenAI-compatible SDK
  - Embedding: BAAI/bge-m3 (1024-dim) via sentence-transformers locally
  - Tests: insert, query (naive/local/hybrid), graph population verified
  - Bug fixed: `workspace=tmp_path.name` isolates shared_storage in-memory state per test

### TODO: Phase 4 — MiQi Integration
**Goal**: Integrate lightrag-slim into [MiQi](https://github.com/lichman0405/MiQi.git) as an Agent Tool.

MiQi is an AI agent runtime at `/home/shibo/projects/MiQi/`:
- Uses direct openai/anthropic SDKs (NO litellm)
- Tool-based architecture: `Tool` ABC + `ToolRegistry`
- 22+ LLM providers via registry
- No existing RAG capability

**Integration plan**:
1. Create `miqi/agent/tools/rag.py` with `RAGTool` class (rag_insert / rag_query / rag_delete)
2. Write LLM adapter: MiQi `LLMProvider.chat()` → LightRAG `llm_model_func` signature
3. Write Embedding adapter: wrap external embedding service → LightRAG `embedding_func`
4. Register RAGTool in MiQi's tool system
5. Add RAG config section to MiQi config
6. Test end-to-end

**Key interfaces**:
- LightRAG `llm_model_func`: `async (prompt, system_prompt, history_messages, keyword_extraction, **kwargs) -> str`
- LightRAG `embedding_func`: `async (texts: list[str]) -> np.ndarray` (use `@wrap_embedding_func_with_attrs`)
- MiQi `LLMProvider.chat()`: `async (messages, tools, model, max_tokens, temperature) -> LLMResponse`
- MiQi `Tool` ABC: needs `name`, `description`, `parameters` properties

## Technical Decisions
- **Integration method**: MiQi Agent Tool (direct Python call), NOT MCP Server
- **Storage**: Default file-based (JSON + NanoVectorDB + NetworkX)
- **LLM**: Bridge MiQi provider system via adapter
- **Scope**: Global knowledge base, independent from MiQi Memory, agent-autonomous query triggering
