#!/usr/bin/env python3
"""
CaelumSwarm™ — Library Index Agent v1.0
Infrastructure = bibliothèque ordonnée, fiable, consultable par tous les agents.
Chaque fichier catalogué, indexé, accessible.
Validé: CoordAgent, DatabaseGuardian, QuantumAgent
"""

import json, os, hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List

BASE = Path(__file__).parent.parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)
LIBRARY_INDEX_FILE = DATA / "library_index.json"
AGENT_INBOXES = DATA / "agent_inboxes.json"

# Catégories bibliothèque
LIBRARY_CATEGORIES = {
    "engines": {
        "emoji": "⚙️",
        "path": "swarm/intelligence",
        "pattern": "*.py",
        "description": "Engines Python CSDDD — avg_composite=61.03",
        "tag": "ENGINE"
    },
    "routes": {
        "emoji": "🛣️",
        "path": "app/api",
        "pattern": "**/route.ts",
        "description": "Routes API Next.js avec sealResponse",
        "tag": "ROUTE"
    },
    "dashboards": {
        "emoji": "📊",
        "path": "app/dashboard",
        "pattern": "**/page.tsx",
        "description": "Dashboards React avec GaugeRing",
        "tag": "DASHBOARD"
    },
    "sidebar_icons": {
        "emoji": "🎨",
        "path": "components",
        "pattern": "sidebar-icons*.tsx",
        "description": "Icônes SVG Sidebar — sans doublons",
        "tag": "ICON"
    },
    "scripts": {
        "emoji": "🤖",
        "path": "scripts",
        "pattern": "*.py",
        "description": "Scripts infrastructure CaelumSwarm™",
        "tag": "SCRIPT"
    },
    "data_files": {
        "emoji": "💾",
        "path": "data",
        "pattern": "*.json",
        "description": "Bases de données JSON — versionnées",
        "tag": "DATA"
    },
    "protocols": {
        "emoji": "📜",
        "path": "docs/protocols",
        "pattern": "*.md",
        "description": "Protocoles officiels CaelumSwarm™",
        "tag": "PROTOCOL"
    },
    "documentation": {
        "emoji": "📚",
        "path": "docs",
        "pattern": "*.md",
        "description": "Documentation générale",
        "tag": "DOC"
    }
}

def build_index() -> Dict:
    """Construire l'index complet de la bibliothèque."""
    index = {
        "version": "1.0.0",
        "built_at": datetime.now().isoformat(),
        "categories": {},
        "total_files": 0,
        "search_index": {}
    }

    for cat_key, cat_info in LIBRARY_CATEGORIES.items():
        cat_path = BASE / cat_info["path"]
        if not cat_path.exists():
            index["categories"][cat_key] = {"files": [], "count": 0}
            continue

        files = []
        for f in sorted(cat_path.glob(cat_info["pattern"])):
            if f.is_file() and "__pycache__" not in str(f):
                rel_path = str(f.relative_to(BASE))
                size = f.stat().st_size
                entry = {
                    "path": rel_path,
                    "name": f.name,
                    "size_bytes": size,
                    "tag": cat_info["tag"],
                    "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")
                }
                files.append(entry)
                # Ajouter au search index
                index["search_index"][f.name.lower()] = rel_path
                index["search_index"][rel_path.lower()] = rel_path

        index["categories"][cat_key] = {
            "emoji": cat_info["emoji"],
            "description": cat_info["description"],
            "files": files,
            "count": len(files)
        }
        index["total_files"] += len(files)

    return index

def search_library(keyword: str, index: Dict) -> List[Dict]:
    """Chercher dans la bibliothèque."""
    results = []
    keyword_lower = keyword.lower()

    for cat_key, cat_data in index.get("categories", {}).items():
        for f in cat_data.get("files", []):
            if (keyword_lower in f["name"].lower() or
                keyword_lower in f["path"].lower()):
                results.append({**f, "category": cat_key})

    return results

def print_library(index: Dict):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n\033[1m\033[96m{'═'*70}\033[0m")
    print(f"\033[1m\033[96m  CaelumSwarm™ — Bibliothèque Infrastructure v1.0\033[0m")
    print(f"\033[1m\033[96m  Ordonnée · Fiable · Accessible · Versionnée\033[0m")
    print(f"\033[1m\033[96m  {timestamp}\033[0m")
    print(f"\033[1m\033[96m{'═'*70}\033[0m\n")

    for cat_key, cat_data in index["categories"].items():
        if cat_data["count"] == 0:
            continue
        emoji = cat_data.get("emoji", "📁")
        print(f"  {emoji} \033[1m{cat_key.upper()}\033[0m — {cat_data['description']}")
        print(f"     {cat_data['count']} fichier(s)")

        # Afficher 5 premiers
        for f in cat_data["files"][:5]:
            size_kb = f["size_bytes"] / 1024
            print(f"     \033[92m✓\033[0m {f['name']:45} {size_kb:.1f}KB")

        if cat_data["count"] > 5:
            print(f"     \033[90m... et {cat_data['count']-5} autres\033[0m")
        print()

    print(f"  \033[1m{'─'*70}\033[0m")
    print(f"\033[1m  ✓ {index['total_files']} fichiers indexés dans la bibliothèque\033[0m")
    print(f"  ✓ Recherche: python3 scripts/library_index_agent.py --search <mot-clé>")
    print(f"  ✓ Index: data/library_index.json")
    print(f"\033[1m\033[96m{'═'*70}\033[0m\n")

def notify_agents(index: Dict):
    if not AGENT_INBOXES.exists():
        return
    try:
        inboxes = json.loads(AGENT_INBOXES.read_text())
        msg = {
            "from": "LibraryIndexAgent",
            "timestamp": datetime.now().isoformat(),
            "subject": f"Bibliothèque indexée: {index['total_files']} fichiers",
            "content": "Consulter data/library_index.json pour accéder à tous les fichiers",
            "priority": "NORMAL",
            "index_path": "data/library_index.json"
        }
        for agent in ["CoordAgent", "GitAgent", "EngineAgent", "QAAgent", "SidebarAgent"]:
            inboxes.setdefault("inboxes", {}).setdefault(agent, []).append(msg)
            inboxes["inboxes"][agent] = inboxes["inboxes"][agent][-50:]
        AGENT_INBOXES.write_text(json.dumps(inboxes, indent=2, ensure_ascii=False))
    except:
        pass

if __name__ == "__main__":
    import sys

    index = build_index()
    LIBRARY_INDEX_FILE.write_text(json.dumps(index, indent=2, ensure_ascii=False))

    if "--search" in sys.argv:
        idx = sys.argv.index("--search")
        keyword = sys.argv[idx+1] if idx+1 < len(sys.argv) else "engine"
        results = search_library(keyword, index)
        print(f"\n{len(results)} résultats pour '{keyword}':")
        for r in results[:10]:
            print(f"  [{r['tag']}] {r['path']}")

    elif "--stats" in sys.argv:
        for cat, data in index["categories"].items():
            if data["count"] > 0:
                print(f"  {cat}: {data['count']} fichiers")
        print(f"  TOTAL: {index['total_files']}")

    else:
        print_library(index)
        notify_agents(index)
