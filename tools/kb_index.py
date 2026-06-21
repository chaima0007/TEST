#!/usr/bin/env python3
"""
Caelum KB Index Builder & Searcher (FAISS + sentence-transformers)
Usage:
  python3 tools/kb_index.py build    -- build index from data/knowledge_base/
  python3 tools/kb_index.py search "CCO automobile LkSG"
Index stored at: data/knowledge_base/index/kb.faiss + kb_meta.pkl
"""
import sys
import json
import os
import pickle
from pathlib import Path

KB_ROOT = Path("data/knowledge_base")
INDEX_DIR = KB_ROOT / "index"


def build_index():
    try:
        import faiss
        import numpy as np
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("Install: pip install faiss-cpu sentence-transformers")
        sys.exit(1)

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    docs = []
    meta = []

    for pattern, doc_type in [("companies/*.json", "company"), ("personas/*.md", "persona"), ("playbooks/*.md", "playbook")]:
        for path in sorted(KB_ROOT.glob(pattern)):
            content = path.read_text(encoding="utf-8")
            slug = path.stem
            snippet = content[:300].replace("\n", " ")
            docs.append(content)
            meta.append({"slug": slug, "type": doc_type, "source": str(path), "snippet": snippet})

    if not docs:
        print("No documents found. Check KB_ROOT path.")
        sys.exit(1)

    print(f"Encoding {len(docs)} documents...")
    embeddings = model.encode(docs, show_progress_bar=True, convert_to_numpy=True)
    embeddings = embeddings / (embeddings ** 2).sum(axis=1, keepdims=True) ** 0.5  # normalize

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_DIR / "kb.faiss"))
    with open(INDEX_DIR / "kb_meta.pkl", "wb") as f:
        pickle.dump(meta, f)
    print(f"Index built: {len(docs)} vectors → {INDEX_DIR}/kb.faiss")


def search_index(query: str, top_k: int = 5):
    try:
        import faiss
        import numpy as np
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("Install: pip install faiss-cpu sentence-transformers")
        sys.exit(1)

    idx_path = INDEX_DIR / "kb.faiss"
    meta_path = INDEX_DIR / "kb_meta.pkl"
    if not idx_path.exists():
        print("Index not found. Run: python3 tools/kb_index.py build")
        sys.exit(1)

    index = faiss.read_index(str(idx_path))
    with open(meta_path, "rb") as f:
        meta = pickle.load(f)

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    vec = model.encode([query], convert_to_numpy=True)
    vec = vec / (vec ** 2).sum(axis=1, keepdims=True) ** 0.5

    D, I = index.search(vec, top_k)
    print(f"\nResults for: '{query}'\n{'='*50}")
    for score, idx in zip(D[0], I[0]):
        if idx < 0:
            continue
        m = meta[idx]
        print(f"[{score:.3f}] {m['type']:8s} {m['slug']}")
        print(f"  {m['snippet'][:120]}...\n")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "build":
        build_index()
    elif sys.argv[1] == "search" and len(sys.argv) > 2:
        search_index(" ".join(sys.argv[2:]))
    else:
        print(__doc__)
