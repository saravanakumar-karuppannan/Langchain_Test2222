import streamlit as st
import os
import time
import requests
import json
import re
from typing import Optional
import tempfile

# ─────────────────────────────────────────────
# Page configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Agentic RAG System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS – dark editorial aesthetic
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;700;800&display=swap');

    /* Global */
    html, body, [class*="css"] {
        font-family: 'Syne', sans-serif;
        background-color: #f5f7ff;
        color: #1a1a2e;
    }
    .stApp { background-color: #f5f7ff; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #eef1ff 100%);
        border-right: 1px solid #dde2f5;
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #4f46e5;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown p {
        color: #374151 !important;
    }

    /* Title / brand */
    .brand-header {
        text-align: center;
        padding: 2rem 0 1rem;
    }
    .brand-header .logo-text {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 2.6rem;
        letter-spacing: -1px;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #0ea5e9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .brand-header .tagline {
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        color: #9ca3af;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 0.3rem;
    }

    /* Cards */
    .card {
        background: #ffffff;
        border: 1px solid #e5e9f7;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 6px rgba(79,70,229,0.06);
    }
    .card-accent {
        border-left: 3px solid #4f46e5;
    }

    /* Source badge */
    .source-badge {
        display: inline-block;
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 3px 10px;
        border-radius: 4px;
        font-weight: 700;
        margin-right: 6px;
    }
    .badge-doc    { background: #ecfdf5; color: #059669; border: 1px solid #6ee7b7; }
    .badge-web    { background: #eff6ff; color: #2563eb; border: 1px solid #93c5fd; }
    .badge-arxiv  { background: #fff7ed; color: #ea580c; border: 1px solid #fdba74; }
    .badge-wiki   { background: #ecfeff; color: #0891b2; border: 1px solid #67e8f9; }
    .badge-llm    { background: #faf5ff; color: #7c3aed; border: 1px solid #c4b5fd; }

    /* Answer box */
    .answer-box {
        background: #ffffff;
        border: 1px solid #e5e9f7;
        border-radius: 12px;
        padding: 1.6rem 2rem;
        line-height: 1.8;
        font-size: 0.97rem;
        color: #1f2937;
        box-shadow: 0 2px 12px rgba(79,70,229,0.07);
    }

    /* Step trace */
    .step-trace {
        font-family: 'Space Mono', monospace;
        font-size: 0.72rem;
        color: #9ca3af;
        border-left: 2px solid #e5e9f7;
        padding-left: 12px;
        margin: 6px 0;
    }
    .step-active { color: #4f46e5; border-color: #4f46e5; }

    /* Input styling */
    .stTextArea textarea, .stTextInput input {
        background: #ffffff !important;
        border: 1px solid #dde2f5 !important;
        border-radius: 8px !important;
        color: #1a1a2e !important;
        font-family: 'Syne', sans-serif !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 3px rgba(79,70,229,0.12) !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        padding: 0.55rem 1.8rem !important;
        transition: opacity 0.2s, box-shadow 0.2s !important;
        box-shadow: 0 2px 8px rgba(79,70,229,0.25) !important;
    }
    .stButton > button:hover {
        opacity: 0.88 !important;
        box-shadow: 0 4px 16px rgba(79,70,229,0.35) !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        border: 1px dashed #c7d0f0;
        border-radius: 10px;
        padding: 0.5rem;
        background: #fafbff;
    }

    /* Divider */
    hr { border-color: #e5e9f7 !important; }

    /* Metric */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e5e9f7;
        border-radius: 10px;
        padding: 0.8rem;
        box-shadow: 0 1px 4px rgba(79,70,229,0.06);
    }
    [data-testid="stMetricLabel"] { color: #6b7280 !important; }
    [data-testid="stMetricValue"] { color: #1a1a2e !important; }

    /* Labels & general text */
    .stSelectbox label, .stFileUploader label,
    .stTextArea label, .stTextInput label {
        color: #374151 !important;
        font-weight: 600 !important;
    }
    p, span, li { color: #1f2937; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# Helpers – document parsing
# ─────────────────────────────────────────────

def extract_text_from_file(uploaded_file) -> str:
    """Extract plain text from uploaded PDF, TXT, or DOCX."""
    fname = uploaded_file.name.lower()
    raw = uploaded_file.read()

    if fname.endswith(".txt") or fname.endswith(".md"):
        return raw.decode("utf-8", errors="ignore")

    if fname.endswith(".pdf"):
        try:
            import pdfplumber
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(raw)
                tmp_path = tmp.name
            text_parts = []
            with pdfplumber.open(tmp_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text_parts.append(t)
            os.unlink(tmp_path)
            return "\n".join(text_parts)
        except ImportError:
            return raw.decode("utf-8", errors="ignore")

    if fname.endswith(".docx"):
        try:
            import docx
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
                tmp.write(raw)
                tmp_path = tmp.name
            doc = docx.Document(tmp_path)
            os.unlink(tmp_path)
            return "\n".join([p.text for p in doc.paragraphs])
        except ImportError:
            return raw.decode("utf-8", errors="ignore")

    return raw.decode("utf-8", errors="ignore")


def chunk_text(text: str, chunk_size: int = 1500, overlap: int = 200) -> list[str]:
    chunks, start = [], 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def simple_relevance(query: str, chunk: str) -> float:
    """Keyword-overlap relevance score (no external deps)."""
    q_words = set(re.findall(r'\w+', query.lower()))
    c_words = set(re.findall(r'\w+', chunk.lower()))
    if not q_words:
        return 0.0
    return len(q_words & c_words) / len(q_words)


def retrieve_from_doc(query: str, doc_text: str, top_k: int = 3) -> list[str]:
    chunks = chunk_text(doc_text)
    scored = [(simple_relevance(query, c), c) for c in chunks]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for score, c in scored[:top_k] if score > 0.05]


# ─────────────────────────────────────────────
# Helpers – external sources
# ─────────────────────────────────────────────

def search_tavily(query: str, api_key: str) -> Optional[dict]:
    """Tavily web search."""
    try:
        resp = requests.post(
            "https://api.tavily.com/search",
            json={"api_key": api_key, "query": query, "max_results": 5},
            timeout=20,
        )
        return resp.json() if resp.status_code == 200 else None
    except Exception:
        return None


def search_arxiv(query: str) -> Optional[list[dict]]:
    """arXiv REST API – no key needed."""
    try:
        import xml.etree.ElementTree as ET
        url = "https://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": 4,
            "sortBy": "relevance",
        }
        resp = requests.get(url, params=params, timeout=20)
        if resp.status_code != 200:
            return None
        root = ET.fromstring(resp.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        results = []
        for entry in root.findall("atom:entry", ns):
            title   = entry.find("atom:title", ns)
            summary = entry.find("atom:summary", ns)
            link    = entry.find("atom:id", ns)
            results.append({
                "title":   title.text.strip()   if title   is not None else "",
                "summary": summary.text.strip() if summary is not None else "",
                "url":     link.text.strip()    if link    is not None else "",
            })
        return results if results else None
    except Exception:
        return None


def search_wikipedia(query: str) -> Optional[dict]:
    """Wikipedia REST API."""
    try:
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 3,
        }
        resp = requests.get(search_url, params=params, timeout=15)
        if resp.status_code != 200:
            return None
        data = resp.json()
        results = data.get("query", {}).get("search", [])
        if not results:
            return None
        # fetch extract for top result
        page_title = results[0]["title"]
        extract_params = {
            "action": "query",
            "titles": page_title,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "format": "json",
        }
        er = requests.get(search_url, params=extract_params, timeout=15)
        pages = er.json().get("query", {}).get("pages", {})
        page  = next(iter(pages.values()))
        return {
            "title":   page.get("title", page_title),
            "extract": page.get("extract", ""),
            "url":     f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}",
        }
    except Exception:
        return None


# ─────────────────────────────────────────────
# LLM via OpenRouter
# ─────────────────────────────────────────────

def call_openrouter(
    system_prompt: str,
    user_prompt: str,
    api_key: str,
    model: str = "mistralai/mistral-7b-instruct",
) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type":  "application/json",
        "HTTP-Referer":  "https://agentic-rag.streamlit.app",
    }

    # Gemma models (Google AI Studio) do NOT support the "system" role.
    # Merge system prompt into the user turn instead.
    NO_SYSTEM_ROLE_MODELS = ("gemma",)
    if any(kw in model.lower() for kw in NO_SYSTEM_ROLE_MODELS):
        messages = [
            {
                "role": "user",
                "content": f"{system_prompt}\n\n{user_prompt}",
            }
        ]
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]

    body = {
        "model": model,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.3,
    }
    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=body,
        timeout=60,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"OpenRouter error {resp.status_code}: {resp.text[:300]}")
    return resp.json()["choices"][0]["message"]["content"]


def is_research_query(query: str) -> bool:
    research_kw = [
        "paper", "study", "research", "arxiv", "journal", "experiment",
        "algorithm", "neural", "model", "dataset", "benchmark", "survey",
        "novel", "propose", "method", "framework", "transformer", "llm",
        "deep learning", "machine learning", "ai ", "artificial intelligence",
    ]
    q_lower = query.lower()
    return any(kw in q_lower for kw in research_kw)


# ─────────────────────────────────────────────
# Core agentic pipeline
# ─────────────────────────────────────────────

def agentic_rag(
    query: str,
    doc_text: Optional[str],
    openrouter_key: str,
    tavily_key: str,
    model: str,
    status_container,
) -> dict:
    """
    Returns {answer, source_type, sources, steps}
    """
    steps   = []
    sources = []

    def log(msg: str, active: bool = False):
        steps.append({"msg": msg, "active": active})
        cls = "step-trace step-active" if active else "step-trace"
        status_container.markdown(f'<div class="{cls}">▸ {msg}</div>', unsafe_allow_html=True)

    # ── STEP 1 – Document check ──────────────────────
    doc_chunks = []
    if doc_text and len(doc_text.strip()) > 50:
        log("📄 Document detected — retrieving relevant passages …", active=True)
        doc_chunks = retrieve_from_doc(query, doc_text)
        if doc_chunks:
            log(f"   Found {len(doc_chunks)} relevant chunk(s) in the document.")
        else:
            log("   No relevant passages found in document.")
    else:
        log("📂 No document uploaded — skipping document retrieval.")

    # ── STEP 2 – Decide if doc is sufficient ────────
    if doc_chunks:
        context_for_llm = "\n\n---\n\n".join(doc_chunks)
        sys_p = (
            "You are a precise RAG assistant. Use ONLY the provided document context to answer."
            " If the context clearly answers the question, respond with a complete answer."
            " If the context does NOT contain enough information, reply with exactly: INSUFFICIENT"
        )
        user_p = f"Document context:\n{context_for_llm}\n\nQuestion: {query}"
        log("🤖 Asking LLM if document context is sufficient …", active=True)
        try:
            doc_answer = call_openrouter(sys_p, user_p, openrouter_key, model)
        except Exception as e:
            doc_answer = "INSUFFICIENT"
            log(f"   LLM error: {e}")

        if "INSUFFICIENT" not in doc_answer.upper():
            log("✅ Answer found in document!", active=True)
            return {
                "answer":      doc_answer,
                "source_type": "document",
                "sources":     [{"label": "Uploaded Document", "url": None}],
                "steps":       steps,
            }
        else:
            log("   Document context insufficient — escalating to external search …")

    # ── STEP 3 – Route to correct external source ───
    if is_research_query(query):
        log("🔬 Research query detected — searching arXiv …", active=True)
        arxiv_results = search_arxiv(query)
        if arxiv_results:
            context_parts = []
            for r in arxiv_results:
                context_parts.append(f"Title: {r['title']}\nAbstract: {r['summary']}")
                sources.append({"label": r["title"], "url": r["url"]})
            context_for_llm = "\n\n---\n\n".join(context_parts)
            sys_p = (
                "You are an expert scientific assistant. Synthesise the arXiv abstracts below "
                "to give a comprehensive, well-structured answer to the question."
            )
            user_p = f"arXiv results:\n{context_for_llm}\n\nQuestion: {query}"
            log("🤖 Synthesising arXiv results with LLM …", active=True)
            answer = call_openrouter(sys_p, user_p, openrouter_key, model)
            return {"answer": answer, "source_type": "arxiv", "sources": sources, "steps": steps}

        log("   No arXiv results — falling back to web search …")

    # ── STEP 4 – Tavily web search ───────────────────
    if tavily_key:
        log("🌐 Searching the web via Tavily …", active=True)
        tavily_data = search_tavily(query, tavily_key)
        if tavily_data and tavily_data.get("results"):
            context_parts = []
            for r in tavily_data["results"][:4]:
                snippet = r.get("content", r.get("snippet", ""))
                context_parts.append(f"Source: {r.get('url','')}\n{snippet}")
                sources.append({"label": r.get("title", r.get("url", "Web")), "url": r.get("url")})
            context_for_llm = "\n\n---\n\n".join(context_parts)
            sys_p = (
                "You are a helpful assistant. Use the web search results below to answer accurately. "
                "Be concise and cite which source supports each point where possible."
            )
            user_p = f"Web search results:\n{context_for_llm}\n\nQuestion: {query}"
            log("🤖 Synthesising web results with LLM …", active=True)
            answer = call_openrouter(sys_p, user_p, openrouter_key, model)
            return {"answer": answer, "source_type": "web", "sources": sources, "steps": steps}

    # ── STEP 5 – Wikipedia fallback ──────────────────
    log("📖 Searching Wikipedia …", active=True)
    wiki = search_wikipedia(query)
    if wiki and wiki.get("extract"):
        extract = wiki["extract"][:3000]
        sources.append({"label": wiki["title"], "url": wiki["url"]})
        sys_p = (
            "You are a knowledgeable assistant. Use the Wikipedia extract below to answer the question clearly."
        )
        user_p = f"Wikipedia – {wiki['title']}:\n{extract}\n\nQuestion: {query}"
        log("🤖 Synthesising Wikipedia content with LLM …", active=True)
        answer = call_openrouter(sys_p, user_p, openrouter_key, model)
        return {"answer": answer, "source_type": "wikipedia", "sources": sources, "steps": steps}

    # ── STEP 6 – Pure LLM fallback ──────────────────
    log("🧠 No external sources found — using LLM knowledge …", active=True)
    sys_p = "You are a knowledgeable assistant. Answer the question as accurately as possible from your training knowledge."
    answer = call_openrouter(sys_p, query, openrouter_key, model)
    return {
        "answer":      answer,
        "source_type": "llm",
        "sources":     [{"label": "LLM Knowledge (OpenRouter)", "url": None}],
        "steps":       steps,
    }


# ─────────────────────────────────────────────
# UI Layout
# ─────────────────────────────────────────────

# Brand header
st.markdown(
    """
    <div class="brand-header">
        <div class="logo-text">⬡ AgenticRAG</div>
        <div class="tagline">Multi-source · Adaptive · Intelligent retrieval</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ──────────────────────────────────
with st.sidebar:
    st.markdown("### 🔑 API Keys")
    openrouter_key = st.text_input(
        "OpenRouter API Key",
        type="password",
        placeholder="sk-or-v1-…",
        help="Get yours at openrouter.ai",
    )
    tavily_key = st.text_input(
        "Tavily Search API Key",
        type="password",
        placeholder="tvly-…",
        help="Get yours at tavily.com",
    )

    st.markdown("---")
    st.markdown("### 🤖 Model")
    model_choice = st.selectbox(
        "OpenRouter model",
        [
            "mistralai/mistral-7b-instruct",
            "meta-llama/llama-3-8b-instruct",
            "google/gemma-3-27b-it:free",
            "deepseek/deepseek-r1:free",
            "openai/gpt-4o-mini",
        ],
        index=0,
    )

    st.markdown("---")
    st.markdown("### 📄 Upload Document")
    uploaded_file = st.file_uploader(
        "PDF / TXT / DOCX",
        type=["pdf", "txt", "md", "docx"],
        help="The system will search this first before going online.",
    )
    if uploaded_file:
        st.success(f"✓ {uploaded_file.name}")

    st.markdown("---")
    st.markdown(
        """
        <div style='font-family:Space Mono,monospace;font-size:0.62rem;color:#9ca3af;line-height:1.8'>
        PIPELINE<br>
        1 → Document (if uploaded)<br>
        2 → arXiv (research Qs)<br>
        3 → Tavily web search<br>
        4 → Wikipedia<br>
        5 → LLM knowledge
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Main panel ───────────────────────────────
col_main, col_right = st.columns([2.5, 1])

with col_main:
    query = st.text_area(
        "Ask anything",
        placeholder="e.g.  What are the key findings of the uploaded report?",
        height=110,
        label_visibility="collapsed",
    )
    run_btn = st.button("⟶ Run Query", use_container_width=False)

with col_right:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card" style="margin-top:0.2rem">
        <span style="font-family:Space Mono,monospace;font-size:0.68rem;color:#9ca3af;letter-spacing:2px">ROUTING LOGIC</span><br><br>
        <span style="font-size:0.82rem;color:#059669">📄 Doc</span> → keyword overlap + LLM check<br>
        <span style="font-size:0.82rem;color:#ea580c">🔬 arXiv</span> → research keyword match<br>
        <span style="font-size:0.82rem;color:#2563eb">🌐 Web</span> → Tavily real-time search<br>
        <span style="font-size:0.82rem;color:#0891b2">📖 Wiki</span> → encyclopedic fallback<br>
        <span style="font-size:0.82rem;color:#7c3aed">🧠 LLM</span> → model knowledge last
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Execution ────────────────────────────────
if run_btn:
    if not query.strip():
        st.warning("Please enter a question.")
        st.stop()
    if not openrouter_key:
        st.error("OpenRouter API key is required.")
        st.stop()

    doc_text = None
    if uploaded_file:
        uploaded_file.seek(0)
        with st.spinner("Parsing document …"):
            doc_text = extract_text_from_file(uploaded_file)

    st.markdown("---")
    st.markdown(
        '<span style="font-family:Space Mono,monospace;font-size:0.7rem;letter-spacing:2px;color:#9ca3af">AGENT TRACE</span>',
        unsafe_allow_html=True,
    )
    status_box = st.container()

    try:
        t0 = time.time()
        result = agentic_rag(query, doc_text, openrouter_key, tavily_key, model_choice, status_box)
        elapsed = time.time() - t0
    except Exception as e:
        st.error(f"Pipeline error: {e}")
        st.stop()

    # ── Source badge ─────────────────────────
    badge_map = {
        "document":  ("📄 DOCUMENT",  "badge-doc"),
        "arxiv":     ("🔬 ARXIV",     "badge-arxiv"),
        "web":       ("🌐 WEB",       "badge-web"),
        "wikipedia": ("📖 WIKIPEDIA", "badge-wiki"),
        "llm":       ("🧠 LLM",       "badge-llm"),
    }
    label, badge_cls = badge_map.get(result["source_type"], ("SOURCE", "badge-llm"))

    st.markdown("---")
    st.markdown(
        f'<span class="source-badge {badge_cls}">{label}</span>'
        f'<span style="font-family:Space Mono,monospace;font-size:0.65rem;color:#3a3a5a"> {elapsed:.1f}s</span>',
        unsafe_allow_html=True,
    )

    # ── Answer ───────────────────────────────
    answer_html = result["answer"].replace("\n", "<br>")
    st.markdown(
        f'<div class="answer-box">{answer_html}</div>',
        unsafe_allow_html=True,
    )

    # ── Sources list ─────────────────────────
    if result["sources"]:
        st.markdown(
            '<br><span style="font-family:Space Mono,monospace;font-size:0.68rem;letter-spacing:2px;color:#9ca3af">SOURCES</span>',
            unsafe_allow_html=True,
        )
        for src in result["sources"]:
            if src.get("url"):
                st.markdown(
                    f'<div class="card card-accent" style="padding:0.7rem 1rem;margin:0.4rem 0">'
                    f'<a href="{src["url"]}" target="_blank" style="color:#2563eb;text-decoration:none;font-size:0.85rem">'
                    f'↗ {src["label"]}</a></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="card card-accent" style="padding:0.7rem 1rem;margin:0.4rem 0">'
                    f'<span style="color:#4f46e5;font-size:0.85rem">{src["label"]}</span></div>',
                    unsafe_allow_html=True,
                )

    # ── Metrics ──────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("⏱ Latency",   f"{elapsed:.1f}s")
    m2.metric("🔗 Sources",  len(result["sources"]))
    m3.metric("📍 Route",    label.split(" ", 1)[-1])
