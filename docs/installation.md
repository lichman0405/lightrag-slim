# Installation

## Requirements

- **Python** ≥ 3.10
- A POSIX system (Linux / macOS) or Windows with WSL2

---

## Install from PyPI

```bash
pip install lightrag-slim
```

---

## Install from Source

```bash
git clone https://github.com/lichman0405/lightrag-slim.git
cd lightrag-slim
pip install -e .
```

---

## Verify the Installation

```bash
python -c "from lightrag_slim import LightRAG, QueryParam; print('lightrag-slim OK ✓')"
```

You should see:

```
lightrag-slim OK ✓
```

!!! note "pypinyin warning"
    If you see a warning about `pypinyin` not being installed, that is expected and harmless.
    It only affects Chinese-character sorting in entity names. Install it optionally:
    ```bash
    pip install pypinyin
    ```

---

## Optional Dependencies

`lightrag-slim` has no opinion about which LLM or embedding model you use.
Install the SDK that matches your choice:

=== "DeepSeek / OpenAI"

    ```bash
    pip install openai
    ```

    Works with any OpenAI-compatible API endpoint (DeepSeek, Together AI, local vLLM, etc.)

=== "Local embedding (BAAI/bge-m3)"

    ```bash
    pip install sentence-transformers
    ```

    Downloads and runs the `BAAI/bge-m3` model locally (1 GB, CPU-compatible).
    No API key needed.

=== "OpenAI Embeddings"

    ```bash
    pip install openai
    ```

    Use `text-embedding-3-small` or `text-embedding-3-large` via the OpenAI API.

=== "Anthropic"

    ```bash
    pip install anthropic
    ```

    Use Claude models for the LLM function.

---

## Core Dependencies

These are installed automatically with `lightrag-slim`:

| Package | Purpose |
|---|---|
| `json-repair` | Repair malformed JSON returned by LLMs |
| `nano-vectordb` | Lightweight file-based vector store |
| `networkx` | In-memory knowledge graph |
| `numpy` | Vector operations |
| `pydantic` | Data validation |
| `python-dotenv` | Load `.env` configuration |
| `tiktoken` | Token counting for chunking |
