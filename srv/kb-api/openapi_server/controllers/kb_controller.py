"""
KB API Controller — FAISS semantic search + file retrieval.
Falls back to mock data if index not found.
"""
import os
import json
import time
import glob
import hashlib
from pathlib import Path
from flask import request, abort

KB_ROOT = Path(os.getenv("KB_ROOT", "data/knowledge_base"))
KB_TOKEN = os.getenv("KB_TOKEN", "")
_faiss_index = None
_faiss_meta = None


def _check_auth():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer ") or auth[7:] != KB_TOKEN:
        abort(401, "Invalid or missing KB_TOKEN")


def _load_index():
    global _faiss_index, _faiss_meta
    if _faiss_index is not None:
        return True
    try:
        import faiss
        import pickle
        idx_path = KB_ROOT / "index" / "kb.faiss"
        meta_path = KB_ROOT / "index" / "kb_meta.pkl"
        if idx_path.exists() and meta_path.exists():
            _faiss_index = faiss.read_index(str(idx_path))
            with open(meta_path, "rb") as f:
                _faiss_meta = pickle.load(f)
            return True
    except Exception:
        pass
    return False


def _mock_search(q: str, type_filter: str, limit: int):
    """Fallback: simple keyword search over file contents."""
    results = []
    patterns = {
        "company": str(KB_ROOT / "companies" / "*.json"),
        "persona": str(KB_ROOT / "personas" / "*.md"),
        "playbook": str(KB_ROOT / "playbooks" / "*.md"),
    }
    search_patterns = [patterns[type_filter]] if type_filter != "all" else list(patterns.values())
    q_lower = q.lower()
    for pattern in search_patterns:
        for path in glob.glob(pattern):
            try:
                content = Path(path).read_text(encoding="utf-8")
            except Exception:
                continue
            if q_lower in content.lower():
                slug = Path(path).stem
                doc_type = "company" if "/companies/" in path else ("persona" if "/personas/" in path else "playbook")
                snippet = next((line.strip() for line in content.splitlines() if q_lower in line.lower()), content[:120])
                results.append({
                    "id": slug,
                    "slug": slug,
                    "type": doc_type,
                    "score": round(0.70 + len(q) / 200, 4),
                    "snippet": snippet[:200],
                    "source": str(Path(path).relative_to(Path.cwd())),
                })
    return sorted(results, key=lambda r: -r["score"])[:limit]


def kb_search(q=None, type="all", limit=5, min_score=0.65, next_token=None):
    if KB_TOKEN:
        _check_auth()
    t0 = time.time()
    results = []
    if _load_index():
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            vec = model.encode([q])
            import numpy as np
            D, I = _faiss_index.search(np.array(vec, dtype="float32"), limit * 2)
            for dist, idx in zip(D[0], I[0]):
                if idx < 0 or idx >= len(_faiss_meta):
                    continue
                meta = _faiss_meta[idx]
                score = float(1 - dist / 2)
                if score < min_score:
                    continue
                if type != "all" and meta.get("type") != type:
                    continue
                results.append({
                    "id": meta["slug"],
                    "slug": meta["slug"],
                    "type": meta["type"],
                    "score": round(score, 4),
                    "snippet": meta.get("snippet", "")[:200],
                    "source": meta.get("source", ""),
                })
                if len(results) >= limit:
                    break
        except Exception as e:
            results = _mock_search(q, type, limit)
    else:
        results = _mock_search(q, type, limit)

    query_ms = round((time.time() - t0) * 1000, 2)
    return {
        "results": results,
        "total": len(results),
        "next_token": None,
        "query_time_ms": query_ms,
    }, 200


def kb_get_company(slug):
    if KB_TOKEN:
        _check_auth()
    path = KB_ROOT / "companies" / f"{slug}.json"
    if not path.exists():
        abort(404, f"Company '{slug}' not found")
    content = path.read_text(encoding="utf-8")
    return {
        "id": slug,
        "slug": slug,
        "type": "company",
        "score": 1.0,
        "snippet": content[:200],
        "source": str(path.relative_to(Path.cwd())),
    }, 200


def kb_get_persona(slug):
    if KB_TOKEN:
        _check_auth()
    path = KB_ROOT / "personas" / f"{slug}.md"
    if not path.exists():
        abort(404, f"Persona '{slug}' not found")
    content = path.read_text(encoding="utf-8")
    return {
        "id": slug,
        "slug": slug,
        "type": "persona",
        "score": 1.0,
        "snippet": content[:200],
        "source": str(path.relative_to(Path.cwd())),
    }, 200


def kb_health():
    index_loaded = _load_index()
    total = _faiss_index.ntotal if index_loaded and _faiss_index else 0
    return {"status": "ok", "index_loaded": index_loaded, "total_vectors": total}, 200
