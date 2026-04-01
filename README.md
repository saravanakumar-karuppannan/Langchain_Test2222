# ⬡ AgenticRAG — Multi-Source Agentic RAG System

A Streamlit-powered Agentic RAG (Retrieval-Augmented Generation) system that
intelligently routes your question through multiple knowledge sources.

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt
streamlit run agentic_rag_app.py
```

---

## 🔑 API Keys Required

| Key | Where to get it | Used for |
|-----|-----------------|----------|
| **OpenRouter** | [openrouter.ai](https://openrouter.ai) | LLM synthesis (required) |
| **Tavily** | [tavily.com](https://tavily.com) | Real-time web search (optional) |

Both keys are entered in the **sidebar** of the app — never stored anywhere.

---

## 🧠 Routing Pipeline

```
Query received
     │
     ▼
[1] Document uploaded?
     ├── YES → Keyword retrieval + LLM check
     │           ├── Sufficient? → ✅ Return answer (source: Document)
     │           └── Insufficient → continue ↓
     └── NO  → continue ↓
     │
     ▼
[2] Research / academic query?
     ├── YES → arXiv REST API → LLM synthesis → ✅ Return (source: arXiv)
     └── NO  → continue ↓
     │
     ▼
[3] Tavily key provided?
     ├── YES → Tavily web search → LLM synthesis → ✅ Return (source: Web)
     └── NO  → continue ↓
     │
     ▼
[4] Wikipedia lookup → LLM synthesis → ✅ Return (source: Wikipedia)
     │
     ▼ (fallback)
[5] LLM knowledge only → ✅ Return (source: LLM)
```

---

## 📄 Supported Document Formats

- **PDF** — full text extraction via `pdfplumber`
- **TXT / MD** — plain text
- **DOCX** — Word documents via `python-docx`

---

## 🤖 Supported Models (via OpenRouter)

- `mistralai/mistral-7b-instruct` *(default, fast & free)*
- `meta-llama/llama-3-8b-instruct`
- `google/gemma-3-27b-it:free`
- `deepseek/deepseek-r1:free`
- `openai/gpt-4o-mini`

Any model available on OpenRouter can be added to the selectbox.

---

## 📁 File Structure

```
agentic_rag_app.py   ← Main Streamlit app (single file)
requirements.txt     ← Python dependencies
README.md            ← This file
```

---

## ✨ Features

- **Zero vector DB** — lightweight keyword-overlap retrieval, no Chroma/FAISS needed
- **Transparent routing** — every agent step is shown live in the UI
- **Source attribution** — every answer links back to its origin
- **Latency metrics** — see how long each query took
- **Dark editorial UI** — clean, professional interface
