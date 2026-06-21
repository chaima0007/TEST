#!/usr/bin/env python3
"""
Caelum KB — Local FAISS index builder & search.
Usage:
  python3 tools/kb_index.py build   # Build index from KB files
  python3 tools/kb_index.py search "CCO automobile LkSG"
"""
from __future__ import annotations
import argparse
import json
import os
import pickle
import sys
from pathlib import Path

KB_DIR = Path("data/knowledge_base")
INDEX_DIR = KB_DIR / "index"
INDEX_FILE = INDEX_DIR / "kb.faiss"
META_FILE = INDEX_DIR / "kb_meta.pkl"

def load_documents() -> list[dict]:
    docs = []
    for kind in ["companies", "personas", "playbooks"]:
        folder = KB_DIR / kind
        if not folder.exists():
            continue
        for f in sorted(folder.iterdir()):
            if f.suffix in (".json", ".md"):
                text = f.read_text(encoding="utf-8")
                docs.append({"id": f.stem, "type": kind.rstrip("s"), "path": str(f), "text": text[:2000]})
    return docs

def build_index(docs: list[dict]) -> None:
    try:
        import faiss
        import numpy as np
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("Install deps: pip install faiss-cpu sentence-transformers")
        sys.exit(1)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    texts = [d["text"] for d in docs]
    print(f"Embedding {len(texts)} documents...")
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    embeddings = np.array(embeddings, dtype="float32")
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, str(INDEX_FILE))
    with open(META_FILE, "wb") as fh:
        pickle.dump(docs, fh)
    print(f"Index built: {len(docs)} docs → {INDEX_FILE}")

def search_index(query: str, top_k: int = 5) -> list[dict]:
    try:
        import faiss
        import numpy as np
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("Install deps: pip install faiss-cpu sentence-transformers")
        sys.exit(1)
    if not INDEX_FILE.exists():
        print("Index not built. Run: python3 tools/kb_index.py build")
        sys.exit(1)
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    index = faiss.read_index(str(INDEX_FILE))
    with open(META_FILE, "rb") as fh:
        docs = pickle.load(fh)
    vec = model.encode([query], normalize_embeddings=True)
    vec = np.array(vec, dtype="float32")
    scores, indices = index.search(vec, top_k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        doc = docs[idx].copy()
        doc["score"] = float(score)
        doc["excerpt"] = doc["text"][:200].replace("\n", " ")
        results.append(doc)
    return results

def main() -> None:
    parser = argparse.ArgumentParser(description="Caelum KB index")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("build")
    sp = sub.add_parser("search")
    sp.add_argument("query", nargs="+")
    sp.add_argument("--top", type=int, default=5)
    args = parser.parse_args()
    if args.cmd == "build":
        docs = load_documents()
        build_index(docs)
    elif args.cmd == "search":
        query = " ".join(args.query)
        results = search_index(query, top_k=args.top)
        for r in results:
            print(f"[{r['score']:.3f}] [{r['type']}] {r['id']}")
            print(f"  {r['excerpt'][:120]}...")
            print()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
