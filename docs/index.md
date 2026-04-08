---
hide:
  - navigation
  - toc
---

# lightrag-slim

**A lightweight, standalone graph-based RAG engine** — extracted from [LightRAG](https://github.com/HKUDS/LightRAG).

Pure Python · zero server dependencies · bring your own LLM.

[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue?style=flat-square&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](https://github.com/lichman0405/lightrag-slim/blob/main/LICENSE)
[![Based on LightRAG](https://img.shields.io/badge/based%20on-LightRAG-blueviolet?style=flat-square)](https://github.com/HKUDS/LightRAG)

[Get Started](installation.md){ .md-button .md-button--primary }
[Quick Start](quickstart.md){ .md-button }
[GitHub :fontawesome-brands-github:](https://github.com/lichman0405/lightrag-slim){ .md-button }

---

## Features

<div class="grid cards" markdown>

-   :material-graph-outline:{ .lg .middle } **Graph-Based Retrieval**

    ---

    Builds a knowledge graph from documents to answer complex multi-hop questions that simple vector search misses.

-   :material-lightning-bolt:{ .lg .middle } **8 Dependencies**

    ---

    Reduced from 18+ in full LightRAG. No database server, no vendor SDK required.

-   :material-power-plug-outline:{ .lg .middle } **Bring Your Own LLM**

    ---

    Plug in any LLM or embedding model — OpenAI, DeepSeek, Anthropic, local Ollama, or anything else.

-   :material-folder-outline:{ .lg .middle } **File-Based Storage**

    ---

    All data stored as plain files — NetworkX graph, NanoVectorDB, JSON. No infrastructure needed.

-   :material-magnify:{ .lg .middle } **4 Query Modes**

    ---

    `naive` / `local` / `global` / `hybrid` — from simple vector search to full graph traversal.

-   :material-language-python:{ .lg .middle } **Pure Async Python**

    ---

    Built entirely on `asyncio`. Drop into any Python application or agent framework.

</div>

---

## Acknowledgements

!!! quote "Built on the shoulders of giants"

    `lightrag-slim` is a derivative of [**LightRAG**](https://github.com/HKUDS/LightRAG) — a brilliant graph-based RAG
    framework developed by researchers at The Hong Kong University of Science and Technology.
    The core retrieval algorithm, entity/relation extraction pipeline, multi-mode query system,
    and cross-process shared storage design all originate from their exceptional work.

    If this library is useful to you, please **[⭐ star the original LightRAG repository](https://github.com/HKUDS/LightRAG)** and consider citing their paper.

| Resource | Link |
|---|---|
| :fontawesome-brands-github: Original GitHub | [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) |
| :fontawesome-solid-file-pdf: Research Paper | [arXiv:2410.05779](https://arxiv.org/abs/2410.05779) |
| :fontawesome-solid-users: Authors | Zirui Guo, Lianghao Xia, Yanhua Yu, Tu Ao, Chao Huang |

??? note "BibTeX Citation"
    ```bibtex
    @article{guo2024lightrag,
      title={LightRAG: Simple and Fast Retrieval-Augmented Generation},
      author={Guo, Zirui and Xia, Lianghao and Yu, Yanhua and Ao, Tu and Huang, Chao},
      journal={arXiv preprint arXiv:2410.05779},
      year={2024}
    }
    ```

---

## What's Removed vs LightRAG

| Component | LightRAG | lightrag-slim |
|---|:---:|:---:|
| Core RAG pipeline | ✅ | ✅ |
| 4 query modes (naive/local/global/hybrid) | ✅ | ✅ |
| File-based storage (4 backends) | ✅ | ✅ |
| REST API server (FastAPI) | ✅ | ❌ |
| Web UI (React 19) | ✅ | ❌ |
| 13+ extra storage backends | ✅ | ❌ |
| 12+ LLM provider bindings | ✅ | ❌ |
| Evaluation framework | ✅ | ❌ |
