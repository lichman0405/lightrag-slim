---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

# lightrag-slim

<div class="hero-subtitle">
A lightweight, standalone graph-based RAG engine.<br>
Extracted from the outstanding <strong>LightRAG</strong> — pure Python, zero server dependencies, bring your own LLM.
</div>

<div class="hero-badges">
  <img src="https://img.shields.io/badge/python-%3E%3D3.10-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/dependencies-8-informational?style=flat-square" alt="Dependencies">
  <img src="https://img.shields.io/badge/based%20on-LightRAG-blueviolet?style=flat-square" alt="Based on LightRAG">
</div>

<div class="hero-buttons">
  <a class="btn btn-primary" href="installation/">Get Started</a>
  <a class="btn btn-outline" href="quickstart/">Quick Start</a>
  <a class="btn btn-outline" href="https://github.com/lichman0405/lightrag-slim" target="_blank">GitHub</a>
</div>

</div>

---

## Features

<div class="feature-grid" markdown>

<div class="feature-card" markdown>
<div class="icon">🕸️</div>
### Graph-Based Retrieval
Builds a knowledge graph from documents to answer complex multi-hop questions that simple vector search misses.
</div>

<div class="feature-card" markdown>
<div class="icon">⚡</div>
### 8 Dependencies Only
Reduced from 18+ in the full LightRAG. No database server, no vendor SDK required.
</div>

<div class="feature-card" markdown>
<div class="icon">🔌</div>
### Bring Your Own LLM
Plug in any LLM or embedding model — OpenAI, DeepSeek, Anthropic, local Ollama, or anything else.
</div>

<div class="feature-card" markdown>
<div class="icon">📁</div>
### File-Based Storage
All data stored as plain files (NetworkX graph + NanoVectorDB + JSON). No infrastructure needed.
</div>

<div class="feature-card" markdown>
<div class="icon">🔍</div>
### 4 Query Modes
`naive` / `local` / `global` / `hybrid` — from simple vector search to full graph traversal.
</div>

<div class="feature-card" markdown>
<div class="icon">🐍</div>
### Pure Async Python
Built entirely on `asyncio`. Drop into any async Python application or agent framework.
</div>

</div>

---

## Acknowledgements

<div class="ack-box" markdown>

**This project is built on the shoulders of giants.**

`lightrag-slim` is a derivative of [**LightRAG**](https://github.com/HKUDS/LightRAG) — a brilliant graph-based RAG framework developed by researchers at The Hong Kong University of Science and Technology. The core retrieval algorithm, entity/relation extraction pipeline, multi-mode query system, and cross-process shared storage design all originate from their exceptional work.

If this library is useful to you, please **[⭐ star and fork the original LightRAG repository](https://github.com/HKUDS/LightRAG)** and consider citing their paper.

</div>

| Resource | Link |
|---|---|
| 📦 Original GitHub | [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) |
| 📄 Research Paper (arXiv) | [LightRAG: Simple and Fast Retrieval-Augmented Generation](https://arxiv.org/abs/2410.05779) |
| 👥 Authors | Zirui Guo, Lianghao Xia, Yanhua Yu, Tu Ao, Chao Huang |

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
