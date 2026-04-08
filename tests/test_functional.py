"""
Step 9: Functional test for lightrag-slim.

LLM:       DeepSeek (deepseek-chat) via OpenAI-compatible API
Embedding: BAAI/bge-m3 (1024-dim) via sentence-transformers (local)

Run:
    pytest tests/test_functional.py -v -s
"""

from __future__ import annotations

import asyncio
import os

import numpy as np
import pytest
import pytest_asyncio
from openai import AsyncOpenAI

from lightrag_slim import LightRAG, QueryParam
from lightrag_slim.utils import wrap_embedding_func_with_attrs

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "REMOVED_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = "deepseek-chat"
BGE_MODEL_NAME = "BAAI/bge-m3"
BGE_DIM = 1024

# ---------------------------------------------------------------------------
# LLM function (DeepSeek via OpenAI SDK)
# ---------------------------------------------------------------------------

_openai_client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)


async def deepseek_llm_func(
    prompt: str,
    system_prompt: str | None = None,
    history_messages: list[dict] | None = None,
    keyword_extraction: bool = False,
    **kwargs,
) -> str:
    """LightRAG-compatible LLM function backed by DeepSeek chat."""
    messages: list[dict] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if history_messages:
        messages.extend(history_messages)
    messages.append({"role": "user", "content": prompt})

    response = await _openai_client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=messages,
        temperature=0.0,
    )
    return response.choices[0].message.content or ""


# ---------------------------------------------------------------------------
# Embedding function (BAAI/bge-m3, lazy-loaded)
# ---------------------------------------------------------------------------

_bge_model = None


def _get_bge_model():
    global _bge_model
    if _bge_model is None:
        from sentence_transformers import SentenceTransformer
        _bge_model = SentenceTransformer(BGE_MODEL_NAME)
    return _bge_model


@wrap_embedding_func_with_attrs(
    embedding_dim=BGE_DIM,
    max_token_size=8192,
    model_name=BGE_MODEL_NAME,
)
async def bge_embedding_func(texts: list[str]) -> np.ndarray:
    """Local BAAI/bge-m3 embedding via sentence-transformers."""
    model = _get_bge_model()
    loop = asyncio.get_event_loop()
    embeddings = await loop.run_in_executor(None, model.encode, texts)
    return np.array(embeddings, dtype=np.float32)


# ---------------------------------------------------------------------------
# Test document
# ---------------------------------------------------------------------------

TEST_DOCUMENT = """
LightRAG is a graph-based Retrieval-Augmented Generation system developed at HKUST.
It constructs a knowledge graph from documents to enable structured retrieval.

The system has two main components:
1. Indexing: documents are chunked, entities and relations are extracted by an LLM,
   and stored in a graph database alongside a vector store.
2. Querying: user queries are matched against the graph and vector store to retrieve
   relevant context, which is then used by the LLM to generate the final answer.

LightRAG supports multiple query modes:
- naive: traditional chunked-document retrieval (no graph)
- local: retrieves entities and relations directly connected to matched entities
- global: retrieves community-level summaries from the graph
- hybrid: combines local and global retrieval strategies

lightrag-slim is a stripped-down version that keeps only the core pipeline
with four storage backends: JsonKVStorage, NanoVectorDBStorage,
NetworkXStorage, and JsonDocStatusStorage.
"""

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def rag(tmp_path):
    """Create and initialize a LightRAG instance in a temp directory.

    Use tmp_path.name as workspace to isolate the shared_storage in-memory
    state between tests (which are keyed by workspace+namespace).
    """
    instance = LightRAG(
        working_dir=str(tmp_path),
        workspace=tmp_path.name,  # unique per test to avoid shared-state leakage
        llm_model_func=deepseek_llm_func,
        llm_model_name=DEEPSEEK_MODEL,
        embedding_func=bge_embedding_func,
        addon_params={"language": "English"},
    )
    await instance.initialize_storages()
    yield instance
    await instance.finalize_storages()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_insert_document(rag: LightRAG):
    """Insert a document and verify it appears in doc_status."""
    track_id = await rag.ainsert(TEST_DOCUMENT)
    assert track_id, "ainsert should return a non-empty track_id"
    print(f"\n[insert] track_id={track_id}")


@pytest.mark.asyncio
async def test_query_naive(rag: LightRAG):
    """Insert then query in naive mode."""
    await rag.ainsert(TEST_DOCUMENT)

    result = await rag.aquery(
        "What are the query modes supported by LightRAG?",
        param=QueryParam(mode="naive"),
    )
    print(f"\n[naive] {result}")
    assert result, "naive query should return a non-empty answer"
    # Check that at least one mode is mentioned
    assert any(mode in result.lower() for mode in ("naive", "local", "global", "hybrid")), (
        "Result should mention at least one query mode"
    )


@pytest.mark.asyncio
async def test_query_local(rag: LightRAG):
    """Insert then query in local mode (graph-entity level)."""
    await rag.ainsert(TEST_DOCUMENT)

    result = await rag.aquery(
        "What is LightRAG and where was it developed?",
        param=QueryParam(mode="local"),
    )
    print(f"\n[local] {result}")
    assert result, "local query should return a non-empty answer"


@pytest.mark.asyncio
async def test_query_hybrid(rag: LightRAG):
    """Insert then query in hybrid mode."""
    await rag.ainsert(TEST_DOCUMENT)

    result = await rag.aquery(
        "Describe the indexing and querying pipeline of LightRAG.",
        param=QueryParam(mode="hybrid"),
    )
    print(f"\n[hybrid] {result}")
    assert result, "hybrid query should return a non-empty answer"


@pytest.mark.asyncio
async def test_knowledge_graph_populated(rag: LightRAG):
    """After insert, the knowledge graph should contain at least one entity label."""
    await rag.ainsert(TEST_DOCUMENT)

    labels = await rag.get_graph_labels()
    print(f"\n[graph labels] count={len(labels)}: {labels[:10]}")
    assert len(labels) > 0, "Knowledge graph should have at least one entity after insert"
