"""RAG: chunking + TF-IDF retrieval over seed docs and uploaded documents (no external model required)."""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any

import numpy as np

from app.data.seed_docs import SEED_DOCS

_STOP = set("a an the and or of to in is are was were be it that this for on with as by at from how what why when which do does your you i can about into".split())
_WORD = re.compile(r"[a-z0-9]+")


def _stem(word: str) -> str:
    """Very light stemmer so 'quokkas'/'quokka' and 'queries'/'query' match."""
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 4 and word.endswith("es") and word[-3] in "sxz":
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def tokenize(text: str) -> list[str]:
    return [_stem(w) for w in _WORD.findall(text.lower()) if w not in _STOP and len(w) > 1]


def embed_text(text: str, dim: int = 384) -> np.ndarray:
    """Deterministic hashing embedding (384-dim, same size as all-MiniLM-L6-v2). Uses
    sentence-transformers automatically if it is installed and EMBEDDING_BACKEND=st."""
    import os
    if os.getenv("EMBEDDING_BACKEND") == "st":  # pragma: no cover - optional
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer(os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"))
            return np.asarray(model.encode(text), dtype=float)
        except Exception:
            pass
    vec = np.zeros(dim)
    for tok in tokenize(text):
        h = hash_token(tok)
        vec[h % dim] += 1.0 if (h >> 20) & 1 else -1.0
    n = np.linalg.norm(vec)
    return vec / n if n else vec


def hash_token(tok: str) -> int:
    h = 2166136261
    for ch in tok.encode():
        h = ((h ^ ch) * 16777619) & 0xFFFFFFFF
    return h


def chunk_text(text: str, max_chars: int = 600) -> list[str]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks, cur = [], ""
    for p in paras:
        if cur and len(cur) + len(p) > max_chars:
            chunks.append(cur)
            cur = p
        else:
            cur = f"{cur}\n\n{p}".strip()
    if cur:
        chunks.append(cur)
    out = []
    for c in chunks:  # split any oversized chunk on sentences
        while len(c) > max_chars * 1.5:
            cut = c.rfind(". ", 0, max_chars) + 1 or max_chars
            out.append(c[:cut].strip())
            c = c[cut:].strip()
        out.append(c)
    return [c for c in out if c]


class KnowledgeBase:
    def __init__(self) -> None:
        self.docs: dict[int, dict[str, Any]] = {}
        self._next_id = 1
        for title, text in SEED_DOCS.items():
            self.add_document(title, text, source="built-in", owner=None)

    def add_document(self, title: str, text: str, source: str = "", owner: int | None = None) -> dict[str, Any]:
        doc_id = self._next_id
        self._next_id += 1
        chunks = [{"text": c, "tokens": Counter(tokenize(c))} for c in chunk_text(text)]
        self.docs[doc_id] = {"id": doc_id, "title": title, "source": source or title, "owner": owner,
                             "status": "indexed", "chunks": chunks}
        return self.docs[doc_id]

    def delete_document(self, doc_id: int, owner: int | None) -> bool:
        doc = self.docs.get(doc_id)
        if not doc or doc["owner"] != owner:
            return False
        del self.docs[doc_id]
        return True

    def list_documents(self, owner: int) -> list[dict[str, Any]]:
        return [{"id": d["id"], "title": d["title"], "source": d["source"], "status": d["status"],
                 "chunk_count": len(d["chunks"])} for d in self.docs.values() if d["owner"] == owner]

    def retrieve(self, query: str, owner: int | None = None, top_k: int = 3) -> list[dict[str, Any]]:
        q = Counter(tokenize(query))
        if not q:
            return []
        visible = [d for d in self.docs.values() if d["owner"] in (None, owner)]
        n_chunks = sum(len(d["chunks"]) for d in visible) or 1
        df: Counter = Counter()
        for d in visible:
            for c in d["chunks"]:
                df.update(c["tokens"].keys())
        idf = {t: math.log((n_chunks + 1) / (df.get(t, 0) + 1)) + 1 for t in q}
        scored = []
        for d in visible:
            title_tokens = set(tokenize(d["title"]))
            for c in d["chunks"]:
                dot = sum(q[t] * idf[t] * c["tokens"].get(t, 0) * idf[t] for t in q)
                norm = math.sqrt(sum((v * idf.get(t, 1)) ** 2 for t, v in c["tokens"].items())) or 1.0
                score = dot / norm + 0.5 * len(title_tokens & set(q))
                if score > 0:
                    scored.append((score, d, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        if scored:  # drop weak matches relative to the best one
            scored = [x for x in scored if x[0] >= 0.5 * scored[0][0]]
        return [{"text": c["text"], "document_title": d["title"], "document_id": d["id"],
                 "relevance_score": round(float(s), 3)} for s, d, c in scored[:top_k]]


knowledge_base = KnowledgeBase()


def retrieve_chunks(query: str, owner: int | None = None, top_k: int = 3) -> list[dict[str, Any]]:
    return knowledge_base.retrieve(query, owner, top_k)
